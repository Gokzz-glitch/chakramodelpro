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
