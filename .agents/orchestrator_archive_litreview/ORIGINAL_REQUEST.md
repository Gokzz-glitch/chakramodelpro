# Original User Request

## 2026-09-12T15:53:46Z

You are the Project Orchestrator.

Your working directory is: m:\chakramodelpro\polyp-detection-research\.agents\orchestrator
Project root: m:\chakramodelpro\polyp-detection-research
User request file: m:\chakramodelpro\polyp-detection-research\.agents\ORIGINAL_REQUEST.md

Mission:
Expand the existing polyp detection literature review by researching and summarizing up to 40 additional high-quality papers using arXiv and PubMed databases.

Requirements & Acceptance Criteria:
1. Literature Search:
   - Search arXiv and PubMed for highly relevant, peer-reviewed papers or preprints on polyp detection, segmentation, and video colonoscopy analysis (preferably 2020 or newer).
   - Strict quality bar: Only include papers that report quantitative metrics (e.g., Dice, IoU, mDice, mIoU, FPS, F-measure, precision, recall). If fewer than 40 highly relevant papers are found, stop there rather than lowering the quality bar.
2. Documentation:
   - Read docs/literature_review.md to understand the existing format, categories, and papers already present.
   - Append the new papers to docs/literature_review.md using the existing format ([PXX] title, authors, year/venue, link/arXiv/DOI, method summary, reported metrics, relevance, code/dataset if any).
   - Update the SOTA comparison table and gap analysis based on these new findings.
   - Ensure there are strictly NO duplicate papers (by title, DOI, or URL) compared to existing papers or newly added papers.
3. Completeness & Verification:
   - Each newly added paper must include Title, Authors, Year, Method Summary, Metrics, and Relevance.
   - Write and execute a Python script or automated check that explicitly verifies no paper titles, URLs, or DOIs are duplicated in docs/literature_review.md.
   - Verify the SOTA Comparison Table includes newly discovered baseline numbers.
4. Version Control:
   - Commit the updated documentation and any verification script to the git repository with a descriptive commit message.

Maintain your plan.md and progress.md in your working directory (m:\chakramodelpro\polyp-detection-research\.agents\orchestrator\).
When all milestones are complete, send a completion report back to Sentinel (parent) claiming victory with full summary of added papers, metrics, and verification results.
