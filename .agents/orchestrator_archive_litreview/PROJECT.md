# Project: Polyp Detection & Segmentation Literature Review Expansion

## Architecture & Scope
- Scope: Expand literature review in `docs/literature_review.md` by researching and documenting up to 40 additional papers from arXiv and PubMed.
- Target document: `docs/literature_review.md`
- Verification script: `scripts/verify_literature_review.py`
- Standards:
  - Strict quality bar: Only papers reporting quantitative metrics (Dice, IoU, mDice, mIoU, FPS, F-measure, precision, recall, etc.).
  - Chronology: Primarily 2020 or newer (plus classic baselines where appropriate).
  - Format: Strictly adhere to `[PXX]` format established in `docs/literature_review.md`.
  - Zero duplicates: Verified by automated verification script across titles, URLs, and DOIs.

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M1 | Literature Search & Discovery | 3 Explorers search arXiv & PubMed across 3 domains | none | IN_PROGRESS |
| M2 | Documentation & Verification Script | 1 Worker compiles up to 40 papers, updates SOTA table, updates gap analysis, creates verification script | M1 | PLANNED |
| M3 | Review & Challenger Verification | 2 Reviewers + 2 Challengers verify zero duplicates, metrics completeness, formatting | M2 | PLANNED |
| M4 | Forensic Audit | 1 Forensic Auditor performs integrity verification | M3 | PLANNED |
| M5 | Git Commit & Parent Completion Handoff | Commit to git repo, send completion report to parent | M4 | PLANNED |

## Interface Contracts & Guidelines
- Each paper entry must follow:
  ```markdown
  #### [PXX] Title
  - **Authors**: ...
  - **Year/Venue**: ...
  - **arXiv** / **DOI**: ...
  - **Method Summary**: ...
  - **Reported Metrics**: ...
  - **Key Insight**: ...
  - **Limitations**: ...
  - **Relevance**: ...
  - **Code**: ... (if available)
  ```
- SOTA Comparison Table:
  - Columns: Method | Year | Backbone | Kvasir Dice | Kvasir IoU | ClinicDB Dice | ClinicDB IoU | ColonDB Dice | ETIS Dice | CVC-300 Dice | FPS
  - Real-Time / Detection table updated where applicable.
- Verification script:
  - Exit code 0 on clean pass; non-zero on failure.
  - Checks: duplicate titles, duplicate URLs, duplicate DOIs, presence of required sections (Title, Authors, Year, Method Summary, Metrics, Relevance).
