## 2026-09-12T15:55:15Z
You are Explorer 3 on the Polyp Detection & Segmentation Literature Review project.
Your working directory is: m:\chakramodelpro\polyp-detection-research\.agents\teamwork_preview_explorer_3\
Project root: m:\chakramodelpro\polyp-detection-research\

Scope:
Research and discover 12 to 15 high-quality, quantitative papers on:
**Real-Time / Lightweight Architectures, Boundary-Aware Networks, CADe Detection (YOLO / Diffusion / Edge), and Multi-Scale Attention (2020–2026)**.

Crucial Guidelines:
1. First read `docs/literature_review.md` (especially lines 50-335) to see existing papers [P01] to [P18]. You MUST NOT duplicate any of [P01] to [P18]!
   Existing papers include: [P04] ColonSegNet, [P06] HarDNet-MSEG, [P12] YOLO-v11n+LOF, [P13] MicroAUNet, [P15] PolypVision, [P16] EndoSight AI, [P18] PolypSeg-GradCAM.
2. Search arXiv and PubMed. You have available skills and scripts:
   - `literature-search-arxiv`: script at `C:/Users/imgk3/.gemini/config/plugins/science/skills/literature_search_arxiv/scripts/search_arxiv.py`
     Example: `python "C:/Users/imgk3/.gemini/config/plugins/science/skills/literature_search_arxiv/scripts/search_arxiv.py" --query "real time polyp segmentation" --max_results 15`
   - `pubmed-database`: script at `C:/Users/imgk3/.gemini/config/plugins/science/skills/pubmed_database/scripts/pubmed_api.py`
   - Target topics: DoubleU-Net (Jha et al., CBMS 2020), MSNet (Zhao et al., MICCAI 2021), BSASNet, DDANet, TGANet, ESFPNet, boundary-guided polyp segmentation, edge/FPGA/mobile deployment, real-time YOLO variants for colonoscopy detection, diffusion-based polyp segmentation.
3. Strict Quality Bar:
   Only select papers that report explicit quantitative metrics (Dice, IoU, FPS, latency, mAP, precision, recall) on standard datasets.
4. For each selected paper, format as:
   - **Title**
   - **Authors**
   - **Year/Venue**
   - **arXiv / DOI / PubMed URL**
   - **Method Summary**
   - **Reported Metrics** (exact numbers for each dataset and FPS if reported)
   - **Key Insight**
   - **Limitations**
   - **Relevance**
   - **Code** (if available)
5. Save your complete report to `m:\chakramodelpro\polyp-detection-research\.agents\teamwork_preview_explorer_3\handoff.md`.
6. Send a message to the orchestrator when completed with a summary of the papers found.
