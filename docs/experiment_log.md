# Experiment Log — All Training Runs

> **Format**: Append new runs at the BOTTOM. Never edit past entries.  
> **Purpose**: Complete audit trail for all experiments.  
> **Rule**: Every training run gets an entry, even failed ones.

---

## Template

```
---
### RUN-[ID]: [Short Description]

**Date**: YYYY-MM-DD  
**Branch**: feature/[name]  
**Config file**: configs/[filename].yaml  
**Git commit**: [hash]

**Hypothesis**: Why we ran this experiment.

**Setup**:
- Model: [name]
- Backbone: [name]
- Dataset: [train split]
- Epochs: [n] / Actual: [n]
- Batch size: [n]
- Input size: [HxW]
- Learning rate: [value]
- Loss: [formula]
- GPU: [model]
- Training time: [hours]

**Checkpoint**: checkpoints/[filename].pt  (git-ignored, path logged here)

**Results** (computed from actual evaluation):
| Dataset | Dice | IoU | F-meas | FPS |
|---------|------|-----|--------|-----|
| [dataset] | — | — | — | — |

**Observations**:
- [what happened during training]
- [loss curve behavior]
- [notable findings]

**Conclusion**: [pass/fail/informative — and why]

**Next action**: [what experiment to run next]
```

---

## Experiments

*(No experiments yet — Phase 0 in progress)*

---

## Summary Table (Updated After Each Run)

| Run ID | Date | Model | Kvasir Dice | ETIS Dice | FPS | Notes |
|--------|------|-------|------------|-----------|-----|-------|
| — | — | — | — | — | — | Phase 0 complete, awaiting Phase 1 |

---

*All metrics in this log are computed from real evaluation on real validation data. No estimated or fabricated values.*
