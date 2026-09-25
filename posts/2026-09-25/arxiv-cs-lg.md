---
title: Methods for Model Auditability, Real-World Time Series, and Multimodal Domain
  Adaptation
date: '2026-09-25'
source: arXiv cs.LG
source_url: https://arxiv.org/list/cs.LG/recent
slug: arxiv-cs-lg
header_image: assets/headers/2026-09-25/arxiv-cs-lg.jpg
---

Modern machine learning research continually encounters discrepancies between simplified operational assumptions and real-world deployment conditions. Recent papers emphasize improving model trust and practical usability through rigorous evaluation protocols and interface corrections. Work in this area addresses visual rendering failures of standard post hoc explainability tools like SHAP and LIME when applied to right-to-left languages, presents a six-property framework for decomposing opaque reinforcement learning policies into auditable discrete rules, and mitigates data leakage in material science tasks by replacing standard image-level evaluation splits with region-held-out validation strategies.

Time-series research is similarly adapting to realistic operational complexities where data is incomplete or continually updated. Recent contributions introduce foundation model techniques designed to handle retroactive data revisions by statistical agencies, avoiding lookahead bias during training and forecasting. Complementary methods address uncertainty quantification in multi-step foundation model forecasts, while infrastructure applications utilize smart-meter electricity data to disentangle co-located residential solar generation and electric vehicle charging patterns.

In specialized scientific domains, hybrid architectures bridge structural and contextual modeling gaps. Researchers report cross-attention fusion methods combining molecular SMILES transformers with graph neural networks for toxicity prediction, variational autoencoder latent-space adaptation to adjust computational fluid dynamics simulations against experimental discrepancies, and spatial context-aware gene program modeling to infer tissue transcriptomics from standard histology slides.

## Papers

* [Stable and Faithful Explanations for Knowledge Tracing](https://arxiv.org/abs/2609.28502): Introduces a validation protocol to evaluate the predictive competitiveness, stability, and retraining-based faithfulness of feature-based explanations in student knowledge tracing models.
* [SMILESGNN: Interpretable Clinical Toxicity Prediction via SMILES-Graph Cross-Attention Fusion](https://arxiv.org/abs/2609.28553): Combines SMILES sequence transformers and graph neural networks via cross-attention fusion to predict drug toxicity while addressing scaffold generalization and class imbalance.
* [CFD Correction of Open Tip Clearance Flow in a Compressor Cascade Using VAE Latent Space Adaptation](https://arxiv.org/abs/2609.28558): Proposes a non-intrusive method using variational autoencoders and latent-space adaptation to correct discrepancies in compressor cascade fluid dynamics simulations.
* [CARE: Condition-Aware Representation Regularization for Diffusion Models](https://arxiv.org/abs/2609.28561): Improves diffusion model training efficiency and generation quality by incorporating target condition signals directly into representation regularization.
* [SpaFactor: Lightweight Spatial Context-Aware Gene Program Modeling for Histology-to-Transcriptomics Inference](https://arxiv.org/abs/2609.28563): Predicts spatial gene expression profiles directly from standard tissue histology images using context-aware spatial gene program modeling.
* [When Explanations Cannot Be Read: Measuring and Correcting SHAP and LIME Rendering for Right-to-Left Languages](https://arxiv.org/abs/2609.28565): Identifies and corrects visualization rendering failures when applying feature attribution tools like SHAP and LIME to right-to-left text.
* [Leakage-Safe Machine Learning for Hydrogen Embrittlement Detection in 316L Stainless Steel: A Region-Held-Out Evaluation of Texture and Deep Features in SEM Micrographs](https://arxiv.org/abs/2609.28567): Demonstrates how region-held-out validation splits prevent data leakage and overoptimistic performance when detecting hydrogen embrittlement in electron microscopy images.
* [Time-Series Foundation Models That Understand Data Revisions](https://arxiv.org/abs/2609.28576): Introduces VINTAGE-TS, an approach that allows time-series foundation models to incorporate historical data revisions without exposing predictions to future information.
* [Uncovering Residential PV-EV Co-Adoption from Smart-Meter Data: Load Archetypes and Detection for Demand-Side Planning](https://arxiv.org/abs/2609.28578): Analyzes smart-meter electricity data to identify behavioral load archetypes and detect co-located residential solar and electric vehicle adoption.
* [Auditability Is Not One Property: Rule Overlap, Behavioural Agreement, and Composition in Reinforcement Learning](https://arxiv.org/abs/2609.28581): Formulates a six-property framework to evaluate and compose reinforcement learning policies using auditable discrete behavioral rules.
* [SGA: Uncertainty Quantification for Multi-Step Forecasting in Time Series Foundation Models](https://arxiv.org/abs/2609.28582): Provides an uncertainty quantification method tailored to manage branching uncertainty in multi-step time-series foundation model forecasts.
* [TAM-Chain: Multi-Scale Thyroid Cytology Classification via Absorbing Markov Chains and Shannon Entropy Uncertainty Quantification for False-Negative Suppression and Domain-Shift Adaptation](https://arxiv.org/abs/2609.28590): Applies absorbing Markov chains and entropy-based uncertainty quantification to reduce false negatives and domain shift errors in thyroid cytology image classification.
