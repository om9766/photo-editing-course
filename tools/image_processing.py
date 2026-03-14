"""Image utility functions for loading, normalization, and metrics."""

from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np


def load_image(path: str | Path, size: tuple[int, int] | None = (1024, 1024)) -> np.ndarray:
    """Load image in RGB format and optionally resize for consistent comparisons."""
    img = cv2.imread(str(path), cv2.IMREAD_COLOR)
    if img is None:
        raise FileNotFoundError(f"Could not read image: {path}")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    if size:
        img = cv2.resize(img, size, interpolation=cv2.INTER_AREA)
    return img


def compute_histogram_similarity(img_a: np.ndarray, img_b: np.ndarray) -> float:
    """Compare normalized HSV histograms; returns 0..1 where 1 is most similar."""
    hsv_a = cv2.cvtColor(img_a, cv2.COLOR_RGB2HSV)
    hsv_b = cv2.cvtColor(img_b, cv2.COLOR_RGB2HSV)

    hist_a = cv2.calcHist([hsv_a], [0, 1], None, [50, 60], [0, 180, 0, 256])
    hist_b = cv2.calcHist([hsv_b], [0, 1], None, [50, 60], [0, 180, 0, 256])

    hist_a = cv2.normalize(hist_a, hist_a).flatten()
    hist_b = cv2.normalize(hist_b, hist_b).flatten()
    score = cv2.compareHist(hist_a, hist_b, cv2.HISTCMP_CORREL)

    return float(max(0.0, min(1.0, (score + 1) / 2)))


def mean_lab_color_distance(img_a: np.ndarray, img_b: np.ndarray) -> float:
    """Compute mean Euclidean distance in LAB color space."""
    lab_a = cv2.cvtColor(img_a, cv2.COLOR_RGB2LAB).astype(np.float32)
    lab_b = cv2.cvtColor(img_b, cv2.COLOR_RGB2LAB).astype(np.float32)
    delta = np.linalg.norm(lab_a - lab_b, axis=2)
    return float(np.mean(delta))
