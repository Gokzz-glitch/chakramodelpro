# Plan: Polyp Detection Literature Review Expansion

## Objective
Expand `docs/literature_review.md` by researching and summarizing up to 40 additional high-quality papers with quantitative metrics from arXiv and PubMed, updating the SOTA comparison table and gap analysis, verifying zero duplicates via automated script, and committing the changes to git.

## Milestones & Iteration Strategy (Project Pattern - 2B)

### Phase 1: Exploration & Paper Discovery (3 Explorers in parallel)
- **Explorer 1** (`.agents/teamwork_preview_explorer_1/`):
  - Focus: Transformer-based, Mamba/State-Space, and Hybrid CNN-Transformer Polyp Segmentation (2021–2026).
  - Search arXiv & PubMed for models like SSFormer, Polyp-PVT v2, ColonFormer, FCBFormer, SegFormer variants, Mamba-based polyp segmentation.
  - Extract: Title, Authors, Year/Venue, URL/arXiv/DOI, Method Summary, Reported Metrics (Dice, IoU, etc. on Kvasir-SEG, CVC-ClinicDB, ColonDB, ETIS), Relevance, Code.
  - Verify none duplicate existing P01-P18.
- **Explorer 2** (`.agents/teamwork_preview_explorer_2/`):
  - Focus: Video Polyp Segmentation & Detection, Temporal Modeling, and Benchmarks (2020–2026).
  - Search arXiv & PubMed for video polyp segmentation (VPS), temporal attention, SUN-SEG, PolypGen, PNS-Net, VPS-Net, cross-dataset multi-center video studies.
  - Extract: Title, Authors, Year/Venue, URL/arXiv/DOI, Method Summary, Reported Metrics, Relevance, Code/Dataset.
  - Verify none duplicate existing P01-P18.
- **Explorer 3** (`.agents/teamwork_preview_explorer_3/`):
  - Focus: Real-Time, Lightweight, Boundary-Aware, and Detection (CADe/YOLO/Diffusion) Models (2020–2026).
  - Search arXiv & PubMed for real-time models (high FPS), edge devices, boundary-guided networks (e.g. BSASNet, DDANet, MSNet, DoubleU-Net), YOLO variants for polyp detection, diffusion models for segmentation.
  - Extract: Title, Authors, Year/Venue, URL/arXiv/DOI, Method Summary, Reported Metrics, Relevance, Code.
  - Verify none duplicate existing P01-P18.

### Phase 2: Implementation & Documentation (1 Worker)
- **Worker** (`.agents/worker_1/`):
  - Ingest findings from all 3 Explorers.
  - Filter and select up to 40 distinct, high-relevance papers with verified quantitative metrics.
  - Number sequentially starting from `[P19]` through `[PXX]`.
  - Append to `docs/literature_review.md` preserving and extending the document structure and formatting.
  - Update the **SOTA Comparison Table** with new baseline numbers across standard benchmarks (Kvasir, ClinicDB, ColonDB, ETIS, CVC-300, etc.) and real-time detection.
  - Update the **Gap Analysis & Our Contribution** and clean up the **Papers To Read (Backlog)**.
  - Author a verification script `scripts/verify_literature_review.py` that parses `docs/literature_review.md`, extracts all paper titles, URLs, and DOIs, verifies 0 duplicates, checks required fields (Title, Authors, Year, Method Summary, Metrics, Relevance), and verifies SOTA table coverage.
  - Execute the verification script and verify clean pass.

### Phase 3: Review & Adversarial Challenge (2 Reviewers + 2 Challengers)
- **Reviewer 1 & Reviewer 2** (`.agents/teamwork_preview_reviewer_1/`, `.agents/teamwork_preview_reviewer_2/`):
  - Independent review of `docs/literature_review.md` and `scripts/verify_literature_review.py`.
  - Verify compliance with all acceptance criteria, format integrity, metric reporting rigor.
- **Challenger 1 & Challenger 2** (`.agents/teamwork_preview_challenger_1/`, `.agents/teamwork_preview_challenger_2/`):
  - Adversarially stress-test for duplicate titles (fuzzy/exact), invalid URLs, missing metrics, and run independent validation checks.

### Phase 4: Forensic Audit & Integrity Gate (1 Auditor)
- **Auditor** (`.agents/teamwork_preview_auditor_1/`):
  - Verify no simulated/fake papers or fabricated metrics.
  - Verify authentic arXiv/PubMed sources.
  - Confirm integrity of the literature review and verification script.

### Phase 5: Version Control & Handoff
- Worker or designated agent stages and commits changes to git with a descriptive commit message.
- Orchestrator synthesizes all results and sends a final completion report to Sentinel (parent).
