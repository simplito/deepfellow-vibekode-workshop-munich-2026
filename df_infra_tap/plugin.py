"""Infra tap plugin.

Observes the data that actually crosses the boundary to the inference infra,
without modifying it. It registers a ChatCompletionsController into
``request.state.chat_completions_controllers``.

Because ``before_request`` hooks run in priority order (higher first) and the
anonymization plugin uses ``priority: 1``, this plugin uses ``priority: 0`` so
its controller is appended *after* the anonymizer's controller. As a result:

  * ``on_request_text`` sees the text exactly as it leaves for infra
    (already anonymized, since the anonymizer's controller runs first).
  * ``on_response`` / ``on_response_chunk`` see the raw response from infra
    (still anonymized) because both fire before the response processors run
    the deanonymization step.

If the anonymizer is not active for a given model, this plugin still logs the
real payload sent to infra (which in that case is the unmodified text).
"""

from openai.types.chat import ChatCompletion, ChatCompletionChunk

from server.core.plugin_manager import BasePlugin, PluginContext
from server.models.chat import ChatCompletionRequest
from server.services.chat_completions.chat_completions_service import ChatCompletionsController
from server.utils.logger import uvicorn_logger

# Truncate logged payloads to keep logs readable. Set to None to disable.
MAX_LOG_LEN: int | None = 4000


def _clip(text: str) -> str:
    if MAX_LOG_LEN is not None and len(text) > MAX_LOG_LEN:
        return f"{text[:MAX_LOG_LEN]}… [+{len(text) - MAX_LOG_LEN} chars]"
    return text


class InfraTapController(ChatCompletionsController):
    """Read-only tap on the data exchanged with infra. Never mutates anything."""

    def on_request_text(self, text: str) -> str:
        """Log the text as it is sent to infra, then pass it through unchanged."""
        uvicorn_logger.info(f"🔎 [INFRA TAP] → out to infra: {_clip(text)}")
        return text

    def on_response(self, response: ChatCompletion) -> ChatCompletion:
        """Log the raw (pre-deanonymization) non-stream response from infra."""
        for choice in response.choices:
            content = choice.message.content
            if isinstance(content, str):
                uvicorn_logger.info(f"🔎 [INFRA TAP] ← in from infra: {_clip(content)}")
        return response

    def on_response_chunk(self, chunk: ChatCompletionChunk) -> ChatCompletionChunk:
        """Log the raw (pre-deanonymization) stream chunk from infra."""
        for choice in chunk.choices:
            delta = choice.delta.content
            if delta:
                uvicorn_logger.info(f"🔎 [INFRA TAP] ← chunk from infra: {_clip(delta)}")
        return chunk


class DFInfraTapPlugin(BasePlugin):
    """Register a read-only controller that taps the infra boundary."""

    async def initialize(self) -> bool:
        """Inform when the plugin is initialized."""
        uvicorn_logger.info("🔎 [INFRA TAP] initialized")
        return True

    async def before_request(self, context: PluginContext) -> PluginContext:
        """Append the tap controller to the request's controller chain."""
        request = context.request
        if request is None or not context.function_kwargs or not context.function_kwargs.get("body"):
            uvicorn_logger.warning("🔎 [INFRA TAP] no request body, skipping")
            return context

        body: ChatCompletionRequest = context.function_kwargs["body"]
        uvicorn_logger.info(f"🔎 [INFRA TAP] tapping request for model {body.model}")

        if not hasattr(request.state, "chat_completions_controllers"):
            request.state.chat_completions_controllers = []
        request.state.chat_completions_controllers.append(InfraTapController())

        self.set_plugin_header(context)
        return context
