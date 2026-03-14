"""Evaluate student edits against target edits with metrics and feedback."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from skimage.metrics import structural_similarity as ssim

from tools.image_processing import (
    compute_histogram_similarity,
    load_image,
    mean_lab_color_distance,
)


@dataclass(slots=True)
class EvaluationResult:
    """Container for edit quality metrics and textual feedback."""

    ssim_score: float
    histogram_similarity: float
    color_distance: float
    feedback: list[str]


def evaluate_edit(student_edit_path: str, target_edit_path: str) -> EvaluationResult:
    """Run objective image comparisons and infer user-friendly suggestions."""
    student = load_image(student_edit_path)
    target = load_image(target_edit_path)

    student_gray = np.mean(student, axis=2).astype(np.uint8)
    target_gray = np.mean(target, axis=2).astype(np.uint8)

    ssim_score = float(ssim(student_gray, target_gray, data_range=255))
    hist_score = compute_histogram_similarity(student, target)
    color_dist = mean_lab_color_distance(student, target)

    feedback = _generate_feedback(student, target, ssim_score, hist_score, color_dist)
    return EvaluationResult(ssim_score, hist_score, color_dist, feedback)


def _generate_feedback(
    student: np.ndarray,
    target: np.ndarray,
    ssim_score: float,
    hist_score: float,
    color_dist: float,
) -> list[str]:
    """Create critique bullets based on metric thresholds and channel statistics."""
    notes: list[str] = []

    student_lum = float(np.mean(np.mean(student, axis=2)))
    target_lum = float(np.mean(np.mean(target, axis=2)))
    lum_diff = student_lum - target_lum

    student_sat = float(np.mean(np.std(student, axis=2)))
    target_sat = float(np.mean(np.std(target, axis=2)))
    sat_diff = student_sat - target_sat

    if ssim_score < 0.75:
        notes.append("Overall structure differs significantly from the target edit.")
    if hist_score < 0.7:
        notes.append("Tonal distribution is off; revisit contrast and dynamic range.")
    if color_dist > 18:
        notes.append("Color balance is noticeably different; adjust white balance and tint.")

    if lum_diff > 12:
        notes.append("Highlights may be too strong; reduce exposure or highlights.")
    elif lum_diff < -12:
        notes.append("Shadows may be too dark; increase shadow recovery or brightness.")

    if sat_diff > 8:
        notes.append("Saturation appears too high compared to the target.")
    elif sat_diff < -8:
        notes.append("Image appears muted; increase vibrance or selective saturation.")

    if not notes:
        notes.append("Great match. Minor local refinements can improve precision.")

    return notes
