---
title: Advances in Long-Context Inference, Model Auditing, and Mechanistic Analysis
date: '2026-09-17'
source: arXiv cs.LG
source_url: https://arxiv.org/list/cs.LG/recent
slug: arxiv-cs-lg
header_image: assets/headers/2026-09-17/arxiv-cs-lg.jpg
---

A central thread across today's research focuses on practical system efficiency during model training and inference. To address key-value (KV) cache bottlenecks in long-context models, "Fathom" dynamically adjusts key-scan precision per query over offloaded host memory, while another framework introduces tri-metric routing to balance context compression against latency on commodity GPUs. For model training, "Temperon" cuts computational costs by running standard SGD through the early training phases before handing off optimization to Sharpness-Aware Minimization (SAM) for the final annealing schedule.

On the theoretical and diagnostic side, researchers are analyzing internal representations and verification methods. One study formalizes model update auditing by restricting risk-difference evaluations solely to inputs where the old and new models disagree. Another paper uses activation games to track where Transformers shift from memorization to generalization (grokking), while foundational work on matrix memories tests whether gradient descent can acquire the exact matrix ranks needed to compose key-value bindings. Additionally, a set of lecture notes summarizes pedagogical foundations for Physics-Informed Neural Networks (PINNs) and Neural Operators.

Finally, applied frameworks address bias evaluation, control, and agent adaptation. In multimodal auditing, researchers isolate algorithmic valuation disparities in vision-language models from archival metadata confounders using museum data. For autonomous tasks, a training-free skill evolution framework allows GUI agents to dynamically adapt to shifting user interface layouts, and Diffusion Skill Discovery (DSD) provides a method for learning reusable motor skills for simulated physical tasks.

## Papers

- [Pay Only for Disagreement: Certified No-Regression Verdicts for Model Updates with Matching Label-Complexity Bounds](https://arxiv.org/abs/2609.17560): Proposes a certified framework for auditing risk differences during model updates by evaluating inputs where candidate models disagree.
- [Beyond Static RAG: An Adaptive, Tri-Metric Routing Framework for Efficient Long-Context Inference on Commodity GPUs](https://arxiv.org/abs/2609.17564): Introduces an adaptive routing mechanism to avoid key-value cache contention and memory overhead when deploying retrieval-augmented generation on hardware like NVIDIA T4 GPUs.
- [Where Grokking Happens: Distributed Utility and Fourier Recoding Without a Module Switch](https://arxiv.org/abs/2609.17571): Uses activation games to localize where Transformers transition from memorization to generalization during training.
- [Disentangling Algorithmic Bias from Archival Artifacts: A Controlled Audit of Vision-Language Model Valuation in Metropolitan Museum Archives](https://arxiv.org/abs/2609.17572): Audits CLIP models on historical artwork metadata to separate direct algorithmic valuation biases from existing archival metadata confounders.
- [Temperon: Full-Time SAM Quality at a Third Less Wall-Clock](https://arxiv.org/abs/2609.17575): Reduces training overhead by restricting Sharpness-Aware Minimization to the final phase of an epoch budget after initial SGD optimization.
- [When the Gradient Sees Rank: Provable Necessity, Causal Recruitment, and Composition in Trained Matrix Memories](https://arxiv.org/abs/2609.17594): Analyzes whether gradient descent can effectively learn the necessary matrix rank required for linear key-value binding and composition.
- [Prior-Free Competitive Ratios for Improving Bandits: Scale, Curvature and Horizon Are Free, but Not Jointly Under Noise](https://arxiv.org/abs/2609.17595): Explores theoretical competitive ratio bounds for multi-armed bandit algorithms operating on nondecreasing, concave reward curves under noise.
- [Lecture notes on Physics Informed Neural Networks, Neural Operators, and their applications](https://arxiv.org/abs/2609.17638): Summarizes a doctoral-level curriculum covering Physics-Informed Neural Networks and Neural Operators for scientific computing tasks.
- [Fathom: Per-Query Read Depth for Sparse Decoding over Offloaded KV Caches](https://arxiv.org/abs/2609.17652): Presents a decoding strategy that dynamically adjusts key-scan read depth per query to relieve memory traffic during long-context LLM inference.
- [Reflect, Revise, Reuse: Training-Free Skill Evolution for GUI Agents](https://arxiv.org/abs/2609.17653): Details a skill framework enabling graphical user interface agents to adapt procedural knowledge without retraining when interface layouts change.
- [Regularized Least Squares Training of Quadratic Neural Networks with Applications to System Identification](https://arxiv.org/abs/2609.17654): Derives closed-form approximate solutions and optimization lower bounds for regularized quadratic neural networks.
- [DSD: Learning Diverse and Reusable Motor Skills via Diffusion Skill Discovery](https://arxiv.org/abs/2609.17682): Proposes a diffusion-based framework for learning diverse, task-agnostic motor skill repertoires in simulated agents.
