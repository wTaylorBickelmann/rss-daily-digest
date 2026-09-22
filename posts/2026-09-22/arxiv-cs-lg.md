---
title: Advances in Model Distillation Rigor, Spatial Representation, and Efficient
  Inference
date: '2026-09-22'
source: arXiv cs.LG
source_url: https://arxiv.org/list/cs.LG/recent
slug: arxiv-cs-lg
header_image: assets/headers/2026-09-22/arxiv-cs-lg.jpg
---

Recent machine learning research from arXiv cs.LG highlights fundamental refinements in efficiency, experimental methodology, and domain-specific architectures. In model compression and optimization, studies introduce PRQuant to address low-bit quantization bottlenecks caused by activation outliers, alongside ZoAQ, which reduces query costs in zeroth-order optimization through query reuse. Methodological rigor also receives critical attention: research on selective on-policy distillation reveals that using a single shared learning rate across different selectors acts as a confounded variable rather than a neutral control, while analysis in hardware evaluation demonstrates that cross-device performance ranking correlation does not guarantee target feasibility under strict latency and energy budgets.

Spatial modeling and environmental forecasting models are increasingly integrating physical constraints and inductive representations. StationPDE incorporates continuous surface PDE learning into discrete multi-station weather modeling to retain physical consistency, while SolarFlowRefiner utilizes refinement-aware flow matching to downscale coarse solar radiation fields. For human mobility analysis, new architectures establish distance-aware location embeddings capable of generalizing to unseen geographic regions, supported by deep representation learning techniques that infer activity purpose from passive location data.

Finally, advancements in decision-making and applied safety emphasize robust execution and fairness. Researchers present state-estimation correction techniques designed to mitigate perception errors before they trigger unsafe control actions in autonomous systems. To improve long-horizon agents, novel methods extract compact, state-conditioned walkthroughs from sparse-reward trajectories that contain detours or failures. In clinical ML, fairness audits are applied to predictive models for medication-assisted opioid treatment to ensure equitable risk evaluation across patient demographics.

## Included Papers

- [PRQuant: Permutation Residual Quantization for Low-Overhead Inference](https://arxiv.org/abs/2609.22106): This paper proposes a permutation residual quantization approach to mitigate accuracy degradation caused by activation outliers during low-bit linear layer inference.
- [Generalized Multimodal Foundation Model](https://arxiv.org/abs/2609.22107): The authors examine methods for enabling multimodal fusion models to generalize dynamically to unseen modalities and tasks beyond pre-defined input types.
- [Correcting Learning-based Perception for Safety](https://arxiv.org/abs/2609.22108): The paper introduces a two-step state estimation correction framework to prevent machine learning perception errors from causing unsafe control outputs in autonomous systems.
- [A Shared Learning Rate Is Not a Neutral Control in Selective On-Policy Distillation](https://arxiv.org/abs/2609.22109): This study demonstrates that holding learning rates fixed across different token selection methods in on-policy distillation introduces evaluation bias rather than serving as a neutral control.
- [Toward Fairness in Machine Learning Models for Predicting Treatment Retention and Premature Discontinuation in Medication for Opioid Use Disorder](https://arxiv.org/abs/2609.22113): The authors investigate and address algorithmic fairness concerns in machine learning models used to predict patient retention in opioid use disorder treatment programs.
- [ZoAQ: Adaptive Zeroth-Order Querying via Query-Reuse Coupling](https://arxiv.org/abs/2609.22115): This work presents an adaptive zeroth-order optimization technique that reduces function evaluation overhead by coupling perturbation query reuse with reliability checks.
- [LE4Mob: Towards Inductive, Distance-Aware and General-Purpose Location Embedding for Human Mobility Modelling](https://arxiv.org/abs/2609.22117): The paper proposes an inductive location embedding approach that retains geographic distance constraints to represent unseen spatial locations in mobility modeling.
- [Success Leaves Detours: Learning Executable Walkthroughs for Long-Horizon Agents](https://arxiv.org/abs/2609.22120): The authors introduce a framework for extracting compact, state-conditioned executable walkthroughs from noisy, sparse-reward agent trajectories.
- [Modelling daily activity patterns from mobile phone location data via deep representation learning](https://arxiv.org/abs/2609.22121): This study leverages deep representation learning to infer human daily activity purposes from passive mobile phone location tracks and spatial contextual data.
- [Rank Portability Does Not Imply Feasibility Portability: Target-Specific Evaluation of Joint Hardware Constraints](https://arxiv.org/abs/2609.22122): The paper demonstrates that high architectural rank correlation across hardware devices does not ensure that model selection transfers under joint latency and energy feasibility limits.
- [StationPDE: Station-Oriented Surface PDE Learning for Multi-Station Multivariate Weather Forecasting](https://arxiv.org/abs/2609.22123): This work combines station-level surface partial differential equation learning with statistical models to improve physical consistency in multivariate weather forecasting.
- [SolarFlowRefiner: Refinement-Aware Flow Matching for Surface Solar Radiation Downscaling](https://arxiv.org/abs/2609.22126): The paper presents a flow-matching model designed to downscale coarse reanalysis weather data into high-resolution surface solar radiation fields.
