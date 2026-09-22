---
title: Hugging Face Integrates llama.cpp Quants and Expands MLX Support
date: '2026-09-22'
source: Hugging Face Blog
source_url: https://huggingface.co/blog
slug: huggingface-blog
header_image: assets/headers/2026-09-22/huggingface-blog.jpg
---

Hugging Face released two major updates focused on local inference integration and hardware-specific framework support. The core updates address compatibility between widely used quantization formats and ecosystem expansion for Apple Silicon machine learning workflows.

First, the Hugging Face `transformers` library now natively supports executing quantized models created for `llama.cpp`. This integration allows developers to load and run GGUF and `llama.cpp` quantized weights directly within Python workflows using standard `transformers` pipelines, reducing friction between C++ optimized quant formats and PyTorch-centric toolchains.

Additionally, Hugging Face announced that Jun Kim, the creator and maintainer of the oMLX project, has joined the organization. This move is aimed at strengthening support for the MLX open-source community and improving machine learning framework capabilities tailored for Apple Silicon architectures.

## Covered Items

- [Transformers now runs llama.cpp quants](https://huggingface.co/blog/transformers-llama-cpp-quants): Hugging Face added native support for running `llama.cpp` quantized model formats directly inside the `transformers` library.
- [Jun Kim, oMLX creator and maintainer, joins Hugging Face to support the MLX community](https://huggingface.co/blog/omlx): Jun Kim has joined Hugging Face to advance ecosystem support for Apple Silicon users working with MLX and oMLX.
