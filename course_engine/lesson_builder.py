"""Build lesson markdown using OpenAI with deterministic fallback content."""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(slots=True)
class LessonContent:
    """Generated lesson sections in markdown format."""

    theory: str
    example: str
    breakdown: str
    exercise: str


class LessonBuilder:
    """Builds lesson content from prompts and curriculum metadata."""

    def __init__(self, lesson_prompt_path: str = "prompts/lesson_prompt.txt") -> None:
        load_dotenv()
        self.lesson_prompt_path = lesson_prompt_path
        self.api_key = os.getenv("OPENAI_API_KEY", "").strip()
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    def build(self, module_name: str, lesson_title: str, objective: str) -> LessonContent:
        """Generate lesson content using API or fallback template."""
        prompt_text = self._load_prompt_template()
        if self.api_key:
            return self._build_with_openai(prompt_text, module_name, lesson_title, objective)
        return self._fallback_lesson(module_name, lesson_title, objective)

    def _load_prompt_template(self) -> str:
        if not os.path.exists(self.lesson_prompt_path):
            return "Create a concise practical photo editing lesson."
        with open(self.lesson_prompt_path, "r", encoding="utf-8") as f:
            return f.read().strip()

    def _build_with_openai(self, prompt_text: str, module_name: str, lesson_title: str, objective: str) -> LessonContent:
        from openai import OpenAI

        client = OpenAI(api_key=self.api_key)
        user_prompt = (
            f"{prompt_text}\n\n"
            f"Module: {module_name}\n"
            f"Lesson: {lesson_title}\n"
            f"Objective: {objective}\n\n"
            "Return markdown with headings: Theory, Example, Editing Breakdown, Exercise."
        )
        response = client.responses.create(model=self.model, input=user_prompt)
        text = response.output_text or ""

        def section(name: str) -> str:
            marker = f"## {name}"
            if marker not in text:
                return ""
            chunk = text.split(marker, 1)[1]
            for next_name in ["Theory", "Example", "Editing Breakdown", "Exercise"]:
                next_marker = f"## {next_name}"
                if next_name != name and next_marker in chunk:
                    chunk = chunk.split(next_marker, 1)[0]
            return chunk.strip()

        return LessonContent(
            theory=section("Theory") or "Theory section unavailable.",
            example=section("Example") or "Example section unavailable.",
            breakdown=section("Editing Breakdown") or "Breakdown section unavailable.",
            exercise=section("Exercise") or "Exercise section unavailable.",
        )

    @staticmethod
    def _fallback_lesson(module_name: str, lesson_title: str, objective: str) -> LessonContent:
        return LessonContent(
            theory=f"In **{module_name}**, this lesson covers **{lesson_title}**. Goal: {objective}",
            example=(
                "Analyze the original image and identify regions that need exposure, tonal, "
                "or color adjustments before editing."
            ),
            breakdown=(
                "1. Start with global tonal adjustments.\n"
                "2. Recover highlights and open shadows where needed.\n"
                "3. Refine color and white balance.\n"
                "4. Apply local edits to direct attention to the subject."
            ),
            exercise=(
                "Recreate the target edit from the original image and compare your histogram, "
                "highlight detail, and color harmony against the target."
            ),
        )
