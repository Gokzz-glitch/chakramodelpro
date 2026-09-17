# Daily Log — Polyp Detection Research

> **Format**: Append-only. Never edit past entries.  
> **Purpose**: Paper reproducibility section, personal tracking, decision audit trail.

---

## 2026-09-12 — Session 1: Project Initialization & Phase 0 Literature Review

**Date**: Saturday, 2026-09-12  
**Time**: ~20:30 IST  
**Session Duration**: ~2 hours

---

### What Was Done

1. **Project scaffolded** — Created the following structure:
   - `polyp-detection-research/` with all required directories
   - `.gitignore` (excludes: checkpoints, raw data, __pycache__, .env, wandb)
   - `README.md` — project overview with phases, datasets table, strict rules
   - `docs/literature_review.md` — Phase 0 complete first pass (18 papers)
   - `docs/daily_log.md` — this file
   - `docs/architecture_notes.md` — skeleton with Phase 1 reasoning
   - `docs/experiment_log.md` — template for all training runs
   - `data/README.md` — download instructions for 7 datasets
   - `requirements.txt` — pinned dependencies
   - `src/train.py`, `src/eval.py` — entry points (stubs, Phase 1+)
   - `src/models/`, `src/data_loaders/`, `src/utils/`, `configs/` — directory stubs
   - `results/metrics/`, `results/plots/`, `results/sample_predictions/` — output dirs

2. **Git initialized** — `main` branch created. First commit pending approval.

3. **Literature Review — Phase 0 COMPLETE (first pass)**:
   - Searched arXiv with queries: polyp segmentation deep learning, YOLO medical real-time, Polyp-PVT, ColonSegNet, SANet, video polyp
   - Fetched and read abstracts/descriptions for 18 papers
   - All papers sourced from real arXiv pages (verified URLs and arXiv IDs)
   - Populated `docs/literature_review.md` with method summaries, real reported metrics, key insights, limitations, and relevance notes

---

### Results / Findings

**Papers found and documented**: 18 (verified arXiv IDs or DOIs)

**Key SOTA metrics established** (from papers, NOT our experiments):

| Method | Kvasir Dice | ETIS Dice | FPS |
|--------|------------|-----------|-----|
| PraNet (2020) | 0.898 | 0.628 | ~50 |
| HarDNet-MSEG (2021) | 0.904 | 0.677 | 86.7 |
| SANet (2021) | 0.904 | 0.750 | ~72 |
| Polyp-PVT (2021) | 0.917 | 0.787 | ~35 |

**Gaps identified** (evidence-based):
1. No method simultaneously achieves Dice ≥ 0.92 AND ≥ 60 FPS
2. Severe cross-dataset drop (PraNet: Kvasir 0.898 → ETIS 0.628 = -29%)
3. No standard high-accuracy method models temporal video information
4. Small/flat polyp detection remains unsolved

**Working contribution hypothesis**:
- Hybrid CNN+Transformer encoder (EfficientNet + PVT)
- Frequency-domain boundary module
- Lightweight temporal inter-frame attention
- Multi-domain training (Color Exchange + spectral aug)

---

### Blockers

- None for Phase 0 (literature review)
- **Phase 1 blocker identified**: Need dataset download links confirmed and directory `data/raw/` populated before any code can run. See `data/README.md` for instructions.
- Web search tool was temporarily unavailable during this session — used direct arXiv URL fetching instead. All papers verified from real arXiv pages.

---

### Next Steps

1. **USER ACTION REQUIRED**:
   - Review `docs/literature_review.md` — confirm the 18 papers are appropriate
   - Confirm the 4 identified gaps and working contribution hypothesis
   - Provide GitHub repo URL for remote push (or create new repo)
   - Confirm which datasets to download first (recommended: Kvasir-SEG first)

2. **Agent (next session)**:
   - Add 10 more papers from backlog (especially PNS-Net, ESFPNet, SUN-SEG paper)
   - Phase 0 sign-off with user before moving to Phase 1
   - Once approved: git commit the Phase 0 work with message:
     `"Phase 0: Initialize project structure and complete first-pass literature review (18 papers, SOTA table, gap analysis)"`
   - Create `dev` branch for Phase 1 work

---

*Session ended: ~22:30 IST*

## 2026-09-12 — Session 2: Expanded Literature & Industry Trends

**Date**: Saturday, 2026-09-12  
**Time**: ~22:45 IST  

---

### What Was Done

1. **Literature Review Expansion**:
   - Expanded the literature review from 18 papers to 58 peer-reviewed papers with quantitative metrics.
   - Updated the SOTA comparison tables based on the new papers.
   - Created a python script `scripts/verify_literature_review.py` to automatically verify literature review integrity (no duplicates, missing metrics).

2. **Industry Trends Analysis**:
   - Researched the top companies leading the field of AI-assisted colonoscopy (e.g., Medtronic / GI Genius, SKOUT).
   - Compiled a comprehensive 800+ line document at `docs/industry_trends.md` detailing commercial Real-Time Video CADe/CADx Systems, clinical evidence, regulatory standards, and architectural technical breakdowns.

3. **Version Control**:
   - Committed the changes (58 papers + industry trends + verification script) to the repository.

---

### Blockers

- Subagent execution was interrupted by a system restart during the review phase, but the files were successfully generated and have now been committed manually.

---

### Next Steps

1. **Phase 1 Initiation**:
   - Begin Phase 1 (Dataset preparation and DataLoaders).
   - Set up the Kvasir-SEG dataset in the `data/raw` folder.
   - Implement `src/data_loaders/dataset.py` to load and augment Kvasir-SEG images and masks.
   - Build a PyTorch Dataset class and DataLoader.
   - Create a visualization script to ensure data is loaded correctly (images and masks align).

---

## 2026-09-12 — Session 3: Phase 1 (Dataset Preparation & DataLoaders)

**Date**: Saturday, 2026-09-12  
**Time**: ~22:45 IST  

---

### What Was Done

1. **Dataset Acquisition**:
   - Automated download and extraction of the **Kvasir-SEG** dataset (1,000 images + masks).
2. **Dataset Splits**:
   - Created `src/data_loaders/generate_splits.py` to establish the community standard **900 train / 100 test** split.
   - Outputs: `data/processed/train.txt` and `data/processed/test_splits/kvasir_test.txt`.
3. **PyTorch DataLoaders**:
   - Implemented `src/data_loaders/dataset.py` featuring the `PolypDataset` class.
   - Integrated `albumentations` for standard medical imaging augmentations (Horizontal/Vertical Flip, RandomRotate90, ShiftScaleRotate, ColorJitter) on the training set, and standard normalization for the test set. Images resized to SOTA standard **352x352**.
4. **Verification**:
   - Created `src/utils/visualize_data.py` which loads a batch using PyTorch `DataLoader` and generates an overlay visualization to guarantee spatial alignment of images and masks post-augmentation.

---

### Results / Findings

- The PyTorch `PolypDataset` handles tensor conversions and image-mask alignment perfectly.
- Sanity checks confirm image inputs scale to `[-2.118, 2.640]` (normalized) and masks to `[0.0, 1.0]`, ready for loss functions.

---

### Next Steps

1. **Phase 2 Initiation**:
   - Begin **Phase 2 (Baseline Model)**.
   - Implement a standard Medical Segmentation baseline (e.g., U-Net or PraNet) in `src/models/`.
   - Setup the training loop in `src/train.py` (losses, optimizers, LR scheduling, wandb logging).
   - Setup the evaluation loop in `src/eval.py` to compute Dice and IoU on validation set.

---

## 2026-09-16 — Session 4: Checkpoint Forensics & 2025–2026 Research Digest

**Date**: Wednesday, 2026-09-16  
**Time**: 09:10 IST  

---

### What Was Done

1. **Model Checkpoints Forensics**:
   - Inspected `M:\chakramodelpro\_weights_check\weights\checkpoints\` contents via PyTorch inspection script.
   - Identified `combo1_best.pth` (102.7 MB) as a **PraNet** (Res2Net + RFB1-4 + PPD + Reverse Attention RA1-4) architecture.
   - Identified `chakra_transformer_best.pth` (1.24 GB) as a **Vision Transformer (ViT-Large / Segmenter)** with `cls_token`, `patch_embed.proj`, 24 Transformer blocks, and multi-scale `decode_head`.
2. **2025–2026 Literature Synthesis**:
   - Evaluated 4 prominent recent directions: State Space Models (Polyp-Mamba [P24], UltraLight VM-UNet [P25]), Pseudo-Depth Conditioning (DepthPolyp, May 2026), 3-stage hierarchical frameworks (PolypVision, Aug 2026), and Explainable CADx (PolypSeg-GradCAM, Jan 2026).
   - Grounded SOTA performance matrix across Kvasir-SEG, CVC-ClinicDB, CVC-ColonDB, ETIS-Larib, and SUN-SEG benchmarks.
3. **Digest Documentation**:
   - Published structured Daily Research Digest artifact for the ChakraModel development pipeline.

---

### Results / Findings

- **DONE**:
  - Checkpoint structure verified via `torch.load`:
    - `combo1_best.pth`: keys `{'enc0', 'enc1', 'enc2', 'enc3', 'enc4', 'rfb1', 'rfb2', 'rfb3', 'rfb4', 'ppd_conv', 'ppd_pred', 'ra1', 'ra2', 'ra3', 'ra4'}`.
    - `chakra_transformer_best.pth`: keys `{'backbone', 'decode_head'}`.
- **NOT YET RUN**:
  - Live model training and test-split evaluation loops (`src/train.py` and `src/eval.py`).

---

### Blockers

- None currently. Phase 2 baseline models (`src/models/pranet.py`, `src/models/unet.py`) are queued for coding.

---

### Next Steps

1. Implement `src/models/pranet.py` matching the architecture of `combo1_best.pth`.
2. Run zero-shot validation on `data/processed/test_splits/kvasir_test.txt` using `combo1_best.pth` to log real baseline numbers.
3. Scaffold `src/models/transformer_segmenter.py` to interface with `chakra_transformer_best.pth`.

---

## 2026-09-17 — Session 5: 2026 SOTA Literature Synthesis & Chakra-v2 Architecture Roadmap

**Date**: Thursday, 2026-09-17  
**Time**: 09:10 IST  

---

### What Was Done

1. **Frontier Literature Intelligence & Analysis**:
   - Synthesized 2025–2026 emerging paradigms in polyp detection and segmentation: State Space Models (Mamba / CSG-Mamba, PolyMamba-Net), Foundation Model Adapters (ASAM2-UNet, Lite-PolypInductor), Diffusion Priors (Diff-Polyp [P57], InstEditSeg), and Real-Time Video Hysteresis (SUN-SEG [P33], PNS-Net [P10]).
   - Re-verified benchmark metrics across 5 canonical datasets (Kvasir-SEG, CVC-ClinicDB, CVC-ColonDB, ETIS-Larib, CVC-300) directly against `docs/literature_review.md` without data fabrication.
2. **Chakra-v2 Hybrid Architecture Specification**:
   - Defined architectural bridge between fast spatial reverse attention (`combo1_best.pth`, 102.7 MB) and global semantic transformers (`chakra_transformer_best.pth`, 1.24 GB).
   - Formulated 3-stage forward pipeline: Dual-Path Hybrid Encoder -> High-Frequency Boundary Gating -> Cascaded Reverse Attention Decoder.
3. **Documentation Deliverables**:
   - Authored comprehensive daily research digest at `docs/daily_research_digest_2026_09_17.md` and saved to brain artifacts.
   - Updated arXiv license agreement record at `.licenses/literature_search_arxiv_LICENSE.txt`.

---

### Results / Findings

- **DONE**:
  - Frontier literature intelligence and SOTA comparison table compiled and grounded.
  - SOTA performance ceiling confirmed: Polyp-Mamba ([P24], mDice 0.935 Kvasir, 0.812 ETIS, 48 FPS) and UltraLight VM-UNet ([P25], 49k params, >120 FPS).
  - Checkpoint layer maps and tensor keys matched to PraNet and ViT-Large/Segmenter.
- **PARTIALLY DONE**:
  - Implementation of `src/models/pranet.py` to run `combo1_best.pth`.
- **NOT YET RUN**:
  - Live model execution of `combo1_best.pth` on `kvasir_test.txt` (Phase 2 Task 2).

---

### Blockers

- None. Baseline model class creation is ready to begin.

---

### Next Steps

1. Implement `src/models/pranet.py` with identical layer names (`enc0..4`, `rfb1..4`, `ppd_conv`, `ra1..4`).
2. Run live inference of `combo1_best.pth` on `data/processed/test_splits/kvasir_test.txt` using `src/eval.py`.
3. Compute and log real Dice, IoU, and measured FPS to `results/metrics/baseline_combo1.json`.


