"""CLI for generating full courses and individual modules."""

from __future__ import annotations

from pathlib import Path

import typer

from course_engine.curriculum import build_default_curriculum
from course_engine.generator import CourseGenerator

app = typer.Typer(
    add_completion=False,
    no_args_is_help=False,
    invoke_without_command=True,
    help="Generate AI photo editing courses and modules.",
)


@app.callback()
def default_generate_course(
    ctx: typer.Context,
    topic: str = typer.Option("photo editing", "--topic", help="Course topic or framing theme."),
) -> None:
    """Generate full course when called without an explicit subcommand.

    Example:
        python cli/generate_course.py --topic "photo editing"
    """
    if ctx.invoked_subcommand is not None:
        return
    generator = CourseGenerator(output_root=Path("modules"))
    generated = generator.generate_course(topic)
    typer.echo(f"Generated {len(generated)} lessons for topic: {topic}")


@app.command("generate-course")
def generate_course(topic: str = typer.Option("photo editing", help="Course topic or framing theme.")) -> None:
    """Generate the full course curriculum."""
    generator = CourseGenerator(output_root=Path("modules"))
    generated = generator.generate_course(topic)
    typer.echo(f"Generated {len(generated)} lessons for topic: {topic}")


@app.command("generate-module")
def generate_module(module: str = typer.Option(..., help="Module slug (e.g. module_03_color).")) -> None:
    """Generate a specific module only."""
    curriculum = {m.slug: m for m in build_default_curriculum()}
    if module not in curriculum:
        raise typer.BadParameter(f"Unknown module: {module}")

    generator = CourseGenerator(output_root=Path("modules"))
    generated = generator.generate_module(curriculum[module], topic="photo editing")
    typer.echo(f"Generated module '{module}' with {len(generated)} lesson(s).")


if __name__ == "__main__":
    app()
