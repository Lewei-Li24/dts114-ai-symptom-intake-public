# Version Control and CI/CD Evidence Notes

## Version Control Strategy

The public GitHub repository uses staged commits to show incremental software
development rather than a single final upload. The commit sequence is:

1. `v0.1.0 initialize coursework structure and notebook generator`
2. `v0.2.0 add SDLC documentation and UML evidence`
3. `v0.3.0 implement generated Flask website and AI workflows`
4. `v0.4.0 add route API tests and CI workflow`
5. `v0.4.1 fix CI workflow scope`
6. `v0.5.0 add Docker and deployment configuration`
7. `v0.6.0 prepare final coursework evidence package`
8. `v0.6.1 clarify UML workflow evidence`

This sequence maps to the assessed workflow: inception and documentation,
construction of the generated Flask system, testing and CI, Docker/deployment
configuration, and final evidence preparation.

## CI/CD Strategy

GitHub Actions runs on pushes and pull requests to `main` or `master`.

The workflow contains two jobs:

- `build-and-test`: installs dependencies, checks Python syntax, runs pytest,
  and confirms Docker configuration files are present.
- `deploy-check`: imports the Flask app as a deployment smoke test after
  `build-and-test` passes.

The successful workflow page should be captured as `Task2/screenshots/cicd.png`.

## Evidence Pages to Screenshot

- Commit history: `https://github.com/Lewei-Li24/dts114-ai-symptom-intake-public/commits/main`
- CI/CD workflow: `https://github.com/Lewei-Li24/dts114-ai-symptom-intake-public/actions`
- Deployment evidence: Render service page or deployed live website URL
