# Building reliable AI systems with DeepFellow

Workshop materials for **VibeKode Munich 2026**, session *Connecting AI*.

**Trainers:** Piotr Zalewa & Michał Komorowski (DeepFellow core team)

---

## What you will build

A working DeepFellow proxy that sits between your application and one or more LLM backends. By the end of the session you will have wired up model routing, access control, observability, and a production-ready API endpoint, with running code you can carry back to your own stack.

No prior DeepFellow experience required. Familiarity with the command line is enough.

## What is DeepFellow?

DeepFellow is an open-source AI gateway with an OpenAI-compatible API and a plugin system for anonymization, routing, and observability. It lets you orchestrate multiple models for different tasks, apply access control, and keep full control over how AI is used inside your deployments, whether you are building internal tools, customer-facing features, or regulated on-prem systems.

Because the trainers built DeepFellow, you get answers straight from the source.

## Workshop setup

OVH servers are provided. Bring a laptop with internet access and an SSH client.

| Component | Where |
|---|---|
| **DFServer** | laptop |
| **DFInfra (Child)** | laptop, connected to the cloud node via `mesh connect` |
| **DFInfra (cloud)** | shared OVH node (×1 per team) |

Two models out of the box: `gemma` (Ollama on the cloud node) and `gpt` (openAI on the local Child infra).

## Plugins in this repo

### `df_infra_tap`

A read-only observability plugin that logs the exact payload at the infra boundary: after anonymization, before DFServer deanonymizes the response.

```
on_request_text  →  logs what leaves for infra  (already anonymized)
on_response      ←  logs what comes back         (still anonymized)
```

The plugin never mutates. Use it to verify your anonymization pipeline or debug unexpected model behaviour at the raw-infra level.

**Priority:** `0`. The anonymizer runs at priority `1` and prepends its controller; this plugin appends after it.

#### Install

Drop `df_infra_tap/` into your DFServer plugins directory and restart. The plugin registers itself.

## Links

- DeepFellow docs: <https://vibekode.it/connecting-ai/reliable-ai-systems-deepfellow/>
- VibeKode 2026: <https://vibekode.it>
