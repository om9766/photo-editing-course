"""Curriculum primitives and defaults for the AI Photo Editing Course."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass(slots=True)
class LessonSpec:
    """Represents one lesson in a module."""

    title: str
    objective: str


@dataclass(slots=True)
class ModuleSpec:
    """Represents a module with ordered lessons."""

    slug: str
    name: str
    lessons: List[LessonSpec] = field(default_factory=list)


DEFAULT_TOPIC_MAP = {
    "module_01_light": {
        "name": "Light Control",
        "lessons": [
            ("Exposure and Brightness", "Balance overall image brightness without clipping."),
            ("Highlights and Shadows", "Recover detail in bright and dark regions."),
        ],
    },
    "module_02_contrast": {
        "name": "Contrast and Tone",
        "lessons": [
            ("Contrast and Tonal Balance", "Shape midtones and dynamic range."),
            ("Sharpening and Texture", "Improve detail while avoiding artifacts."),
        ],
    },
    "module_03_color": {
        "name": "Color Mastery",
        "lessons": [
            ("Saturation vs Vibrance", "Enhance color selectively and naturally."),
            ("White Balance and Color Correction", "Neutralize casts and correct hues."),
            ("Advanced Color Grading", "Create mood with controlled color palettes."),
            ("Developing Editing Style", "Build consistent visual identity."),
        ],
    },
    "module_04_cropping": {
        "name": "Cropping and Composition",
        "lessons": [
            ("Cropping and Composition", "Use framing to improve visual hierarchy."),
        ],
    },
    "module_05_subject_separation": {
        "name": "Subject Emphasis",
        "lessons": [
            ("Subject Separation", "Guide attention with local light and tone."),
        ],
    },
}


def build_default_curriculum() -> List[ModuleSpec]:
    """Create the default module/lesson structure for the platform."""
    modules: list[ModuleSpec] = []
    for slug, meta in DEFAULT_TOPIC_MAP.items():
        lessons = [LessonSpec(title=title, objective=obj) for title, obj in meta["lessons"]]
        modules.append(ModuleSpec(slug=slug, name=meta["name"], lessons=lessons))
    return modules
