"""Generate exercise artifacts for a lesson."""

from __future__ import annotations

from pathlib import Path
from textwrap import dedent

from PIL import Image, ImageDraw


class ExerciseGenerator:
    """Creates exercise assets including placeholder images and instructions."""

    def create_exercise(self, lesson_dir: Path) -> Path:
        """Create required exercise files in the lesson directory."""
        exercise_dir = lesson_dir / "exercise"
        exercise_dir.mkdir(parents=True, exist_ok=True)

        original_path = exercise_dir / "original_image.jpg"
        target_path = exercise_dir / "target_edit.jpg"
        instructions_path = exercise_dir / "instructions.md"

        if not original_path.exists():
            self._make_placeholder_image(original_path, "Original")
        if not target_path.exists():
            self._make_placeholder_image(target_path, "Target Edit", tinted=True)

        instructions_path.write_text(
            dedent(
                """
                # Exercise Instructions

                1. Open `original_image.jpg` in your preferred editor.
                2. Recreate the look of `target_edit.jpg`.
                3. Focus on exposure, contrast, and color harmony.
                4. Export your result as `student_edit.jpg`.
                5. Run the CLI evaluation command to receive feedback.
                """
            ).strip()
            + "\n",
            encoding="utf-8",
        )
        return exercise_dir

    @staticmethod
    def _make_placeholder_image(path: Path, label: str, tinted: bool = False) -> None:
        """Build a simple visual placeholder image."""
        base_color = (180, 180, 180) if not tinted else (180, 155, 135)
        img = Image.new("RGB", (1280, 720), color=base_color)
        draw = ImageDraw.Draw(img)
        draw.rectangle((80, 80, 1200, 640), outline=(240, 240, 240), width=6)
        draw.text((100, 100), label, fill=(255, 255, 255))
        img.save(path, format="JPEG", quality=90)
