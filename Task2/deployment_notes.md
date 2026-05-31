# Deployment Notes

## Repository

- Repository URL: `https://github.com/Lewei-Li24/dts114-ai-symptom-intake-public`
- Main branch: `main`

## Platform

- Deployment platform: Render
- Service type: Web Service
- Runtime: Python
- Root directory: `Task1/generated_project`
- Live URL: add the Render URL after deployment and before final packaging

## Build and Start Commands

```bash
pip install -r requirements.txt
```

```bash
gunicorn app:app
```

## Docker Deployment Option

The repository also includes a root-level `Dockerfile` and `docker-compose.yml`
for container-based execution.

```bash
docker build -t ai-symptom-intake .
docker run --rm -p 5000:5000 ai-symptom-intake
```

For live AI output, pass `APIFREE_API_KEY` as an environment variable instead of
committing it to the repository.

## Docker Verification

The Docker configuration was checked locally with:

```bash
docker build -t ai-symptom-intake .
docker run -d --rm --name ai-symptom-intake-check -p 5050:5000 ai-symptom-intake
curl http://127.0.0.1:5050/api/health
docker stop ai-symptom-intake-check
```

The health check returned `status: ok`, confirming that the generated Flask
application can start inside the container.

## Environment Variables

- `SECRET_KEY`: set in deployment platform
- `DATABASE_PATH`: optional SQLite database file path; defaults to `symptom_triage.db` if omitted
- `APIFREE_API_KEY`: APIFree model key for live model-backed chat, care guidance, and report structuring
- `APIFREE_BASE_URL`: optional OpenAI-compatible base URL, defaults to `https://api.apifree.ai/v1`
- `APIFREE_MODEL`: optional model name, defaults to `deepseek-ai/deepseek-v4-flash`

## Post-deployment Verification

| Check | Expected Result | Actual Result |
| --- | --- | --- |
| `/` | HTTP 200 and homepage loads with generated banner | To be confirmed from the live Render URL |
| `/api/health` | HTTP 200 and service status JSON returns | To be confirmed from the live Render URL |

## Known Limitations

- The coursework prototype does not include login or role-based access control.
- SQLite is appropriate for this prototype but should be replaced for larger production use.
- This system is not a diagnosis tool and does not provide prescriptions.
- Saved profile, health-record, and location data are local prototype data and should use anonymous demo content only.
- APIFree student accounts may have low concurrency; the app queues model requests and retries provider concurrency errors, but the demo should avoid repeated rapid clicks.

