# AI Photo Editing Course Generator

AI Photo Editing Course Generator is a production-oriented Python project that builds a structured image-editing curriculum automatically.

It generates learning modules and lessons in the format:

**Theory → Example → Editing Breakdown → Exercise → Evaluation**

Each lesson includes:
1. Concept explanation
2. Example original image
3. Target edited image
4. Step-by-step editing instructions
5. An exercise where the student recreates the target edit

---

## Features

- Automatic module and lesson generation
- Curriculum covering beginner to advanced editing concepts
- Exercise bundles with:
  - `original_image.jpg`
  - `target_edit.jpg`
  - `instructions.md`
- Student upload evaluation against a target edit
- Automated scoring and feedback using:
  - SSIM
  - Histogram comparison
  - Color distance

---

## Course Topics

The default curriculum includes:

- exposure and brightness
- highlights and shadows
- contrast and tonal balance
- saturation vs vibrance
- white balance and color correction
- cropping and composition
- subject separation
- sharpening and texture
- advanced color grading
- developing editing style

---

## Tech Stack

- Python 3.11+
- OpenAI API (lesson text generation)
- Pillow + OpenCV + NumPy + scikit-image (image processing and evaluation)
- Typer (CLI)
- Markdown (lesson and instruction output)

---

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Set your API key in `.env`:

```env
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4o-mini
```

---

## CLI Usage

### Generate full course

```bash
python cli/generate_course.py --topic "photo editing"
```

### Generate a single module

```bash
python cli/generate_course.py generate-module --module "module_03_color"
```

### Generate an exercise

```bash
python cli/generate_exercise.py generate-exercise --lesson-id lesson_01 --module module_01_light
```

### Evaluate student edit

```bash
python cli/generate_exercise.py evaluate-edit \
  --student-edit path/to/student_edit.jpg \
  --target-edit path/to/target_edit.jpg
```

---

## Repository Layout

```text
.
├── README.md
├── requirements.txt
├── pyproject.toml
├── .env.example
├── course_engine/
├── datasets/
├── modules/
├── prompts/
├── tools/
└── cli/
```

---

## Typical Workflow

1. Run `generate-course` to scaffold module lessons.
2. Place source/target images in generated lesson folders.
3. Run `generate-exercise` to create student practice bundles.
4. Students submit their edited image.
5. Run `evaluate-edit` to get quantitative metrics and actionable critique.

---

## Notes

- Lesson generation gracefully falls back to template content when no API key is configured.
- Evaluation output is both machine-readable (JSON) and human-readable in CLI output.
