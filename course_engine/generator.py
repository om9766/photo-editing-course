"""High-level orchestration for generating course modules and lessons."""

from __future__ import annotations

from pathlib import Path

from course_engine.curriculum import ModuleSpec, build_default_curriculum
from course_engine.exercise_generator import ExerciseGenerator
from course_engine.lesson_builder import LessonBuilder


class CourseGenerator:
    """Main service that writes modules, lesson markdown, and exercises."""

    def __init__(self, output_root: Path = Path("modules")) -> None:
        self.output_root = output_root
        self.lesson_builder = LessonBuilder()
        self.exercise_generator = ExerciseGenerator()

    def generate_course(self, topic: str) -> list[Path]:
        """Generate the default curriculum for a topic."""
        generated_paths: list[Path] = []
        for module in build_default_curriculum():
            generated_paths.extend(self.generate_module(module, topic))
        return generated_paths

    def generate_module(self, module: ModuleSpec, topic: str) -> list[Path]:
        """Generate one module and all lesson directories/files."""
        module_dir = self.output_root / module.slug
        module_dir.mkdir(parents=True, exist_ok=True)

        module_overview = module_dir / "README.md"
        module_overview.write_text(
            f"# {module.name}\n\n"
            f"This module belongs to the **{topic}** course track.\n",
            encoding="utf-8",
        )

        generated: list[Path] = []
        for idx, lesson in enumerate(module.lessons, start=1):
            lesson_dir = module_dir / f"lesson_{idx:02d}"
            lesson_dir.mkdir(parents=True, exist_ok=True)

            content = self.lesson_builder.build(module.name, lesson.title, lesson.objective)
            lesson_md = (
                f"# {lesson.title}\n\n"
                f"**Topic:** {topic}\n"
                f"**Objective:** {lesson.objective}\n\n"
                f"## Theory\n{content.theory}\n\n"
                f"## Example\n{content.example}\n\n"
                f"## Editing Breakdown\n{content.breakdown}\n\n"
                f"## Exercise\n{content.exercise}\n"
            )
            lesson_path = lesson_dir / "lesson.md"
            lesson_path.write_text(lesson_md, encoding="utf-8")

            self.exercise_generator.create_exercise(lesson_dir)
            generated.append(lesson_path)
        return generated
