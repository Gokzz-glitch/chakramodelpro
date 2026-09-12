# Data Directory — Download Instructions & Licenses

> **⚠️ IMPORTANT**: All datasets must be downloaded manually and placed here.  
> Raw data is git-ignored. Do NOT commit datasets to this repository.  
> Document your download date and source URL in this file after downloading.

---

## Directory Structure

```
data/
├── raw/                    ← [GIT-IGNORED] Place downloaded datasets here
│   ├── kvasir-seg/
│   │   ├── images/         ← 1000 .jpg files
│   │   └── masks/          ← 1000 .jpg files (binary masks)
│   ├── cvc-clinicdb/
│   │   ├── Original/       ← 612 .png files
│   │   └── Ground Truth/   ← 612 .png files
│   ├── cvc-colondb/
│   │   ├── images/
│   │   └── masks/
│   ├── etis-larib/
│   │   ├── ETIS-LaribPolypDB/
│   │   └── Ground Truth/
│   ├── cvc-300/
│   │   ├── images/
│   │   └── masks/
│   ├── sun-seg/            ← Video dataset (large, ~20GB)
│   └── polypgen/           ← Multi-center dataset
└── processed/              ← [GIT-IGNORED] Preprocessed splits (auto-generated)
    ├── train.txt            ← List of training image paths
    ├── val.txt              ← List of validation image paths
    └── test_splits/
        ├── kvasir_test.txt
        ├── clinicdb_test.txt
        ├── colondb.txt
        ├── etis.txt
        └── cvc300.txt
```

---

## Dataset 1: Kvasir-SEG

| Field | Value |
|-------|-------|
| **Images** | 1,000 colonoscopy images + pixel-level segmentation masks |
| **Format** | JPEG (variable resolution, mostly 332×487 to 1920×1072) |
| **Annotation** | Expert gastroenterologist-annotated binary masks |
| **License** | **CC-BY 4.0** (free for research AND commercial use with attribution) |
| **Download** | https://datasets.simula.no/kvasir-seg/ |
| **Citation** | Jha et al., MMM 2020. DOI: 10.1007/978-3-030-37734-2_37 |
| **Size** | ~44 MB |
| **Split used** | 900 train / 100 test (standard PraNet split) |

**Download command**:
```bash
# Manual download from: https://datasets.simula.no/kvasir-seg/
# File: kvasir-seg.zip (~44MB)
# Unzip to: data/raw/kvasir-seg/
```

**Downloaded**: ☐ (mark with date when done)

---

## Dataset 2: CVC-ClinicDB

| Field | Value |
|-------|-------|
| **Images** | 612 still frames from 29 colonoscopy sequences |
| **Format** | PNG (384×288 pixels) |
| **Annotation** | Binary polygon masks |
| **License** | **Research use only** (see Grand Challenge terms) |
| **Download** | https://polyp.grand-challenge.org/CVCClinicDB/ |
| **Citation** | Bernal et al., Computerized Medical Imaging and Graphics, 2015 |
| **Size** | ~64 MB |
| **Split used** | 550 train / 62 test (standard PraNet split) |

**Download command**:
```bash
# Register at: https://polyp.grand-challenge.org/
# Download: CVC-ClinicDB.zip
# Unzip to: data/raw/cvc-clinicdb/
```

**Downloaded**: ☐ (mark with date when done)

---

## Dataset 3: CVC-ColonDB

| Field | Value |
|-------|-------|
| **Images** | 380 colonoscopy frames (15 sequences) |
| **Format** | TIFF/PNG |
| **License** | Research use only |
| **Download** | https://polyp.grand-challenge.org/ (same as ClinicDB) |
| **Citation** | Tajbakhsh et al., TMI 2015 |
| **Size** | ~45 MB |
| **Split used** | **ENTIRE DATASET used as zero-shot test set** (not in training) |

**Downloaded**: ☐

---

## Dataset 4: ETIS-LaribPolypDB

| Field | Value |
|-------|-------|
| **Images** | 196 colonoscopy frames |
| **Format** | PNG (1225×966 pixels, high resolution) |
| **License** | Research use only |
| **Download** | https://polyp.grand-challenge.org/ |
| **Citation** | Silva et al., Journal of Medical Informatics, 2014 |
| **Size** | ~200 MB (high res) |
| **Split used** | **ENTIRE DATASET as zero-shot test set** |
| **Note** | Hardest dataset — polyps are flat and subtle. Biggest cross-dataset performance drop. |

**Downloaded**: ☐

---

## Dataset 5: CVC-300 (EndoScene)

| Field | Value |
|-------|-------|
| **Images** | 300 colonoscopy frames |
| **Format** | PNG |
| **License** | Research use only |
| **Download** | https://polyp.grand-challenge.org/ |
| **Citation** | Vázquez et al., Journal of Healthcare Engineering, 2017 |
| **Size** | ~20 MB |
| **Split used** | 60 images as test set (subset used in PraNet paper) |

**Downloaded**: ☐

---

## Dataset 6: SUN-SEG (Video Polyp Segmentation)

| Field | Value |
|-------|-------|
| **Videos** | 49,136 frames from 1,000+ video clips |
| **Format** | JPEG frames + PNG masks |
| **License** | **CC-BY-NC 4.0** (non-commercial only) |
| **Download** | https://github.com/GewelsJI/VPS-Net (see README for Google Drive link) |
| **Citation** | Ji et al., MICCAI 2021 |
| **Size** | ~20 GB |
| **Split used** | TBD — Phase 4+ (video experiments) |
| **Note** | Download only when starting video experiments. Very large. |

**Downloaded**: ☐ (defer to Phase 4)

---

## Dataset 7: PolypGen (Multi-Center)

| Field | Value |
|-------|-------|
| **Images** | 3,762 images from 6 clinical centers across 4 countries |
| **Format** | PNG |
| **License** | **CC-BY 4.0** |
| **Download** | https://zenodo.org/record/7548828 |
| **Citation** | Ali et al., Scientific Data, 2023. DOI: 10.1038/s41597-023-01981-y |
| **Size** | ~1 GB |
| **Split used** | TBD — cross-center generalization experiments |

**Downloaded**: ☐ (defer to Phase 5 generalization experiments)

---

## Standard Train/Test Split (Used by PraNet/SANet/Polyp-PVT)

This is the community-standard split — we use it for direct comparison:

```
Training:
  - Kvasir-SEG: 900 images
  - CVC-ClinicDB: 550 images
  Total: 1,450 training images

Test Sets (evaluated separately):
  - Kvasir-SEG test: 100 images
  - CVC-ClinicDB test: 62 images
  - CVC-ColonDB: 380 images (ZERO-SHOT)
  - ETIS-LaribPolypDB: 196 images (ZERO-SHOT)
  - CVC-300: 60 images (ZERO-SHOT)
```

**Source**: Fan et al. (PraNet, MICCAI 2020) — we verified this split matches SANet, Polyp-PVT

**Script to generate splits**: `src/data_loaders/generate_splits.py` (to be implemented in Phase 1)

---

## License Compliance Notes

| Dataset | License | Commercial? | Attribution Required? |
|---------|---------|------------|----------------------|
| Kvasir-SEG | CC-BY 4.0 | ✅ Yes | ✅ Yes |
| CVC-ClinicDB | Research Only | ❌ No | ✅ Yes |
| CVC-ColonDB | Research Only | ❌ No | ✅ Yes |
| ETIS-LaribPolypDB | Research Only | ❌ No | ✅ Yes |
| CVC-300 | Research Only | ❌ No | ✅ Yes |
| SUN-SEG | CC-BY-NC 4.0 | ❌ No | ✅ Yes |
| PolypGen | CC-BY 4.0 | ✅ Yes | ✅ Yes |

> **For paper submission**: Include full dataset citations and license acknowledgments in the manuscript.
