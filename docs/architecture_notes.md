# Architecture Notes — Decisions & Reasoning

> **Last Updated**: 2026-09-12  
> **Purpose**: Every major architecture/hyperparameter decision with reasoning.  
> This becomes the "Methodology" section of the paper.  
> **Rule**: No decision in code without an entry here first.

---

## Table of Contents

1. [Task Formulation](#task-formulation)
2. [Backbone Selection](#backbone-selection)
3. [Decoder Design](#decoder-design)
4. [Loss Functions](#loss-functions)
5. [Data Augmentation Strategy](#data-augmentation-strategy)
6. [Training Protocol](#training-protocol)
7. [Evaluation Protocol](#evaluation-protocol)
8. [Pending Decisions](#pending-decisions)

---

## Task Formulation

**Decision**: Frame the primary task as **binary segmentation** (polyp mask vs. background), not detection (bounding box) or classification.

**Reasoning**:
- Pixel-level segmentation provides the most clinical utility (boundary delineation, size estimation, resection planning)
- Dice coefficient is the established primary metric in colonoscopy AI literature
- Detection (YOLO) will be added as a secondary head in later phases for CADe applications
- Reference: All 18 papers in literature review use binary segmentation as the primary task

**Implications**:
- Output: HxW binary mask (sigmoid activation)
- Primary loss: Dice + BCE (structure + pixel-level)
- Primary metrics: mDice, mIoU, F-measure, S-measure, E-measure

---

## Backbone Selection

### Phase 2 Baseline: ResNet-50 (U-Net style)

**Decision**: Use ResNet-50 pretrained on ImageNet as baseline backbone.

**Reasoning**:
- PraNet (MICCAI 2020) uses Res2Net-50 — reproducing a simpler ResNet-50 baseline gives us a lower bound before adding specialized components
- PolypSeg-GradCAM (2026) achieves Dice=0.89 with ResNet-34 — validates that standard CNNs are still competitive
- Widely available pretrained weights, well-understood behavior
- Faster training for initial experiments

**Alternative considered**: VGG-16 — rejected (no skip connections natively, slower)
**Will upgrade to**: Res2Net-50 for PraNet reproduction (Phase 2 Task 2)

---

### Phase 3 Proposed: PVT-v2-B2 + EfficientNet-B3 Hybrid

**Decision (tentative, pending Phase 2 results)**: Use a dual-encoder hybrid.

**Reasoning**:
- Polyp-PVT (2021) uses PVT-v2-B2 alone → best generalizability on ColonDB/ETIS
- HarDNet-MSEG uses lightweight CNN → best FPS
- Literature gap: no paper combines CNN (local/edge features) + Transformer (global context) in a single encoder for polyp segmentation
- EfficientNet-B3: best accuracy/parameter trade-off among CNN backbones per published benchmarks (ImageNet)
- PVT-v2-B2: hierarchical ViT, 4-scale feature pyramid, designed for dense prediction tasks

**Key concern**: Dual encoder increases parameter count and latency. Will measure FPS carefully.  
**Decision Point**: Only adopt dual encoder if PVT-only baseline shows ≥2% Dice improvement over CNN-only — otherwise stick with single encoder + attention modules.

**Status**: ⏳ Pending Phase 2 completion

---

## Decoder Design

### Phase 2 Baseline: Cascaded Partial Decoder (CPD)

**Decision**: Use CPD-style decoder for baseline.

**Reasoning**:
- CPD is used in PraNet and HarDNet-MSEG — both are strong baselines
- Aggregates high-level features first (coarse) then refines with low-level features
- Well-understood, fast (avoids full FPN which adds parameters)

**Key hyperparameters**:
- Feature channels at each scale: [64, 128, 256, 512] (ResNet-50 defaults)
- Output resolution: H/4 × W/4, upsampled to H×W with bilinear interpolation
- Final output: 1 channel (binary mask)

---

### Phase 3 Proposed: Reverse Attention + Boundary-Enhanced Decoder

**Decision (tentative)**: Add RA module from PraNet + frequency-domain boundary branch.

**Reasoning**:
- PraNet's RA module directly addresses boundary refinement, which is our Gap 4 target
- HiFiSeg (2024) and ASGNet (2026) both show frequency-domain features improve boundary accuracy
- The combination (spatial RA + frequency boundary) is novel — not done in any reviewed paper

**Implementation plan** (Phase 3):
1. Generate coarse map using CPD
2. Invert prediction to get reverse attention weights
3. Apply to mid-level features to mine boundary regions
4. Parallel branch: 2D FFT → high-frequency mask → boundary feature
5. Fuse spatial + boundary features for final prediction

**Ablation required**: Verify each component adds value independently before combining.

---

## Loss Functions

**Decision**: Binary Cross-Entropy (BCE) + Dice Loss, equal weighting.

**Formula**:
```
L = L_BCE + L_Dice
L_BCE = -[y·log(p) + (1-y)·log(1-p)]
L_Dice = 1 - (2·Σ(y·p) + ε) / (Σy + Σp + ε)
```

**Reasoning**:
- BCE provides pixel-level supervision (good for class imbalance)
- Dice loss directly optimizes the evaluation metric
- Their combination is the community standard (used in PraNet, SANet, HarDNet-MSEG)
- ε = 1.0 (smoothing factor) — prevents division by zero and reduces sensitivity to small polyps

**Alternatives considered**:
- Focal Loss: good for extreme class imbalance, but colonoscopy datasets are less imbalanced than detection tasks
- Weighted BCE: possible for small polyp emphasis — will test in ablations
- IoU loss: mathematically similar to Dice but Dice is more commonly used here

**Pending**: Test IoTD loss (IoU + Dice) from recent literature.

---

## Data Augmentation Strategy

**Decision (Phase 2 baseline)**:

```yaml
augmentations:
  random_horizontal_flip: p=0.5
  random_vertical_flip: p=0.5
  random_rotation: degrees=90, p=0.5
  random_scale: scale_range=[0.75, 1.25], p=0.5
  normalize:
    mean: [0.485, 0.456, 0.406]   # ImageNet stats
    std: [0.229, 0.224, 0.225]    # ImageNet stats
  resize: [352, 352]              # Standard size in PraNet/SANet
```

**Reasoning**:
- Standard flips/rotations: universal in medical image segmentation
- Scale jitter: polyps appear at different sizes — scale augmentation improves small polyp handling
- ImageNet normalization: required for pretrained backbones (ResNet, PVT)
- Input size 352×352: used by PraNet, SANet, Polyp-PVT — allows direct comparison

**Phase 3 additions (planned, not yet decided)**:
- Color Exchange (SANet): swap RGB channels between image pairs to decouple shape from color
- CutMix/MixUp: will evaluate on validation set before adding
- Spectral augmentation: random frequency masking — needs ablation

**Decision Point**: No augmentation added without a validated improvement on held-out validation set.

---

## Training Protocol

### Phase 2 (Baseline)

| Hyperparameter | Value | Reasoning |
|---------------|-------|-----------|
| Optimizer | Adam | PraNet, SANet both use Adam. AdamW is alternative. |
| Learning Rate | 1e-4 | Standard for finetuning pretrained encoders |
| LR Schedule | PolyLR (power=0.9) | Used in PraNet — smooth decay |
| Batch Size | 16 | Common trade-off between stability and GPU memory |
| Epochs | 100 | PraNet: 100 epochs. We'll use early stopping too. |
| Early Stopping | patience=20 epochs | Monitors validation Dice |
| Gradient Clip | max_norm=0.5 | Prevents exploding gradients |
| Weight Decay | 5e-4 | L2 regularization |

**All hyperparameters stored in YAML config** — never hardcoded in Python.

### Phase 3 (Proposed changes)

- Encoder LR: 1e-5 (lower for pretrained transformer)
- Decoder LR: 1e-4 (higher for randomly initialized decoder)
- Warmup: 1000 steps (for transformer stability)
- Mixed precision (fp16) training to improve FPS during training

**Decision Point**: Only change hyperparameters when:
1. There is a principled reason (documented here)
2. The change is validated on a held-out validation set
3. The new run is logged in `experiment_log.md`

---

## Evaluation Protocol

**Decision**: Use the **standard train/test split** used by PraNet (the community standard):

- **Training set**: 1,450 images = Kvasir-SEG (900) + CVC-ClinicDB (550)
- **Test sets** (zero-shot for generalization):
  - Kvasir-SEG test: 100 images
  - CVC-ClinicDB test: 62 images
  - CVC-ColonDB: 380 images (entire dataset)
  - ETIS-LaribPolypDB: 196 images (entire dataset)
  - CVC-300 (EndoScene): 60 images

**Reasoning**:
- This exact split is used by PraNet, SANet, Polyp-PVT, HarDNet-MSEG → enables direct comparison without re-running baselines
- ColonDB/ETIS are pure test sets (never seen in training) → measures generalization
- Reference: Fan et al. (PraNet, MICCAI 2020)

**Metrics computed**:

| Metric | Formula | Why |
|--------|---------|-----|
| mDice | 2·TP / (2·TP + FP + FN) | Primary metric in all competing methods |
| mIoU | TP / (TP + FP + FN) | Secondary metric, reported alongside Dice |
| F-measure (Fβ²=0.3) | (1+β²)·P·R / (β²·P + R) | Emphasizes precision for clinical use |
| S-measure | α·Sm + (1-α)·So, α=0.5 | Structural similarity (video metrics) |
| E-measure | Enhanced alignment measure | Captures global and local alignment |
| FPS | Frames per second on RTX GPU | Real-time viability metric |

**Code note**: All metrics computed with real forward pass on real validation data. NO threshold tuning on test set.

---

## Pending Decisions

| Decision | Depends On | Target Date |
|----------|-----------|-------------|
| Adopt dual encoder (PVT + EfficientNet)? | Phase 2 baseline Dice | After Phase 2 |
| Add temporal module for video? | Phase 3 still-image results | After Phase 3 |
| Use Dice+IoU loss or Dice+BCE? | Ablation study | Phase 2 |
| Input resolution: 352x352 or 384x384? | Speed vs. accuracy ablation | Phase 2 |
| Transformer variant (PVT-v2 vs. Swin-T vs. MiT-B2)? | Benchmark comparison | Phase 3 |
| Knowledge distillation for lightweight model? | Final accuracy achieved | Phase 4+ |
