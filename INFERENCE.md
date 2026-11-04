# Running the preserved model

This document is a preparation checklist, not a claim that this repository has tested Kimi K3 on a particular GPU.

## Official model information

- Upstream model: https://huggingface.co/moonshotai/Kimi-K3
- Review the model card and license before use.
- Follow the model card's current inference instructions and supported runtime versions.

The upstream model documentation lists inference-engine options such as vLLM, SGLang, and TokenSpeed. Check the current model card for the exact supported versions, launch flags, hardware requirements, and any model-specific patches.

## Hardware planning

Kimi K3 is a very large model. Download storage capacity is not the same as inference capacity. Running it requires a suitable multi-GPU server or hosted compute environment, enough GPU memory for the selected precision and context length, and fast interconnect/storage.

Do not assume that a normal gaming PC can run the full model locally. Before buying hardware, compare the model card's requirements with the actual GPU memory, GPU count, interconnect, system RAM, and supported runtime.

## Reproducible deployment record

When you successfully run the model, add a record containing:

- snapshot commit SHA
- snapshot directory path
- inference engine and exact version
- driver, CUDA/ROCm, and operating-system versions
- GPU model/count and available memory
- precision/quantization format
- context length and relevant launch settings
- exact tested launch command
- a basic test prompt and confirmation that generation worked

Do not write access tokens, private endpoints, or other secrets into this repository.

## API serving

If you expose the model through an API, keep authentication, rate limits, and network access controls enabled. Bind to localhost for private testing unless you deliberately configure a secured remote deployment. Never expose an unauthenticated inference server directly to the public internet.
