"""CLI for exercise generation and student edit evaluation."""

from __future__ import annotations

import json
from pathlib import Path

import typer

from course_engine.exercise_generator import ExerciseGenerator
from tools.evaluation import evaluate_edit

app = typer.Typer(help="Generate exercises and evaluate student edits.")


@app.command("generate-exercise")
def generate_exercise(
    lesson_id: str = typer.Option(..., help="Lesson folder name, e.g. lesson_01."),
    module: str = typer.Option("module_01_light", help="Module slug containing the lesson."),
) -> None:
    """Generate exercise assets in a specific lesson directory."""
    lesson_dir = Path("modules") / module / lesson_id
    lesson_dir.mkdir(parents=True, exist_ok=True)

    exercise_dir = ExerciseGenerator().create_exercise(lesson_dir)
    typer.echo(f"Exercise created at: {exercise_dir}")


@app.command("evaluate-edit")
def evaluate_student_edit(
    student_edit: Path = typer.Option(..., exists=True, dir_okay=False, help="Path to student's JPG/PNG."),
    target_edit: Path = typer.Option(..., exists=True, dir_okay=False, help="Path to target JPG/PNG."),
) -> None:
    """Evaluate student edit and print metrics with recommendations."""
    result = evaluate_edit(str(student_edit), str(target_edit))

    payload = {
        "ssim": round(result.ssim_score, 4),
        "histogram_similarity": round(result.histogram_similarity, 4),
        "color_distance": round(result.color_distance, 4),
        "feedback": result.feedback,
    }
    typer.echo(json.dumps(payload, indent=2))


if __name__ == "__main__":
    app()
