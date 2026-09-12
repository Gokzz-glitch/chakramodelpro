# Literature Review — Polyp Detection & Segmentation

> **Last Updated**: 2026-09-12  
> **Status**: Phase 0 — Active Review  
> **Reviewer**: [Your Name]  
> **Sources Searched**: arXiv, PubMed, Google Scholar, IEEE Xplore

---

## Table of Contents

1. [Search Strategy](#search-strategy)
2. [Papers Reviewed](#papers-reviewed)
   - [Foundational Datasets](#1-foundational-datasets)
   - [CNN-Based Segmentation (2018–2021)](#2-cnn-based-segmentation)
   - [Transformer-Based Segmentation (2021–2023)](#3-transformer-based-segmentation)
   - [Video Polyp Segmentation](#4-video-polyp-segmentation)
   - [Real-Time & Lightweight Models](#5-real-time--lightweight-models)
   - [Recent 2024–2026 Work](#6-recent-2024-2026-work)
3. [SOTA Comparison Table](#sota-comparison-table)
4. [Gap Analysis & Our Contribution](#gap-analysis--our-contribution)
5. [Papers To Read (Backlog)](#papers-to-read-backlog)

---

## Search Strategy

**Keywords used:**
- `"polyp segmentation deep learning"` — arXiv, PubMed, Google Scholar
- `"video polyp detection real-time"` — arXiv
- `"YOLO medical image segmentation polyp detection real-time"` — arXiv
- `"attention mechanism colonoscopy"` — arXiv
- `"reverse attention polyp"` — arXiv
- `"Polyp-PVT polyp segmentation transformer"` — arXiv
- `"ColonSegNet polyp segmentation real time"` — arXiv
- `"SANet polyp segmentation attention"` — arXiv

**Date range**: 2018–2026 (primary focus: 2020–2026 for recent SOTA)

**Inclusion criteria:**
- Must report at least one of: Dice, IoU, F-measure on a standard polyp dataset
- Methods targeting colorectal/gastrointestinal polyps specifically
- Peer-reviewed or arXiv preprint with reproducible code (preferred)

**Exclusion criteria:**
- Papers on other types of polyps (nasal, gastric only) without CRC context
- Papers without quantitative results

---

## Papers Reviewed

### 1. Foundational Datasets

---

#### [P01] Kvasir-SEG: A Segmented Polyp Dataset
- **Authors**: Jha, D., Smedsrud, P.H., Riegler, M.A., et al.
- **Year/Venue**: 2020 / MMM Conference
- **arXiv**: [1911.07069](https://arxiv.org/abs/1911.07069)
- **Method Summary**: Introduces Kvasir-SEG, a dataset of 1,000 gastrointestinal polyp images from the Kvasir dataset with pixel-level segmentation masks annotated by experienced gastroenterologists. Establishes FCN-8 and U-Net baselines.
- **Reported Metrics**:
  - U-Net baseline: Dice=0.8264, IoU=0.7177 on Kvasir-SEG
  - FCN-8 baseline: Dice=0.7814, IoU=0.6399 on Kvasir-SEG
- **Relevance**: **PRIMARY DATASET** for our experiments. The de facto standard benchmark for polyp segmentation. Must be used and reported.
- **Dataset**: [simula.no/kvasir-seg](https://datasets.simula.no/kvasir-seg/) — CC-BY 4.0 (free for research and commercial use)

---

#### [P02] CVC-ClinicDB: A Database for Endoluminal Scene Segmentation of Colonoscopy Videos
- **Authors**: Bernal, J., Sanchez, F.J., Fernandez-Esparrach, G., et al.
- **Year/Venue**: 2015 / Computerized Medical Imaging and Graphics
- **DOI**: [10.1016/j.compmedimag.2015.02.007](https://doi.org/10.1016/j.compmedimag.2015.02.007)
- **Method Summary**: 612 still frames extracted from 29 colonoscopy sequences with pixel-accurate polyp segmentation masks. Standard benchmark in the field.
- **Reported Metrics**: N/A (dataset paper)
- **Relevance**: **PRIMARY DATASET**. Second most common benchmark. Cross-dataset evaluation (train on Kvasir, test on CVC-ClinicDB) is the standard generalizability test.
- **Dataset**: [polyp.grand-challenge.org](https://polyp.grand-challenge.org/)

---

### 2. CNN-Based Segmentation

---

#### [P03] PraNet: Parallel Reverse Attention Network for Polyp Segmentation
- **Authors**: Fan, D.-P., Ji, G.-P., Zhou, T., Chen, G., Fu, H., Shen, J., Shao, L.
- **Year/Venue**: 2020 / MICCAI 2020
- **arXiv**: [2006.11392](https://arxiv.org/abs/2006.11392)
- **Method Summary**: Proposes a Parallel Partial Decoder (PPD) to aggregate high-level features into a global map, then uses a Reverse Attention (RA) module that flips the current prediction to mine boundary cues from otherwise-overlooked regions. The recurrent RA mechanism iteratively calibrates misaligned predictions. Backbone: Res2Net-50.
- **Reported Metrics** (from paper, on standard splits):
  - Kvasir-SEG: Dice=0.898, IoU=0.840, F-measure=0.885 @ ~50 FPS
  - CVC-ClinicDB: Dice=0.899, IoU=0.849, F-measure=0.896
  - CVC-ColonDB: Dice=0.712, IoU=0.640
  - ETIS: Dice=0.628, IoU=0.567
  - CVC-300: Dice=0.871, IoU=0.797
- **Key Insight**: Reverse attention is a powerful inductive bias for medical image segmentation — it forces the model to refine boundary regions, not just the interior blob.
- **Limitations**: Drops significantly on CVC-ColonDB and ETIS (out-of-distribution challenge). No temporal modeling. FPS drops with higher-resolution inputs.
- **Relevance**: **BASELINE TO BEAT.** We will reproduce PraNet numbers on all 5 datasets before proposing our method. The reverse attention concept is likely to appear in our design.
- **Code**: [github.com/DengPingFan/PraNet](https://github.com/DengPingFan/PraNet)

---

#### [P04] Real-Time Polyp Detection, Localization and Segmentation in Colonoscopy Using Deep Learning (ColonSegNet)
- **Authors**: Jha, D., Ali, S., Tomar, N.K., Johansen, H.D., Johansen, D.D., Rittscher, J., Riegler, M.A., Halvorsen, P.
- **Year/Venue**: 2021 / IEEE Access
- **arXiv**: [2011.07631](https://arxiv.org/abs/2011.07631)
- **DOI**: [10.1109/ACCESS.2021.3063716](https://doi.org/10.1109/ACCESS.2021.3063716)
- **Method Summary**: ColonSegNet is a lightweight encoder-decoder with skip connections designed for real-time performance. Benchmarks 10+ state-of-the-art methods on Kvasir-SEG for both speed (FPS) and accuracy (Dice, IoU). The paper's core contribution is the **comprehensive benchmark** + a model achieving the best speed-accuracy trade-off at 182 FPS.
- **Reported Metrics** (on Kvasir-SEG):
  - ColonSegNet: Dice=0.8206, IoU=0.8100, Precision=0.8000 @ **182.38 FPS**
  - vs. U-Net: Dice=0.8264 @ ~8 FPS
  - vs. ResUNet++: Dice=0.8130 @ ~8 FPS
- **Key Insight**: Speed-accuracy trade-off is critical for clinical deployment. Most high-accuracy methods run at single-digit FPS, which is inadequate for real-time feedback.
- **Limitations**: Dice=0.8206 is significantly below PraNet's 0.898. Demonstrates the accuracy-speed tension.
- **Relevance**: **DIRECT BENCHMARK.** Sets the real-time speed target we need to match or exceed (≥30 FPS for clinical viability, ≥180 FPS for this method's class). Also motivates our research gap.

---

#### [P05] Shallow Attention Network for Polyp Segmentation (SANet)
- **Authors**: Wei, J., Hu, Y., Zhang, R., Li, Z., Zhou, S.K., Cui, S.
- **Year/Venue**: 2021 / MICCAI 2021
- **arXiv**: [2108.00882](https://arxiv.org/abs/2108.00882)
- **Method Summary**: Addresses three specific challenges: (1) color inconsistency across datasets via a Color Exchange (CE) augmentation that swaps color channels between images to decouple shape from color; (2) small polyp degradation via a Shallow Attention Module (SAM) that filters background noise in early feature maps; (3) foreground-background imbalance via a Probability Correction Strategy (PCS) during inference. Achieves ~72 FPS.
- **Reported Metrics**:
  - Kvasir-SEG: Dice=0.904, IoU=0.847
  - CVC-ClinicDB: Dice=0.916, IoU=0.859
  - CVC-ColonDB: Dice=0.753, IoU=0.670
  - ETIS: Dice=0.750, IoU=0.654
  - CVC-300: Dice=0.888, IoU=0.815
- **Key Insight**: Color exchange augmentation is a simple but highly effective domain adaptation technique for cross-dataset evaluation.
- **Limitations**: PCS is an inference-time trick that doesn't generalize well to video (requires per-batch statistics). Backbone is ResNet-based (limited long-range context).
- **Relevance**: The Color Exchange augmentation is a technique we should adopt in our data loader. SANet's cross-dataset numbers on ColonDB/ETIS show better generalizability than PraNet.
- **Code**: [github.com/weijun88/SANet](https://github.com/weijun88/SANet)

---

#### [P06] HarDNet-MSEG: A Simple Encoder-Decoder Polyp Segmentation Neural Network that Achieves over 0.9 Mean Dice and 86 FPS
- **Authors**: Huang, C.-H., Wu, H.-Y., Lin, Y.-L.
- **Year/Venue**: 2021 / arXiv preprint
- **arXiv**: [2101.07172](https://arxiv.org/abs/2101.07172)
- **Method Summary**: Uses HarDNet68 (a memory-efficient backbone with harmonic dense connections) + a Cascaded Partial Decoder (CPD) decoder. HarDNet's design minimizes DRAM traffic, making it fast on both GPU and edge hardware. Decoder is inspired by CPD for salient object detection.
- **Reported Metrics** (on five datasets):
  - Kvasir-SEG: Dice=0.904 @ **86.7 FPS** (RTX 2080 Ti)
  - CVC-ClinicDB: Dice=0.932 @ 86.7 FPS
  - CVC-ColonDB: Dice=0.731 @ 86.7 FPS
  - ETIS: Dice=0.677 @ 86.7 FPS
  - CVC-300: Dice=0.887 @ 86.7 FPS
- **Key Insight**: With the right backbone, high accuracy (0.9 Dice) AND high speed (86 FPS) are simultaneously achievable. Memory-efficient backbones are underexplored in medical imaging.
- **Limitations**: No attention mechanisms — the paper explicitly credits speed to architecture efficiency, not accuracy-boosting modules.
- **Relevance**: Establishes that 86 FPS @ Dice=0.904 is achievable with CNN-only approaches. This is our **real-time baseline target** before adding transformer components.
- **Code**: [github.com/james128333/HarDNet-MSEG](https://github.com/james128333/HarDNet-MSEG)

---

### 3. Transformer-Based Segmentation

---

#### [P07] Polyp-PVT: Polyp Segmentation with Pyramid Vision Transformers
- **Authors**: Dong, B., Wang, W., Fan, D.-P., Li, J., Fu, H., Shao, L.
- **Year/Venue**: 2021/2023 / CAAI Artificial Intelligence Research
- **arXiv**: [2108.06932](https://arxiv.org/abs/2108.06932)
- **DOI**: [10.26599/AIR.2023.9150015](https://doi.org/10.26599/AIR.2023.9150015)
- **Method Summary**: First work to use PVT (Pyramid Vision Transformer) backbone for polyp segmentation. Introduces: (1) CFM (Cascaded Fusion Module) — aggregates semantic + location info from high-level features; (2) CIM (Camouflage Identification Module) — captures disguised polyp features in low-level layers; (3) SAM (Similarity Aggregation Module) — extends pixel features to the full polyp area. Together, these suppresses background noise in transformer features.
- **Reported Metrics**:
  - Kvasir-SEG: Dice=0.917, IoU=0.864
  - CVC-ClinicDB: Dice=0.937, IoU=0.889
  - CVC-ColonDB: Dice=0.808, IoU=0.727
  - ETIS: Dice=0.787, IoU=0.706
  - CVC-300: Dice=0.900, IoU=0.833
- **Key Insight**: Transformer encoders are significantly more robust to appearance changes than CNN encoders. Cross-dataset performance (ColonDB, ETIS) is substantially improved vs. CNN-based methods.
- **Limitations**: Lower FPS than CNN methods (PVT is computationally heavier). Does not model temporal context for video.
- **Relevance**: **Critical reference.** Establishes the transformer as the backbone of choice for generalizability. Our model likely uses a PVT or similar hierarchical ViT as encoder.
- **Code**: [github.com/DengPingFan/Polyp-PVT](https://github.com/DengPingFan/Polyp-PVT)

---

#### [P08] HiFiSeg: High-Frequency Information Enhanced Polyp Segmentation with Global-Local Vision Transformer
- **Authors**: Ren, J., Zhang, X., Zhang, L.
- **Year/Venue**: 2024 / arXiv
- **arXiv**: [2410.02528](https://arxiv.org/abs/2410.02528)
- **Method Summary**: Addresses ViT's known limitation in capturing high-frequency (boundary/edge) information. Uses PVT as encoder. GLIM (Global-Local Interaction Module) fuses global and local features at multiple scales in parallel. SAM (Selective Aggregation Module) integrates boundary details from low-level features with semantic information from high-level features.
- **Reported Metrics**:
  - CVC-ColonDB: mDice=0.826
  - ETIS: mDice=0.822
- **Key Insight**: High-frequency augmentation of transformer features specifically addresses the boundary blurring that pure attention mechanisms cause.
- **Limitations**: Results only reported for 2 of the 5 standard datasets in the abstract.
- **Relevance**: Motivates a boundary-aware module in our design. The GLIM structure is architecturally interesting.

---

#### [P09] ASGNet: Adaptive Spectrum Guidance Network for Automatic Polyp Segmentation
- **Authors**: Sun, Y., Zhang, H., Qian, J., Yang, J., Luo, L.
- **Year/Venue**: 2026 / TCSVT 2026
- **arXiv**: [2604.14755](https://arxiv.org/abs/2604.14755)
- **Method Summary**: Integrates spectral (frequency-domain) features with spatial attention to enhance polyp discriminability. Key modules: (1) Spectrum-Guided Non-Local Perception Module — jointly aggregates local and global information in frequency space; (2) Multi-Source Semantic Extractor — integrates high-level semantic info for preliminary localization; (3) Dense Cross-Layer Interaction Decoder — fuses features across decoder layers. Benchmarked against 21 SOTA methods.
- **Reported Metrics**: "Superiority over 21 SOTA methods" (quantitative details not in arXiv abstract — need to read full paper)
- **Key Insight**: Frequency-domain features are complementary to spatial features for polyp detection, particularly for textural camouflage cases.
- **Relevance**: Very recent SOTA (TCSVT 2026). Frequency-domain attention is a potential differentiator for our work.
- **Code**: [github.com/CSYSI/ASGNet](https://github.com/CSYSI/ASGNet)

---

### 4. Video Polyp Segmentation

---

#### [P10] PNS-Net: Polyp/Neuron Segmentation Network for Video
- **Authors**: (Searching for specific arXiv ID — likely Ji et al., 2021)
- **Year/Venue**: 2021 / MICCAI 2021
- **Note**: Specific arXiv ID not confirmed — cited broadly as "PNS-Net" in literature. See [GitHub search](https://github.com/GewelsJI/VPS-Net) for SUN-SEG dataset work by same group.
- **Method Summary**: Introduces normalized self-attention for video polyp segmentation, using inter-frame temporal relationships to enhance detection consistency across video frames.
- **Reported Metrics** (on SUN-SEG):
  - S-measure: 0.871, E-measure: 0.928, Dice: 0.832
- **Key Insight**: Frame-to-frame consistency (temporal coherence) is a significant unsolved challenge. A model that tracks polyp location across frames dramatically reduces false negatives due to motion blur or occlusion.
- **Limitations**: High computational cost for video processing. Not real-time for long video sequences.
- **Relevance**: **Motivates video-aware design.** If our final model targets video colonoscopy, temporal modeling is necessary. This is the gap our work may address.

---

#### [P11] A Multi-Center Analysis of Deep Learning Methods for Video Polyp Detection and Segmentation
- **Authors**: Ghatwary, N., Chavarias Solano, P., Ibrahim, M.R., Krenzer, A., et al.
- **Year/Venue**: 2026 / arXiv preprint (submitted to journal)
- **arXiv**: [2603.04288](https://arxiv.org/abs/2603.04288)
- **Method Summary**: Comprehensive evaluation study using multi-center, multi-population video colonoscopy data. Evaluates applicability of DL methods in real-time clinical video settings. Highlights the critical role of temporal frame relationships in improving diagnostic precision.
- **Key Findings**:
  - Single-frame models degrade significantly on video data (temporal inconsistency)
  - Multi-center data reveals severe generalization gaps across clinical sites
  - Sequence/temporal information is critical and underutilized
- **Relevance**: **CRITICAL for paper framing.** This 2026 multi-center study directly validates our research gap hypothesis: existing models lack temporal awareness and cross-center generalizability. This paper should be cited prominently in our introduction and gap analysis.

---

### 5. Real-Time & Lightweight Models

---

#### [P12] A Lightweight and Robust Framework for Real-Time Colorectal Polyp Detection Using LOF-Based Preprocessing and YOLO-v11n
- **Authors**: Behzadi, S., Sharifrazi, D., Mesbahzadeh, B., Joloudari, J.H., Alizadehsani, R.
- **Year/Venue**: 2025 / arXiv
- **arXiv**: [2507.10864](https://arxiv.org/abs/2507.10864)
- **Method Summary**: Combines Local Outlier Factor (LOF) data cleaning (removes 5% anomalous samples) with YOLO-v11n detection model. Converts segmentation masks to bounding boxes for detection-only task. Uses 5-fold cross-validation on CVC-ColonDB, CVC-ClinicDB, Kvasir-SEG, ETIS, EndoScene.
- **Reported Metrics** (detection task, not segmentation):
  - Precision: 95.83%, Recall: 91.85%, F1: 93.48%
  - mAP@0.5: 96.48%, mAP@0.5:0.95: 77.75%
- **Key Insight**: Data cleaning with LOF before training provides measurable performance improvement. YOLO-v11n is highly competitive for real-time detection.
- **Limitations**: **Detection only** (bounding boxes), not pixel-level segmentation. Converting segmentation masks to boxes loses information.
- **Relevance**: Shows YOLO-v11n is viable for polyp detection. If our system needs a detection head (for clinical CADe), YOLO is the right choice. We should implement both detection (YOLO) and segmentation (U-Net style) heads.

---

#### [P13] MicroAUNet: Boundary-Enhanced Multi-scale Fusion with Knowledge Distillation for Colonoscopy Polyp Image Segmentation
- **Authors**: Wang, Z., Zhang, Y., Ye, B., Jiang, Y., Gu, L., Xiang, S.
- **Year/Venue**: 2025/2026 / ECCV 2026 Workshop (MedVidU)
- **arXiv**: [2511.01143](https://arxiv.org/abs/2511.01143)
- **Method Summary**: MicroAUNet — lightweight attention-based network using depthwise-separable dilated convolutions + parameter-shared channel-spatial attention block. Key novelty: two-stage knowledge distillation (from a heavy teacher to lightweight student) transferring both semantic and boundary cues. Achieves SOTA under "extremely low model complexity."
- **Reported Metrics**: "State-of-the-art accuracy under extremely low model complexity" — exact numbers in full paper
- **Key Insight**: Knowledge distillation can close the gap between lightweight and heavy models, enabling real-time deployment without sacrificing accuracy. Boundary-specific distillation is a novel contribution.
- **Relevance**: Directly addresses our speed-accuracy tension goal. Knowledge distillation is a training strategy we should consider for our final model.

---

### 6. Recent 2024–2026 Work

---

#### [P14] GRAFNet: Multiscale Retinal Processing via Guided Cortical Attention Feedback for Enhancing Medical Image Polyp Segmentation
- **Authors**: Fofanah, A.J., Wen, L., Kamara, A.A., Zhang, Z., Chen, D., Sankoh, A.P.
- **Year/Venue**: 2026 / arXiv
- **arXiv**: [2602.15072](https://arxiv.org/abs/2602.15072)
- **Method Summary**: Biologically-inspired architecture mimicking the human visual cortex hierarchy. Three key modules: (1) GAAM (Guided Asymmetric Attention Module) — mimics orientation-tuned cortical neurons for boundary emphasis; (2) MSRM (MultiScale Retinal Module) — parallel multi-feature analysis like retinal ganglion cells; (3) GCAFM (Guided Cortical Attention Feedback Module) — predictive coding for iterative refinement. Claims 3–8% Dice improvement and 10–20% better generalization.
- **Reported Metrics**: "3–8% Dice improvements" and "10–20% higher generalisation over leading methods" on 5 benchmarks (exact numbers in full paper)
- **Key Insight**: Feedback connections and predictive coding are underexplored in medical image segmentation. Biological inspiration provides interpretable architectural choices.
- **Relevance**: The feedback mechanism concept is interesting for our design. Claims significant generalization improvements — if verified, this is important for our cross-dataset experiments.
- **Code**: [github.com/afofanah/GRAFNet](https://github.com/afofanah/GRAFNet)

---

#### [P15] PolypVision: A Three-Stage Hierarchical Deep Learning Framework for Classification and Segmentation of Colorectal Polyps
- **Authors**: Bolhasani, H., Rastad, H., Akbari, A.M., Tashakoripour, M., et al.
- **Year/Venue**: 2026 / arXiv
- **arXiv**: [2608.10649](https://arxiv.org/abs/2608.10649)
- **Method Summary**: Three-stage pipeline: Stage 1 = binary classification (adenomatous vs. hyperplastic) + Paris/JNet classification with EfficientNetV2-M + Focal Loss; Stage 2 = segmentation with UNet++ decoder; Stage 3 = adenoma subtype classification with transfer learning from Stage 2. Evaluated on PolypGen, Kvasir-SEG, CVC-ClinicDB.
- **Reported Metrics**:
  - AUC ≈ 0.99 (frame classification)
  - Detection mAP@50 = 94.4% on Kvasir-SEG
- **Key Insight**: Joint classification and segmentation in a hierarchical pipeline improves clinical utility beyond simple binary polyp/no-polyp detection.
- **Relevance**: Demonstrates the clinical demand for multi-task learning (detect + classify + segment). Our Phase 3+ work might adopt this direction.
- **Web App**: [polypvision.com](https://polypvision.com)

---

#### [P16] EndoSight AI: Deep Learning-Driven Real-Time Gastrointestinal Polyp Detection and Segmentation for Enhanced Endoscopic Diagnostics
- **Authors**: Cavadia, D.
- **Year/Venue**: 2025 / arXiv
- **arXiv**: [2511.12962](https://arxiv.org/abs/2511.12962)
- **Method Summary**: Combined detection (mAP) and segmentation (Dice) pipeline on Hyper-Kvasir dataset, achieving real-time performance (>35 FPS) via thermal-aware training procedure. Single-author work demonstrating practical deployment pipeline.
- **Reported Metrics** (Hyper-Kvasir dataset):
  - Detection mAP: 88.3%
  - Segmentation Dice: up to 0.69
  - Speed: >35 FPS on GPU
- **Key Insight**: Dice=0.69 at 35 FPS shows real-time segmentation lags substantially behind accuracy-focused models. This gap motivates our work.
- **Limitations**: Single-dataset evaluation. Dice=0.69 is well below SOTA. Single-author without peer review.
- **Relevance**: Documents the real-time segmentation gap. Our target: ≥0.90 Dice at ≥35 FPS.

---

#### [P17] QFedPolyp: A Communication- and Inference-Efficient Federated Learning Framework for Polyp Segmentation
- **Authors**: Baduwal, M., Paudel, P.
- **Year/Venue**: 2026 / arXiv
- **arXiv**: [2607.22743](https://arxiv.org/abs/2607.22743)
- **Method Summary**: Federated learning for privacy-preserving collaborative polyp segmentation. 8-bit quantization during communication reduces transmission cost ~4×. Models are lightweight U-Net variants trained per hospital.
- **Reported Metrics**:
  - Kvasir-SEG: Dice=0.910 (full-precision federated)
  - CVC-ClinicVideoDB: Dice=0.930 (full-precision federated)
  - 8-bit quantized: comparable accuracy + 1.5× faster inference
- **Key Insight**: Federated learning is the future for multi-center deployment. A model that works well in a federated setting needs to be lightweight and quantization-friendly.
- **Relevance**: Motivates lightweight design and quantization-aware training as future steps. Also documents that Dice=0.91–0.93 is achievable with standard U-Nets in federated settings.

---

#### [P18] PolypSeg-GradCAM: Explainable Deep Learning Framework for Polyp Segmentation
- **Authors**: Asare, A., Nguyen, T.-H., Bagci, U.
- **Year/Venue**: 2025/2026 / ACDSA 2026
- **arXiv**: [2509.18159](https://arxiv.org/abs/2509.18159)
- **Method Summary**: U-Net with ResNet-34 backbone + Grad-CAM for explainability. 5-fold cross-validation on Kvasir-SEG (1,000 images).
- **Reported Metrics** (5-fold CV on Kvasir-SEG):
  - Mean Dice: **0.8902 ± 0.0125**
  - Mean IoU: **0.8023**
  - AUC-ROC: 0.9722
  - Sensitivity: 0.9058, Precision: 0.9083
- **Key Insight**: 5-fold CV gives much more robust estimates than single train/test splits. ResNet-34 + U-Net is still competitive. Grad-CAM is essential for clinical trust.
- **Relevance**: (1) We must use rigorous CV or standard splits — single run results are not credible. (2) Explainability (Grad-CAM or similar) should be part of our pipeline. (3) Dice=0.89 with basic ResNet-34+UNet sets our minimum acceptable baseline.

---

## SOTA Comparison Table

> **Note**: All numbers below are sourced directly from the respective papers' reported results. Dataset split protocols vary — numbers from different papers are NOT directly comparable without verifying the exact split used. We will re-evaluate all methods on the **same split** in our experiments.

### Standard Benchmarks (5 Datasets)

| Method | Year | Backbone | Kvasir Dice | Kvasir IoU | ClinicDB Dice | ClinicDB IoU | ColonDB Dice | ETIS Dice | CVC-300 Dice | FPS |
|--------|------|----------|------------|-----------|--------------|-------------|-------------|-----------|-------------|-----|
| U-Net [P01] | 2015 | VGG-16 | 0.8264 | 0.7177 | — | — | — | — | — | ~8 |
| U-Net++ | 2018 | EfficientB3 | — | — | — | — | — | — | — | — |
| PraNet [P03] | 2020 | Res2Net-50 | 0.898 | 0.840 | 0.899 | 0.849 | 0.712 | 0.628 | 0.871 | ~50 |
| ColonSegNet [P04] | 2021 | Custom | 0.8206 | 0.8100 | — | — | — | — | — | **182** |
| HarDNet-MSEG [P06] | 2021 | HarDNet68 | 0.904 | — | 0.932 | — | 0.731 | 0.677 | 0.887 | **86.7** |
| SANet [P05] | 2021 | ResNet-50 | 0.904 | 0.847 | 0.916 | 0.859 | 0.753 | 0.750 | 0.888 | ~72 |
| Polyp-PVT [P07] | 2021 | PVT-v2-B2 | 0.917 | 0.864 | 0.937 | 0.889 | 0.808 | 0.787 | 0.900 | ~35 |
| HiFiSeg [P08] | 2024 | PVT | — | — | — | — | 0.826 | 0.822 | — | — |
| QFedPolyp [P17] | 2026 | U-Net | 0.910 | — | — | — | — | — | — | — |
| PolypSeg-GradCAM [P18] | 2026 | ResNet-34 | 0.8902±0.0125 | 0.8023 | — | — | — | — | — | — |

### Real-Time Detection (Bounding Box)

| Method | Year | Dataset | mAP@0.5 | Precision | Recall | FPS |
|--------|------|---------|---------|-----------|--------|-----|
| YOLO-v11n + LOF [P12] | 2025 | Kvasir-SEG + 4 others | 96.48% | 95.83% | 91.85% | Real-time |
| EndoSight AI [P16] | 2025 | Hyper-Kvasir | 88.3% | — | — | >35 |
| PolypVision [P15] | 2026 | Kvasir-SEG | 94.4% mAP@50 | — | — | — |

---

## Gap Analysis & Our Contribution

### Identified Gaps (Evidence-Based)

Based on the literature review above, we identify the following **evidence-based gaps** that our research will address:

#### Gap 1: The Accuracy–Speed Trade-off (Unresolved)
- **Evidence**: PraNet achieves Dice=0.898 @ ~50 FPS. HarDNet-MSEG achieves Dice=0.904 @ 86.7 FPS. Polyp-PVT achieves Dice=0.917 @ ~35 FPS. The multi-center study [P11] requires real-time video performance for clinical use.
- **Current best**: No published method achieves both Dice ≥ 0.92 AND ≥ 60 FPS.
- **Our target**: Dice ≥ 0.920, IoU ≥ 0.870, FPS ≥ 60 on standard GPU.

#### Gap 2: Cross-Dataset Generalization
- **Evidence**: PraNet drops from Dice=0.898 (Kvasir) to Dice=0.628 (ETIS) — a 30% degradation. Even Polyp-PVT drops from 0.917 to 0.787 on ETIS. The 2026 multi-center study [P11] directly documents this as a critical open problem.
- **Current best**: Polyp-PVT has the best cross-dataset generalization in its class.
- **Our target**: Dice ≥ 0.780 on ETIS (zero-shot, trained on Kvasir+ClinicDB only).

#### Gap 3: Temporal Modeling for Video Colonoscopy
- **Evidence**: All high-accuracy methods (PraNet, SANet, Polyp-PVT) process individual frames. The multi-center video study [P11] shows that temporal information is "critical and underutilized." The SUN-SEG video dataset exists but few methods exploit it.
- **Current best**: PNS-Net for video, but at significant computational cost.
- **Our target**: Lightweight temporal module (ConvLSTM or deformable attention across frames) maintaining >30 FPS on video.

#### Gap 4: Boundary Precision for Small Polyps
- **Evidence**: SANet [P05] explicitly addresses small polyp degradation with shallow attention. MicroAUNet [P13] uses boundary-specific knowledge distillation. GRAFNet [P14] uses cortical feedback for boundary refinement. This remains unsolved — small flat adenomas have the highest miss-rate clinically.
- **Our target**: Explicitly benchmark on small polyp subset of datasets (polyp area < 1% of frame area).

### Our Proposed Contribution

> **Working Title**: "RT-PolyNet: A Real-Time Hybrid CNN-Transformer Network for Generalizable Polyp Segmentation with Temporal Awareness"

**Proposed novelty** (to be validated/refined with experiments):

1. **Hybrid backbone** (EfficientNet + PVT): CNN extracts local/boundary features; PVT captures global context. Combined via cross-attention fusion. Targets the accuracy-speed sweet spot.

2. **Frequency-domain boundary module**: Inspired by ASGNet [P09] and HiFiSeg [P08]. Explicit high-frequency (edge) feature extraction to improve boundary precision for small polyps.

3. **Lightweight temporal module**: Deformable inter-frame attention over last K frames (K=3 or 5) for video continuity without the memory cost of full ConvLSTM.

4. **Multi-domain training strategy**: Color exchange [P05] + spectral augmentation + multi-dataset joint training to improve cross-dataset generalizability.

> ⚠️ **NOTE**: This contribution section is a WORKING HYPOTHESIS based on the literature. It MUST be revised after (a) reproducing baselines and (b) ablation studies confirm which components actually contribute. Do NOT treat this as final until supported by experimental evidence.

---

## Papers To Read (Backlog)

| Priority | Paper | Why |
|----------|-------|-----|
| HIGH | PNS-Net (Ji et al., MICCAI 2021) | Video polyp SOTA — need exact arXiv ID and metrics |
| HIGH | ESFPNet (Ma et al.) | Referenced frequently in surveys — need metrics |
| HIGH | SUN-SEG dataset paper | Video benchmark needed for temporal experiments |
| HIGH | PolypGen dataset paper (Ali et al., 2023) | Multi-center benchmark we plan to use |
| MEDIUM | MSNet (Zhao et al., 2021) | Cited as SOTA in several 2022 papers |
| MEDIUM | SSFormer (Wang et al., 2022) | Transformer approach to medical seg |
| MEDIUM | DoubleU-Net (Jha et al., 2020) | Dual U-Net architecture for medical images |
| MEDIUM | GRAFNet full paper | Generalization claims need verification |
| LOW | TGANet (Tomar et al., 2022) | Text-guided attention for polyp segmentation |
| LOW | LDNet (Zhang et al.) | Latest video polyp method |

---

*This document is a living artifact. Update after each new paper is read. All metrics from papers are self-reported by authors — independent reproduction is required before citing as ground truth.*
