# ChakraModel Pro — Daily Research Digest
**Date**: Thursday, September 17, 2026  
**Focus Area**: Colorectal Polyp Detection (CADe) & Pixel-Level Segmentation (CADx)  
**Project Phase**: Transitioning from Phase 1 (Data Prep & Weight Forensics) into Phase 2 (Baseline Verification & Zero-Shot Benchmark Replication)  
**Protocol Compliance**: Strict alignment with [`.antigravityrules.md`](file:///M:/chakramodelpro/polyp-detection-research/.antigravityrules.md) (Zero fabrication, raw proof, context discipline, phase gating).

---

## 1. Executive Summary & Daily Progress Snapshot

The mission of **ChakraModel Pro** is to engineer a clinically viable, real-time deep learning architecture for colonoscopy polyp detection and segmentation that closes the critical 22–28% adenoma miss rate while overcoming the two persistent failure modes of current academic SOTA:
1. **Catastrophic Out-of-Distribution (OOD) Generalization Drop**: Standard models trained on Kvasir-SEG lose 25–30% Dice when evaluated zero-shot on ETIS-Larib or CVC-ColonDB.
2. **The Accuracy vs. Latency Paradox**: Existing heavy Vision Transformers achieve high still-frame Dice ($\ge 0.92$) but stall at 10–15 FPS on clinical workstations, failing the $\ge 30\text{ FPS}$ real-time video threshold.

```
+----------------------------------------------------------------------------------------------------+
|                                      CHAKRAMODEL PRO ROADMAP                                       |
+----------------------------------------------------------------------------------------------------+
| [Phase 0] Lit Review (58 Papers)   --> [Phase 1] Kvasir-SEG (900/100 Split) & Weight Forensics     |
| [Phase 2] CURRENT: Baseline Models --> [Phase 3] Chakra-v2 Hybrid Architecture                     |
| [Phase 4] Temporal Video Head      --> [Phase 5] Multi-Center OOD Benchmark & Clinical Translation |
+----------------------------------------------------------------------------------------------------+
```

### Current Workspace Asset Audit
- **Dataset**: `Kvasir-SEG` (1,000 images, 900 train / 100 test split verified at [`data/processed/train.txt`](file:///M:/chakramodelpro/polyp-detection-research/data/processed/train.txt) and [`data/processed/test_splits/kvasir_test.txt`](file:///M:/chakramodelpro/polyp-detection-research/data/processed/test_splits/kvasir_test.txt)).
- **Existing Weights**:
  - `combo1_best.pth` (102.7 MB): Verified PraNet architecture (`Res2Net-50` backbone + 4 RFB modules + PPD + 4-stage Reverse Attention heads `ra1..ra4`).
  - `chakra_transformer_best.pth` (1.24 GB): Verified `ViT-Large` / Segmenter architecture (24 Transformer blocks + `patch_embed` + multi-scale `decode_head`).
- **Pending Implementation**: `src/models/pranet.py` and `src/models/transformer_segmenter.py` to bridge these weights into the executable [`src/eval.py`](file:///M:/chakramodelpro/polyp-detection-research/src/eval.py) runner.

---

## 2. 2025–2026 Frontier Literature & SOTA Intelligence

In accordance with **Rule 3 (Context Discipline)**, we analyze the frontier literature through 4 focused technological paradigms directly applicable to the ChakraModel design.

### Paradigm A: State Space Models (Mamba / SSMs) — Breaking Quadratic Complexity
Transformers suffer from $\mathcal{O}(N^2)$ computational complexity with respect to token count, limiting high-resolution feature maps ($352 \times 352$ or $512 \times 512$). State Space Models (SSMs) provide continuous-time memory modeling with linear $\mathcal{O}(N)$ complexity.

1. **Polyp-Mamba ([P24], MICCAI 2024 / LNCS)**:
   - *Innovation*: Dual-path State Space block (SSB) performing multi-directional spatial scanning across 4 cardinal/diagonal paths.
   - *Verified Metrics*: **mDice = 0.935** on Kvasir-SEG, **0.812** on ETIS-Larib, **89.00%** 5-dataset average at **48 FPS** on RTX 3090.
   - *Limitation*: Standard 1D serialization disrupts fine boundary topology.
2. **CSG-Mamba (2026)**:
   - *Innovation*: Introduces **Convolutional Scoring Gating (CSG)** to augment the selective scan mechanism. By computing a local spatial density score via lightweight depthwise convolutions prior to state update, CSG restores high-frequency boundary continuity lost during 1D token unwrapping.
3. **PolyMamba-Net (2025/2026)**:
   - *Innovation*: Hybrid CNN-Mamba pipeline tailored for high-speed endoscopy video. Offloads early feature extraction to inverted residual mobile stages and restricts Mamba blocks to the deep bottleneck.
   - *Throughput*: Achieves **>115 FPS** with Dice $>0.92$, demonstrating that SSMs can comfortably exceed real-time clinical requirements.
4. **UltraLight VM-UNet ([P25], 2024)**:
   - *Extreme Edge Footprint*: Only **0.049M parameters** and **0.06 GFLOPs**, clocking $>120\text{ FPS}$ while reaching 0.908 mDice on Kvasir-SEG.

### Paradigm B: Foundation Model Adaptation (SAM 2 & DINOv2)
Foundation models trained on billions of natural masks offer rich semantic priors, but exhibit severe domain failure on endoscopic mucosal glare and fluid artifacts.

1. **ASAM2-UNet & SAM 2 Colon Adapters (2026)**:
   - *Mechanism*: Adapts Meta's **SAM 2** streaming memory architecture for colonoscopy. The recurrent memory bank caches polyp feature tokens across temporal frames, enabling prompt-free tracking through video sequences.
   - *Clinical Impact*: Resolves flickering detections and false alarms caused by peristaltic contractions.
2. **Lite-PolypInductor & DINOv2 Feature Induction (2026)**:
   - *Mechanism*: Uses frozen DINOv2 attention "keys" as distillation teachers for compact CNN encoders.
   - *Key Advantage*: Improves cross-center generalizability on out-of-distribution endoscopic hardware (e.g., Olympus vs. Pentax vs. Fujifilm) without needing large labeled multi-center datasets.

### Paradigm C: Boundary-Aware Diffusion & High-Frequency Decoders
1. **Diff-Polyp ([P57], 2024) & InstEditSeg (2026)**:
   - *Problem Addressed*: Diminutive, flat, and sessile serrated lesions (Paris classification IIb/IIc) that blend seamlessly into healthy mucosa.
   - *Mechanism*: Formulates boundary extraction as a conditional diffusion reverse process, iteratively sharpening uncertain pixel distributions at lesion perimeters.
2. **HiFiSeg ([P08]) & ASGNet ([P09])**:
   - *Spectral Priors*: Employs 2D Fast Fourier Transforms (FFT) to decompose feature maps into high-frequency (boundary transitions) and low-frequency (semantic body) components, preventing boundary hallucination.

### Paradigm D: Video Temporal Continuity & Commercial Translation
Reviewing commercial CADe systems (Medtronic GI Genius, Iterative Health SKOUT, Olympus ENDO-AID from [`docs/industry_trends.md`](file:///M:/chakramodelpro/polyp-detection-research/docs/industry_trends.md)):
- **Alarm Fatigue**: Single-frame false positives cause endoscopists to disable CAD systems. Commercial systems enforce temporal hysteresis: a detection must persist across $\ge 3\text{--}5$ consecutive frames before triggering a visual bounding box.
- **Academic Video Benchmarks**: PNS-Net ([P10]) and SUN-SEG ([P33]) show that integrating temporal difference blocks increases video Dice from 0.72 to 0.83 on sequences containing rapid scope motion.

---

## 3. Grounded SOTA Performance Benchmark Matrix

> **Rule 2 Audit**: All values in this table represent peer-reviewed published metrics extracted from verified literature documents ([`docs/literature_review.md`](file:///M:/chakramodelpro/polyp-detection-research/docs/literature_review.md)). Zero simulated or fabricated figures.

| Model | Venue / Year | Backbone | Kvasir-SEG (mDice) | CVC-ClinicDB (mDice) | CVC-ColonDB (mDice) | ETIS-Larib (mDice) | CVC-300 (mDice) | Speed (FPS) | Params (M) |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **U-Net** | MICCAI '15 | Standard Conv | 0.818 | 0.823 | 0.512 | 0.398 | 0.710 | ~35 | 31.0 |
| **ResUNet++** | ISM '19 | ResNet-50 | 0.813 | 0.796 | - | - | - | 42 | 4.8 |
| **PraNet ([P03])** | MICCAI '20 | Res2Net-50 | 0.898 | 0.899 | 0.712 | 0.628 | 0.871 | ~50 | 32.5 |
| **ColonSegNet ([P04])** | IEEE Access '21| Custom CNN | 0.821 | 0.810 | - | - | - | **182** | **5.0** |
| **SANet ([P05])** | MICCAI '21 | Res2Net-50 | 0.904 | 0.916 | 0.753 | 0.750 | 0.888 | ~72 | 24.7 |
| **HarDNet-MSEG ([P06])**| BMVC '21 | HarDNet-68 | 0.904 | 0.887 | 0.731 | 0.677 | 0.876 | 86.7 | 33.3 |
| **Polyp-PVT ([P07])** | arXiv '21 | PVT-v2-B2 | 0.917 | 0.937 | 0.808 | 0.787 | 0.900 | ~35 | 25.4 |
| **ColonFormer ([P20])**| JBHI '23 | MiT-B3 | 0.922 | 0.932 | 0.809 | 0.782 | 0.898 | 42 | 48.0 |
| **Polyp-Mamba ([P24])**| MICCAI '24 | Dual-path SSM | **0.935** | **0.948** | **0.834** | **0.812** | **0.921** | ~48 | 31.4 |
| **UltraLight VM-UNet ([P25])**| arXiv '24 | Parallel Mamba| 0.908 | 0.914 | - | <0.700 | - | **>120** | **0.049** |

---

## 4. The ChakraModel Architectural Blueprint: Chakra-v2

### Structural Synthesis of Existing Weights
Our repository contains two pre-existing checkpoints under `_weights_check/weights/checkpoints/`:
1. **`combo1_best.pth` (102.7 MB)**:
   - Encodes a spatial boundary-refining PraNet architecture.
   - Backbone: `Res2Net-50` with Receptive Field Blocks (`rfb1..4`) capturing multi-scale context without resolution loss.
   - Decoder: Parallel Partial Decoder (`ppd`) for initial coarse saliency, followed by 4 cascaded Reverse Attention (`ra1..ra4`) heads that invert predictions to actively mine perimeter regions.
2. **`chakra_transformer_best.pth` (1.24 GB)**:
   - Encodes a heavyweight `ViT-Large` representation with 24 multi-head self-attention transformer blocks.
   - Exceptional global receptive field and semantic discrimination, but prohibitive compute cost (estimated <12 FPS on edge GPUs).

### The Proposed Chakra-v2 Hybrid Architecture
Rather than deploying either model in isolation, Chakra-v2 synthesizes the advantages of both:

```
[Input Frame: 352x352x3]
         |
         v
+-------------------------------------------------------------+
| STAGE 1: Dual-Path Hybrid Encoder                           |
|  ├─ Fast Spatial Stream (Res2Net / Inverted Residuals)      |
|  │    --> Preserves sharp boundary edges, polyp crypts      |
|  └─ Semantic Stream (MiT-B2 / Selective Mamba Block)        |
|       --> Linear-complexity global contextual reasoning     |
+-------------------------------------------------------------+
         |
         v
+-------------------------------------------------------------+
| STAGE 2: High-Frequency Boundary Gating (HiFi / CSG Block)  |
|  ├─ 2D FFT / Depthwise Conv extracts mucosal boundary cues   |
|  └─ Gated fusion suppresses specular endoscopic reflections |
+-------------------------------------------------------------+
         |
         v
+-------------------------------------------------------------+
| STAGE 3: Cascaded Reverse Attention Decoder (from combo1)   |
|  ├─ Coarse Global Saliency Map                              |
|  └─ Iterative RA mining: RA4 -> RA3 -> RA2 -> Final Mask    |
+-------------------------------------------------------------+
         |
         v
[Output: 352x352 Binary Mask @ >= 60 FPS]
```

---

## 5. Phase 2 Immediate Implementation Action Plan

To comply with **Phase Gating (Rule 4)** and **Self-Audit (Rule 6)**, the following sequence must be executed systematically:

| Task ID | Component | Action Required | Status | Target Date |
| :--- | :--- | :--- | :--- | :--- |
| **P2-T1** | `src/models/pranet.py` | Implement PraNet architecture matching `combo1_best.pth` layer keys | **QUEUED** | 2026-09-17 |
| **P2-T2** | Baseline Eval Runner | Run zero-shot validation of `combo1_best.pth` on `kvasir_test.txt` via `src/eval.py` | **QUEUED** | 2026-09-17 |
| **P2-T3** | Real Metric Audit | Log actual computed Dice, IoU, and FPS from `results/metrics/baseline_combo1.json` | **NOT YET RUN** | 2026-09-17 |
| **P2-T4** | `src/models/chakra_vit.py` | Implement ViT architecture loader matching `chakra_transformer_best.pth` | **PENDING P2-T2** | 2026-09-18 |
| **P2-T5** | Chakra-v2 Hybrid Spec | Finalize layer dimensions and forward graph in `docs/architecture_notes.md` | **PENDING P2-T3** | 2026-09-18 |

---
*Digest compiled and verified against project rules on 2026-09-17.*
