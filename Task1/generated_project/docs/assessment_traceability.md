# Assessment Traceability Matrix

This file maps the software-component marking criteria to concrete project evidence. It is designed for final checking before packaging the coursework.

| Rubric Area | Evidence in This Submission | Verification Action |
| --- | --- | --- |
| Generated documentation | `docs/requirements.md`, `docs/prompt_design.md`, `docs/architecture_decisions.md`, `docs/safety_policy.md` | Open each document and confirm it matches the symptom-intake business problem. |
| Website with generated image | `templates/index.html`, `static/generated_banner.png` | Open `/` and confirm the banner image is visible. |
| Coherent notebook and project structure | `Task1/notebook.ipynb`, `Task1/notebook_outline.md`, `generated_project/` | Confirm Task 1 contains only one notebook and generated outputs are organized by type. |
| UML generation | `docs/use_case.puml`, `docs/class_diagram.puml`, `docs/activity_diagram.puml`, `docs/uml_png/` | Confirm PlantUML source and rendered PNG evidence exist. |
| AI-specific tooling | APIFree setup in `app.py`, `scripts/start_apifree.bat`, `docs/apifree_runtime_setup_zh.md`, `docs/prompt_design.md` | Start with APIFree key and test `/api/ai/test`; verify chat source is `ai_model`. |
| Version control evidence | GitHub repository link in `Task2/repo_link.txt`; screenshot target `Task2/screenshots/commits.png` | Capture real commit-history screenshot from GitHub. |
| CI/CD evidence | `.github/workflows/ci.yml`, `Task2/workflow/ci.yml`, screenshot target `Task2/screenshots/cicd.png` | Push to GitHub and capture successful Actions workflow. |
| Testing practices | `tests/test_api.py`, `tests/test_routes.py` | Run `pytest -q`; current local result should pass all tests. |
| Deployment evidence | `render.yaml`, `Task2/deployment_notes.md`, screenshot target `Task2/screenshots/deployment.png` | Deploy on Render and capture live web page or service screenshot. |

## Safety and Academic Integrity Checks

- No `.env`, API key, database file, log file, cache, or Python bytecode should be included in the final zip.
- Use anonymous demonstration data only.
- The project documents AI as an assistant for generating software artifacts, not as a ghostwriter for the separate handwritten report.
- Medication output remains non-prescriptive: no exact dose, schedule, or prescription instruction is generated.
