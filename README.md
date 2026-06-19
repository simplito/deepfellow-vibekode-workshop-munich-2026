# Building reliable AI systems with DeepFellow

Workshop materials for **VibeKode Munich 2026** — session *Connecting AI*.

## What is DeepFellow?

DeepFellow is an open-source AI gateway that sits between your applications and any LLM inference backend (OpenAI, Ollama, and others). It provides a unified OpenAI-compatible API with a plugin system for anonymization, routing, observability, and more — so teams can build reliable, privacy-aware AI pipelines without locking into a single provider.

## Workshop setup

Each participant runs a local stack:

| Component | Where |
|---|---|
| **DFServer** | laptop |
| **DFInfra (Child)** | laptop — connected to AWS via `mesh connect` |
| **DFInfra (AWS)** | shared cloud node (×1 per team) |

Models available out of the box: `gemma` (via Ollama on AWS) and `gpt` (via openAI on the local Child infra).

## Plugins in this repo

### `df_infra_tap`

A read-only observability plugin that taps the exact payload crossing the infra boundary — after anonymization runs, before deanonymization on the way back.

```
on_request_text  →  logs what leaves for infra  (already anonymized)
on_response      ←  logs what comes back         (still anonymized)
```

It never mutates the request or response. Use it to verify that your anonymization pipeline is doing what you think it is, or to debug unexpected model behaviour at the raw-infra level.

**Priority:** `0` (appended after the anonymizer, which runs at priority `1`).

#### Install

Drop `df_infra_tap/` into your DFServer plugins directory and restart the server. The plugin self-registers; no additional config required.

## Links

- DeepFellow docs: <https://vibekode.it/connecting-ai/reliable-ai-systems-deepfellow/>
- VibeKode 2026: <https://vibekode.it>
