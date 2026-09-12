"""
dataset.py — Polyp Segmentation Dataset Loader

STRICT RULES:
  - No mock data. If a file is missing, raise FileNotFoundError.
  - Images loaded from REAL disk paths.
  - Masks loaded alongside images with existence check.

Supports: Kvasir-SEG, CVC-ClinicDB, CVC-ColonDB, ETIS-LaribPolypDB, CVC-300
"""

import os
from pathlib import Path
from typing import List, Optional, Tuple, Callable

import numpy as np
from PIL import Image
import torch
from torch.utils.data import Dataset


class PolypDataset(Dataset):
    """
    Dataset class for polyp segmentation.
    
    Loads image-mask pairs from a text file listing paths.
    Each line in the list file: <image_path> <mask_path>
    
    Args:
        list_file: Path to text file with image/mask paths
        data_root: Root directory prepended to paths in list_file
        transform: Transform applied to both image and mask
        img_size: Resize all images to this (H, W)
    
    Raises:
        FileNotFoundError: If list_file or any image/mask doesn't exist
    """
    
    def __init__(
        self,
        list_file: str,
        data_root: str,
        transform: Optional[Callable] = None,
        img_size: Tuple[int, int] = (352, 352),
    ):
        self.data_root = Path(data_root)
        self.transform = transform
        self.img_size = img_size
        
        # Validate list file
        list_file = Path(list_file)
        if not list_file.exists():
            raise FileNotFoundError(
                f"Dataset list file not found: {list_file}\n"
                f"Run src/data_loaders/generate_splits.py to create split files."
            )
        
        # Parse image-mask pairs
        self.samples: List[Tuple[Path, Path]] = []
        with open(list_file, "r") as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = line.split()
                if len(parts) != 2:
                    raise ValueError(
                        f"Invalid format at line {line_num} in {list_file}: '{line}'\n"
                        f"Expected: <image_path> <mask_path>"
                    )
                img_path = self.data_root / parts[0]
                mask_path = self.data_root / parts[1]
                self.samples.append((img_path, mask_path))
        
        if len(self.samples) == 0:
            raise ValueError(f"No valid samples found in {list_file}")
        
        # STRICT: Verify all files exist at init time
        self._verify_files()
    
    def _verify_files(self) -> None:
        """Verify all image and mask files exist. Fail explicitly if not."""
        missing = []
        for img_path, mask_path in self.samples:
            if not img_path.exists():
                missing.append(f"Image: {img_path}")
            if not mask_path.exists():
                missing.append(f"Mask: {mask_path}")
        
        if missing:
            missing_str = "\n  ".join(missing[:10])  # Show first 10
            if len(missing) > 10:
                missing_str += f"\n  ... and {len(missing) - 10} more"
            raise FileNotFoundError(
                f"Missing {len(missing)} file(s):\n  {missing_str}\n"
                f"Please check data/README.md for download instructions."
            )
    
    def __len__(self) -> int:
        return len(self.samples)
    
    def __getitem__(self, idx: int) -> dict:
        img_path, mask_path = self.samples[idx]
        
        # Load image
        image = Image.open(img_path).convert("RGB")
        
        # Load mask — must be binary (0 or 255)
        mask = Image.open(mask_path).convert("L")
        
        # Resize to standard size
        image = image.resize(self.img_size, Image.BILINEAR)
        mask = mask.resize(self.img_size, Image.NEAREST)
        
        # Convert to numpy
        image_np = np.array(image, dtype=np.float32) / 255.0
        mask_np = np.array(mask, dtype=np.float32)
        
        # Binarize mask: threshold at 128
        mask_np = (mask_np >= 128).astype(np.float32)
        
        # Apply transforms
        if self.transform is not None:
            transformed = self.transform(image=image_np, mask=mask_np)
            image_np = transformed["image"]
            mask_np = transformed["mask"]
        
        # Convert to tensors: HWC -> CHW
        if isinstance(image_np, np.ndarray):
            image_tensor = torch.from_numpy(image_np.transpose(2, 0, 1))
        else:
            image_tensor = image_np  # Already tensor (from albumentations)
        
        if isinstance(mask_np, np.ndarray):
            mask_tensor = torch.from_numpy(mask_np).unsqueeze(0)
        else:
            mask_tensor = mask_np.unsqueeze(0)
        
        return {
            "image": image_tensor,          # (3, H, W) float32 in [0, 1]
            "mask": mask_tensor,            # (1, H, W) float32 in {0, 1}
            "image_path": str(img_path),
            "mask_path": str(mask_path),
        }
