# Building reliable AI systems with DeepFellow

Workshop materials for **VibeKode Munich 2026**, session *Connecting AI*.

**Trainers:** Piotr Zalewa & Michał Komorowski (DeepFellow core team)

## What you will build

A working DeepFellow proxy that sits between your application and one or more LLM backends. By the end of the session you will have wired up model routing, access control, observability, and a production-ready API endpoint, with running code you can carry back to your own stack.

No prior DeepFellow experience required. Familiarity with the command line is enough.

## What is DeepFellow?

DeepFellow is an open-source AI gateway with an OpenAI-compatible API and a plugin system for anonymization, routing, and observability. It lets you orchestrate multiple models for different tasks, apply access control, and keep full control over how AI is used inside your deployments, whether you are building internal tools, customer-facing features, or regulated on-prem systems.

Because the trainers built DeepFellow, you get answers straight from the source.

## Prerequisites

- Repo: [bit.ly/deepfellow-munich-repo](https://bit.ly/deepfellow-munich-repo)
- Chat: [bit.ly/deepfellow-munich-chat](https://bit.ly/deepfellow-munich-chat)

- [Git 2.30+](https://git-scm.com/downloads)
- [Python 3.13.x](https://www.python.org/downloads/)
- [Docker Engine 28+](https://docs.docker.com/engine/install/)
- Python package manager: [uv](https://docs.astral.sh/uv/) / [pipx](https://pipx.pypa.io/) / pip3
- [Cherry Studio](https://cherryai.com/download)
- bore (see below)

### bore

```bash
# macOS
brew install bore-cli

# Cargo (all platforms)
cargo install bore-cli

# Arch Linux
yay -S bore

# Gentoo
sudo emerge net-proxy/bore

# Prebuilt binaries (Linux, macOS)
# https://github.com/ekzhang/bore/releases
```

## CLI Commands

```bash
# CLI install
curl https://deepfellow.ai/install.sh | bash

# Run the CLI
deepfellow

# DFServer install
deepfellow server install

# Start the DFServer
deepfellow server start
deepfellow server create-admin

# Local DFInfra install
deepfellow infra install

# Expose DFInfra via bore
# In separate terminal
bore local 8086 --to bore.pub

# Update the INFRA_URL
deepfellow infra env set INFRA_URL http://bore.pub:4321
deepfellow infra info

# Connect Infras
deepfellow infra connect wss://<YOUR TEAM INFRA>.workshop-demo.deepfellow.com <DF_MESH_KEY>

# df_infra_tap plugin
cp -r server-plugins/df_infra_tap ~/.deepfellow/server/plugins/
deepfellow server restart
deepfellow server logs -f | grep "INFRA TAP"

# PII anonymization
deepfellow server env set PLUGINS_SETUP '{"df_anonymize_models": ["gpt-5-mini"]}'
```

## Links

- [DeepFellow docs](https://docs.deepfellow.ai)
- [VibeKode workshop page](https://vibekode.it/connecting-ai/reliable-ai-systems-deepfellow/)
- [Workshop Chat](https://hack.chat/?workshop-DF-Munich-2026)

