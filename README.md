# AI Symptom Intake and Triage Support

This repository is the staged development record for a DTS114 software component.
The project will become a notebook-driven AI software generator that produces a
Flask symptom intake and triage support website.

## Project Scope

The system is designed to support:

- symptom intake and follow-up question collection
- structured symptom summaries
- UML Generator page backed by `/api/uml/generate`
- non-diagnostic care guidance
- health profile and checkup-text structuring
- testing, CI/CD, deployment, and coursework evidence

The system is not a diagnosis tool and does not replace professional medical
advice.

## Version Plan

- `v0.1.0` Project setup
- `v0.2.0` Notebook generator skeleton
- `v0.3.0` SDLC documents and UML
- `v0.4.0` Profile and intake workflow
- `v0.5.0` AI summary, non-diagnostic care guidance, and UML generation API
- `v0.6.0` Testing, CI/CD, deployment, and submission evidence
- `v0.7.0` Docker deployment support

## Current Version

`v0.7.0` adds Docker container configuration so the generated Flask application
can be built and run in a reproducible container environment.

## Docker Run

The project includes a Docker setup so the generated Flask application can run
in a consistent container environment.

Build the image:

```bash
docker build -t ai-symptom-intake .
```

Run the website:

```bash
docker run --rm -p 5000:5000 ^
  -e APIFREE_BASE_URL=https://api.apifree.ai/v1 ^
  -e APIFREE_MODEL=deepseek-ai/deepseek-v4-flash ^
  -e APIFREE_API_KEY=your_apifree_key ^
  ai-symptom-intake
```

Or use Docker Compose:

```bash
set APIFREE_API_KEY=your_apifree_key
docker compose up --build
```

Then open `http://127.0.0.1:5000`.

## Scope Note

Optional map search, saved location, and image-recognition/report-image features were removed from the final software package so the submission focuses on the assessed AI text workflow, generated image evidence, UML, testing, CI/CD, Docker, and deployment.



