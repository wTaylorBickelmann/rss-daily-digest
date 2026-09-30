---
title: Advances in Model Compression, Physics-Informed Operators, and Generalization
  Theory
date: '2026-09-30'
source: arXiv cs.LG
source_url: https://arxiv.org/list/cs.LG/recent
slug: arxiv-cs-lg
header_image: assets/headers/2026-09-30/arxiv-cs-lg.jpg
---

This collection of research focuses heavily on computational efficiency and structured model optimization. For large-scale language models, methods like Orthogonal Matching Pursuit are applied to prune experts in Mixture-of-Experts architectures without retraining, while deterministic product-aware rounding improves the precision of quantized matrix multiplication. For broader optimization workflows, energy-aware metrics are integrated into Bayesian optimization to prevent excessive computational overhead during multi-disciplinary design tasks.

In physical and biological domains, researchers incorporate domain-specific priors into learning models. Neural operator architectures are augmented with physical superposition principles to predict turbine film cooling layouts, and domain adaptation benchmarks for physical vibration sensors are re-evaluated under strict held-out physical bearing splits. For medical signal processing, specialized agent benchmarks evaluate how language models conduct multi-step, tool-assisted analysis over extended temporal horizons.

Methodological evaluations and theoretical analyses also highlight limitations in existing training and evaluation paradigms. Theoretical proofs link quotient linear stability to input smoothness and model generalization under structural symmetries. In application contexts, closed-loop evaluation frameworks reveal compounding errors in emergency department simulators that standard next-event accuracy metrics miss, while new continual learning methodologies explore biologically constrained memory consolidation and long-horizon steady-state evaluation metrics.

## Covered Papers

* [Replay in the Silent Degrees of Freedom: Continual Learning Without an Offline Phase](https://arxiv.org/abs/2609.31630): Introduces a biologically inspired continual learning mechanism that consolidates memory through local circuit off-periods without requiring a separate offline phase.
* [OMP-MoE: Efficient Expert Pruning for Mixture-of-Experts LLMs via Orthogonal Matching Pursuit](https://arxiv.org/abs/2609.31631): Presents a training-free expert pruning method using Orthogonal Matching Pursuit to reduce memory overhead in Mixture-of-Experts language models while accounting for expert interdependencies.
* [EEGAgentBench: Benchmarking LLM Agents on Short- and Long-Horizon EEG Analysis](https://arxiv.org/abs/2609.31632): Proposes a benchmark to assess large language model agents on complex, multi-step EEG analysis tasks requiring tool orchestration and long-horizon reasoning.
* [Enhancing generalization in endwall film cooling prediction: Incorporating the superposition principle into transformer-based neural operators](https://arxiv.org/abs/2609.31633): Integrates the film cooling superposition principle into transformer-based neural operators to improve prediction accuracy for turbine endwall layouts.
* [Symmetry-quotient Flatness and Generalization](https://arxiv.org/abs/2609.31634): Establishes theoretical connections between quotient stability, flatness, input smoothness, and generalization in neural networks with structural symmetries.
* [What Next-Event Accuracy Cannot See: Closed-Loop Evaluation of Emergency Department Trajectory Simulators](https://arxiv.org/abs/2609.31635): Introduces a closed-loop evaluation framework for emergency department trajectory models to capture compounding errors missed by standard next-event accuracy metrics.
* [Grounding Vision-Language Models in Driving Semantics: A Multi-Dataset Predicate Framework for Explainable Reasoning](https://arxiv.org/abs/2609.31636): Develops a deterministic predicate framework using geometric and kinematic variables to ground vision-language models in verifiable driving semantics.
* [FIDAL: Diversity-Aware Federated Active Learning Under Real-World Distribution Shifts](https://arxiv.org/abs/2609.31637): Proposes a federated active learning framework designed to mitigate domain shifts, class imbalances, and out-of-distribution noise during decentralized training.
* [Energy-aware frugal Bayesian optimization](https://arxiv.org/abs/2609.31638): Introduces an acquisition framework that balances computational energy overhead with prediction accuracy in sample-efficient Bayesian optimization.
* [When Does Domain Adaptation Help on Physical Vibration Sensors? A Held-Out-Bearing Study of Neural-Operator and Convolutional Models](https://arxiv.org/abs/2609.31639): Evaluates domain adaptation methods for bearing fault diagnosis under a strict held-out physical bearing evaluation split.
* [Measure Learning at Steady State: A BIRD-SQL Formula 1 Case Study](https://arxiv.org/abs/2609.31640): Evaluates in-context learning as a continual learning system by measuring long-horizon steady-state performance gains on a SQL task sequence.
* [Product-Aware Deterministic Rounding for Quantized Matrix Multiplication](https://arxiv.org/abs/2609.31641): Proposes a deterministic scalar rounding strategy that reduces matrix multiplication error by optimizing rounding choices across active scalar interactions.
