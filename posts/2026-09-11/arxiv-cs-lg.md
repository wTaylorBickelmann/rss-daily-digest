---
title: Advances in Activation Steering, Conformal Calibration, and Continual RL
date: '2026-09-11'
source: arXiv cs.LG
source_url: https://arxiv.org/list/cs.LG/recent
slug: arxiv-cs-lg
header_image: assets/headers/2026-09-11/arxiv-cs-lg.jpg
---

Recent research in machine learning focuses heavily on interpreting, controlling, and evaluating complex models. Work in large language model (LLM) internal mechanics explores GEOSTEER, a method utilizing geodesic optimization to achieve norm-preserving activation steering without representation collapse, while parallel investigations analyze "perfect aliasing" failures in truth probes when task instructions align with truthful outputs. In continual reinforcement learning (RL), foundational work formalizes the stability-plasticity tradeoff via an information-theoretic Bellman optimality equation, while hierarchical RL research leverages directed graph connectivity to shape dense reward functions.

Methodological improvements to model reliability and calibration also take center stage. Studies on ordinal classification identify "center-class hedging" and introduce adaptive margin loss functions to penalize intermediate-class biases. In uncertainty estimation, conformal prediction frameworks are extended to support calibration transfer across domain shifts, and counterfactual marginalization is proposed as a test-time evaluation method using counterfactual generators to detect model reliance on shortcut features. Notably, time-series forecasting research demonstrates that joint heteroscedastic scale estimation directly improves point prediction accuracy.

Domain-specific applications illustrate the practical deployment of these specialized architectures. Research in trajectory modeling combines mixture-of-experts architectures with text-derived domain context for long-term vessel prediction. In federated learning, new rotating-coordinator paradigms tackle Byzantine clients and bandwidth limits for edge-based fire detection. Additionally, zero-shot structural engineering merges frozen diffusion models with topology optimization for rib design, and systematic reviews synthesize deep learning progress in lung cancer imaging.

## Papers

- [M3-Former: Multimodal Transformer with Mixture-of-Experts for Long-Term Vessel Trajectory Prediction](https://arxiv.org/abs/2609.10559): Combines language model context and mixture-of-experts architectures with static vessel attributes to improve long-term maritime trajectory forecasting.
- [Halo: Improving forecast accuracy through heteroscedastic estimation](https://arxiv.org/abs/2609.10589): Demonstrates that estimating scale parameters alongside location parameters directly improves point estimate accuracy in time series forecasting models.
- [Zero-shot rib design: merging training-free generative prior with topology optimization](https://arxiv.org/abs/2609.10643): Integrates frozen text-to-image diffusion priors with topology optimization to synthesize structural load-bearing rib patterns guided by natural language.
- [Byzantine-Robust Federated Fire Detection with a Rotating Coordinator](https://arxiv.org/abs/2609.10647): Introduces a rotating coordinator setup for federated indoor fire detection to address uplink bandwidth limits and malicious or faulty edge devices.
- [Artificial Intelligence Algorithms for the Detection of Pathologies Related to Lung Cancer through Image Analysis using Convolutional Neural Networks and Data Augmentation: a systematic mapping of the literature](https://arxiv.org/abs/2609.10652): Presents a systematic mapping of literature regarding convolutional neural networks and data augmentation for lung cancer image analysis.
- [GEOSTEER: Geodesic Optimization for Activation Steering in Large Language Models](https://arxiv.org/abs/2609.10658): Applies geodesic optimization to perform norm-preserving activation steering in language models without causing activation norm collapse.
- [Conformal Calibration Transfer](https://arxiv.org/abs/2609.10737): Extends conformal prediction guarantees to deployment target spaces where labeled calibration data is only available in a source space.
- [The Truth Was Never Gone: Perfect Aliasing in Compliant-Context Truth Probes](https://arxiv.org/abs/2609.10739): Examines the phenomenon of perfect aliasing, where truth probes trained on compliant contexts fail to separate truthfulness from task-prescribed actions.
- [Adaptive Margin Ordinal Loss: Penalizing Center-Class Hedging in Ordinal Classification](https://arxiv.org/abs/2609.10752): Proposes an adaptive margin loss to correct center-class hedging, a failure mode where ordinal classifiers default to predicting middle classes.
- [A Bellman Optimality Equation for Plasticity](https://arxiv.org/abs/2609.10776): Formulates the stability-plasticity dilemma in continual reinforcement learning using an information-theoretic Bellman optimality framework.
- [Counterfactual Marginalisation: Framework for Evaluating Robustness to Nuisance Variables](https://arxiv.org/abs/2609.10778): Evaluates model robustness against demographic and acquisition shortcuts at test time using counterfactual image generation.
- [From Connectivity to Rewards: Dense Reward Learning with Directed State Graphs](https://arxiv.org/abs/2609.10781): Uses directed graph connectivity within goal-conditioned hierarchical reinforcement learning to construct dense reward functions.
