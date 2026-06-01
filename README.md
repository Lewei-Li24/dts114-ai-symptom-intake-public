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

## Version Plan and Evidence

- `v0.1.0` Initialize coursework structure and notebook generator
- `v0.2.0` Add SDLC documentation and UML evidence
- `v0.3.0` Implement generated Flask website and AI workflows
- `v0.4.0` Add route/API tests and CI workflow
- `v0.4.1` Fix CI workflow scope
- `v0.5.0` Add Docker and deployment configuration
- `v0.6.0` Prepare final coursework evidence package
- `v0.6.1` Clarify UML workflow evidence

## Current Version

`v0.6.1` is the final checked software version. It keeps the submission focused
on the assessed workflow: notebook generation, Flask API and website, generated
image evidence, UML, tests, CI/CD, Docker support, deployment configuration, and
Task 2 evidence files.

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



