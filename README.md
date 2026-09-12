# Polyp Detection & Segmentation — Research Project

> **Status**: 🔬 Phase 0 — Literature Review  
> **Goal**: Research-grade polyp detection/segmentation for paper submission  
> **Started**: 2026-09-12  
> **Primary Investigator**: [Your Name]

---

## Project Overview

This repository contains the full, reproducible pipeline for developing and evaluating deep-learning models for **colorectal polyp detection and segmentation** in colonoscopy images and video. The work is intended for eventual publication in a peer-reviewed venue (e.g., MedIA, MICCAI, CVPR Workshop on Medical Imaging).

### Motivation

Colorectal cancer (CRC) is the 2nd leading cause of cancer death worldwide. Colonoscopy is the gold-standard screening tool, but polyp miss-rates of **22–28%** remain a serious clinical problem. Computer-aided detection (CADe) and segmentation (CADx) systems powered by deep learning have the potential to close this gap — but most current research lacks either **real-time performance** OR **generalizability** across clinical sites and endoscope models.

### Our Target Contribution

> *To be refined after literature review is complete and gap is evidenced.*  
> Current working hypothesis: **A lightweight, temporally-aware hybrid (CNN+Transformer) model that achieves SOTA segmentation accuracy on still images while maintaining real-time throughput (≥30 FPS) for video colonoscopy — with improved cross-dataset generalizability.**

---

## Project Phases

| Phase | Description | Status |
|-------|-------------|--------|
| 0 | Literature Review | 🟡 In Progress |
| 1 | Dataset Preparation & EDA | ⬜ Pending |
| 2 | Baseline Model (U-Net / PraNet repro) | ⬜ Pending |
| 3 | Proposed Architecture Design | ⬜ Pending |
| 4 | Ablation Studies | ⬜ Pending |
| 5 | Cross-dataset Generalization Eval | ⬜ Pending |
| 6 | Paper Writing | ⬜ Pending |

---

## Datasets (Planned)

| Dataset | Images | Type | License | Source |
|---------|--------|------|---------|--------|
| Kvasir-SEG | 1,000 | Still + Masks | CC-BY 4.0 | [simula.no](https://datasets.simula.no/kvasir-seg/) |
| CVC-ClinicDB | 612 | Still + Masks | Research | [cvc.uab.cat](https://polyp.grand-challenge.org/) |
| CVC-ColonDB | 380 | Still + Masks | Research | Grand Challenge |
| ETIS-LaribPolypDB | 196 | Still + Masks | Research | [polyp.grand-challenge.org](https://polyp.grand-challenge.org/) |
| CVC-300 (EndoScene) | 300 | Still + Masks | Research | [polyp.grand-challenge.org](https://polyp.grand-challenge.org/) |
| SUN-SEG | 49,136 | Video + Masks | CC-BY-NC | [GitHub](https://github.com/GewelsJI/VPS-Net) |
| PolypGen | 3,762 | Multi-center | CC-BY 4.0 | [Zenodo](https://zenodo.org/record/7548828) |

> ⚠️ See `data/README.md` for download instructions and license compliance notes.

---

## Repository Structure

```
polyp-detection-research/
├── README.md                       ← This file
├── docs/
│   ├── literature_review.md        ← All papers read, SOTA table, gap analysis
│   ├── daily_log.md                ← Date-wise progress log
│   ├── architecture_notes.md       ← Architectural decisions with reasoning
│   └── experiment_log.md           ← Every training run (params + results)
├── data/
│   ├── raw/                        ← [git-ignored] Downloaded datasets
│   ├── processed/                  ← [git-ignored] Preprocessed splits
│   └── README.md                   ← Download instructions + licenses
├── src/
│   ├── models/                     ← Model architecture files
│   ├── data_loaders/               ← Dataset classes and augmentation
│   ├── train.py                    ← Training entry point
│   ├── eval.py                     ← Evaluation entry point
│   └── utils/                     ← Metrics, visualization, helpers
├── configs/                        ← YAML experiment configs
├── checkpoints/                    ← [git-ignored] Saved model weights
├── results/
│   ├── metrics/                    ← JSON/CSV metric files per run
│   ├── plots/                      ← Loss curves, ablation charts
│   └── sample_predictions/         ← Qualitative visualizations
├── requirements.txt
└── .gitignore
```

---

## Quick Start

```bash
# 1. Clone
git clone <repo_url>
cd polyp-detection-research

# 2. Setup environment
python -m venv .venv
.venv\Scripts\activate       # Windows
pip install -r requirements.txt

# 3. Download datasets (see data/README.md)

# 4. Train baseline
python src/train.py --config configs/baseline_unet.yaml

# 5. Evaluate
python src/eval.py --config configs/baseline_unet.yaml --checkpoint checkpoints/best.pt
```

---

## Strict Rules for This Repository

1. **NO hardcoded metric values** — all numbers come from real computation
2. **NO mock/dummy data** — only real dataset paths
3. **NO skipping steps** — if data is missing, code raises an explicit error
4. **Every metric** (Dice, IoU, FPS) computed on real validation data
5. **Every architectural/hyperparameter decision** documented in `docs/architecture_notes.md`
6. **Git commits** after every meaningful milestone with descriptive messages

---

## Environment

- Python 3.10+
- PyTorch 2.x
- CUDA 12.x (recommended)

---

## Citation

> *To be filled once paper is submitted.*

---

## License

Code: MIT  
Trained weights: CC-BY-NC-SA 4.0  
Dataset licenses: See `data/README.md`
