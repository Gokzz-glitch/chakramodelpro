## 2026-09-12T15:55:15Z

You are Explorer 2 on the Polyp Detection & Segmentation Literature Review project.
Your working directory is: m:\chakramodelpro\polyp-detection-research\.agents\teamwork_preview_explorer_2\
Project root: m:\chakramodelpro\polyp-detection-research\

Scope:
Research and discover 12 to 15 high-quality, quantitative papers on:
**Video Polyp Segmentation (VPS), Temporal Modeling, Multi-Center Benchmarks, and Datasets (2020–2026)**.

Crucial Guidelines:
1. First read `docs/literature_review.md` (especially lines 50-335) to see existing papers [P01] to [P18]. You MUST NOT duplicate any of [P01] to [P18]!
   Existing papers include: [P01] Kvasir-SEG, [P02] CVC-ClinicDB, [P10] PNS-Net, [P11] A Multi-Center Analysis (Ghatwary et al.).
2. Search arXiv and PubMed. You have available skills and scripts:
   - `literature-search-arxiv`: script at `C:/Users/imgk3/.gemini/config/plugins/science/skills/literature_search_arxiv/scripts/search_arxiv.py`
     Example: `python "C:/Users/imgk3/.gemini/config/plugins/science/skills/literature_search_arxiv/scripts/search_arxiv.py" --query "video polyp segmentation" --max_results 15`
   - `pubmed-database`: script at `C:/Users/imgk3/.gemini/config/plugins/science/skills/pubmed_database/scripts/pubmed_api.py`
   - Target topics: SUN-SEG dataset paper (Ji et al.), PolypGen dataset paper (Ali et al.), VPS-Net, LDNet, CC-Net for video polyps, temporal consistency models, endoscopic video tracking and detection networks, etc.
3. Strict Quality Bar:
   Only select papers that report explicit quantitative metrics (Dice, IoU, S-measure, E-measure, FPS, mAP, etc.) on video or multi-center datasets (SUN-SEG, PolypGen, CVC-VideoClinicDB, etc.).
4. For each selected paper, format as:
   - **Title**
   - **Authors**
   - **Year/Venue**
   - **arXiv / DOI / PubMed URL**
   - **Method Summary**
   - **Reported Metrics** (exact numbers for each dataset)
   - **Key Insight**
   - **Limitations**
   - **Relevance**
   - **Code / Dataset URL** (if available)
5. Save your complete report to `m:\chakramodelpro\polyp-detection-research\.agents\teamwork_preview_explorer_2\handoff.md`.
6. Send a message to the orchestrator when completed with a summary of the papers found.
