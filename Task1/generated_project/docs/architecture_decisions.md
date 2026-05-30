# Architecture Decisions

## ADR 1: Use Flask for the Web Layer

Flask was selected because it is lightweight, readable, and appropriate for a coursework prototype. It supports HTML routes and JSON API routes without a large framework structure.

## ADR 2: Use SQLite for Persistence

SQLite keeps the project reproducible because it does not require a separate database server. It is sufficient for storing anonymous demonstration intake sessions.

## ADR 3: Build Symptom Intake Instead of Diagnosis

The system is scoped as symptom intake and triage support, not diagnosis. This safer boundary keeps the project realistic for healthcare software while avoiding claims that should only be made by professionals.

## ADR 4: Add a Rule-based Safety Layer

The app checks for emergency-like keywords and very high severity before normal AI follow-up generation. This deterministic layer prevents the model workflow from hiding important safety warnings.

## ADR 5: Use AI for Follow-up Questions and Summaries

Large-model use is focused on bounded generation tasks: follow-up question generation and structured summary drafting. The output is always framed as non-diagnostic and is paired with a disclaimer.

## ADR 6: Store Personalization Data Locally

Profile details and health-record imports are stored in SQLite for a reproducible coursework prototype. The project does not include login or production privacy controls, so the intended data is anonymous demonstration data only.

## ADR 7: Make History Context Opt-in

The chat page has a separate history/profile toggle. This keeps the model prompt small by default and makes it clear when saved profile details or recent records are allowed to influence follow-up questions.

## ADR 8: Remove Map and Image-recognition Scope

Map search, browser location storage, and image-recognition/report-image generation were removed to keep the project focused on the assessed AI text workflow: symptom intake, follow-up questions, structured summaries, care guidance, profile consent, and pasted checkup-text structuring.
