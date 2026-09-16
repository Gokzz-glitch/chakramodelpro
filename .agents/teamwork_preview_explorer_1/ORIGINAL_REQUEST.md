## 2026-09-12T15:55:15Z

You are Explorer 1 on the Polyp Detection & Segmentation Literature Review project.
Your working directory is: m:\chakramodelpro\polyp-detection-research\.agents\teamwork_preview_explorer_1\
Project root: m:\chakramodelpro\polyp-detection-research\

Scope:
Research and discover 12 to 15 high-quality, quantitative papers on:
**Transformer-Based, Mamba/State-Space, and Hybrid CNN-Transformer Polyp Segmentation (2021–2026)**.

Crucial Guidelines:
1. First read `docs/literature_review.md` (especially lines 50-335) to see existing papers [P01] to [P18]. You MUST NOT duplicate any of [P01] to [P18]!
   Specifically already present: Kvasir-SEG, CVC-ClinicDB, PraNet, ColonSegNet, SANet, HarDNet-MSEG, Polyp-PVT, HiFiSeg, ASGNet, PNS-Net, Multi-Center Analysis, YOLO-v11n+LOF, MicroAUNet, GRAFNet, PolypVision, EndoSight AI, QFedPolyp, PolypSeg-GradCAM.
2. Search arXiv and PubMed. You have available skills and scripts:
   - `literature-search-arxiv`: script at `C:/Users/imgk3/.gemini/config/plugins/science/skills/literature_search_arxiv/scripts/search_arxiv.py`
     Example: `python "C:/Users/imgk3/.gemini/config/plugins/science/skills/literature_search_arxiv/scripts/search_arxiv.py" --query "polyp transformer segmentation" --max_results 15`
   - `pubmed-database`: script at `C:/Users/imgk3/.gemini/config/plugins/science/skills/pubmed_database/scripts/pubmed_api.py`
   - You can also search for prominent models like SSFormer, ColonFormer, FCBFormer, Polyp-SAM, SegFormer in polyp segmentation, Polyp-Mamba / Mamba polyp, TransUNet variants for polyp segmentation, PVT-based variants, MSNet, etc.
3. Strict Quality Bar:
   Only select papers that report explicit quantitative metrics (Dice, IoU/mIoU, FPS, etc.) on standard datasets (Kvasir-SEG, CVC-ClinicDB, CVC-ColonDB, ETIS, CVC-300).
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
   - **Code** (if available)
5. Save your complete report to `m:\chakramodelpro\polyp-detection-research\.agents\teamwork_preview_explorer_1\handoff.md`.
6. Send a message to the orchestrator when completed with a summary of the papers found.
