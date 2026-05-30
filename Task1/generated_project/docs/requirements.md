# Requirements Document

## System Overview

The system is an AI symptom intake and triage-support website. It collects user-entered symptoms, generates follow-up questions, creates a structured summary, and gives non-diagnostic next-step guidance. It is explicitly not a diagnosis, prescription, or doctor-replacement tool.

## Business Objectives

- Provide a structured pre-consultation intake workflow.
- Help users organize symptoms before speaking with a healthcare professional.
- Demonstrate AI-specific tooling through question generation and summary generation.
- Keep medical safety boundaries clear and visible throughout the website.

## Functional Requirements

| ID | Requirement | Priority |
| --- | --- | --- |
| FR1 | Users can enter a main symptom, duration, severity, and context. | Must |
| FR2 | The system can generate follow-up questions from symptom input. | Must |
| FR3 | Users can answer follow-up questions. | Must |
| FR4 | The system can generate a structured symptom summary. | Must |
| FR5 | The system can provide non-diagnostic next-step guidance. | Must |
| FR6 | The system triggers a safety notice for emergency-like keywords or very high severity. | Must |
| FR7 | The website displays a persistent medical disclaimer. | Must |
| FR8 | The homepage displays a generated healthcare intake banner image. | Must |
| FR9 | Users can generate PlantUML diagrams from a business problem through an AI-backed UML API. | Must |
| FR10 | The system can generate non-prescriptive care guidance and visit preparation prompts. | Should |
| FR11 | Users can complete symptom intake through a conversational AI chat flow. | Should |
| FR12 | Users can maintain a local health profile with allergies, medicines, conditions, and history. | Should |
| FR13 | Users can paste checkup or health-record text for AI-assisted JSON structuring. | Should |
| FR14 | Users can choose whether the model may use previous chat turns and saved profile context. | Must |

## Non-functional Requirements

| ID | Requirement |
| --- | --- |
| NFR1 | The app should run locally with standard Python dependencies. |
| NFR2 | Data should persist in SQLite for local and small deployment use. |
| NFR3 | Tests should verify routes, API behavior, and safety-rule behavior. |
| NFR4 | The app should be deployable to a platform such as Render. |
| NFR5 | AI-labelled features should fail visibly when the APIFree provider is unavailable, while local safety rules continue to work without the model. |
| NFR6 | No real patient identifiers, API keys, or private medical records should be stored in the repository. |
| NFR7 | Medication-related output must avoid prescriptions, exact dosing, and individualized drug instructions. |
| NFR8 | Profile and health-record context must be user-controlled and documented as local prototype data. |

## User Stories

- As a user, I want to describe symptoms so I can prepare a clearer summary.
- As a user, I want the system to ask follow-up questions so important context is not missed.
- As a user, I want a structured summary so I can share organized information with a professional.
- As a user, I want to save profile details and recent checkup notes so repeated intake can be more personalized.
- As a user, I want to decide whether model-assisted chat can use my previous answers and saved profile.
- As a developer/student, I want to generate UML from a business problem so the system demonstrates AI-assisted SDLC documentation.

## Constraints

- The system must not diagnose disease or recommend prescriptions.
- The system must display a disclaimer on every page.
- Safety rules must override normal follow-up flow when emergency-like keywords appear.
- The app uses Flask and SQLite to remain simple and reproducible for coursework.

## Assumptions

- Users provide anonymous demonstration symptoms, not real patient records.
- The AI model is used for text generation assistance only.
- Human medical judgement is required for any actual health decision.

## API Summary

| Method | Endpoint | Purpose |
| --- | --- | --- |
| GET | `/api/health` | Service health check |
| POST | `/api/symptoms` | Create symptom intake session |
| POST | `/api/followup-questions` | Generate follow-up questions |
| POST | `/api/summary` | Generate structured symptom summary |
| POST | `/api/care-guidance` | Generate safe non-prescriptive care guidance |
| POST | `/api/intake-chat` | Ask conversational follow-up questions and create a session when enough context is collected |
| GET/POST | `/api/profile` | Read or update the local health profile and history consent |
| POST | `/api/health-records/analyze` | Structure pasted checkup text into JSON |
| POST | `/api/health-records` | Save a local checkup or history record |
| POST | `/api/uml/generate` | Generate PlantUML from a business problem using the AI model API |

## Database Summary

- `user_sessions`: anonymous intake sessions and triage status.
- `symptom_inputs`: initial symptom details and red-flag matches.
- `followup_questions`: generated follow-up questions and user answers.
- `symptom_summaries`: structured summaries, triage level, next steps, and disclaimer.
- `user_profiles`: local demo profile, allergies, medicines, conditions, and consent flag.
- `health_records`: pasted checkup or history records with structured JSON.
- Care guidance is generated at request time from session data and is not stored by default.

## Out of Scope

- Diagnosis, treatment decisions, prescriptions, and disease prediction.
- Emergency dispatch or real-time clinical monitoring.
- User login, identity verification, or storage of real patient records in production systems.
- Integration with electronic health record systems.
- Personalized prescriptions, medication dosing, or drug interaction checking.

## Future Enhancements

- Add multilingual symptom intake.
- Add clinician-reviewed prompt templates.
- Export summaries as PDF.
- Add stricter privacy controls before any real-world use.

## Traceability Between Requirements and Diagrams

| Requirement | UML Evidence |
| --- | --- |
| FR1-FR5 | Activity diagram follows input, follow-up, summary, and guidance flow. |
| FR6-FR7 | Safety policy and activity diagram document safety-rule branching. |
| FR1-FR8 | Class diagram maps sessions, symptom input, follow-up questions, summaries, profiles, and safety rules. |
| FR9 | Use case and sequence diagrams show the UML generation API path through Flask and APIFree. |
| FR10-FR11 | Care guidance and chat intake API tests verify the conversational workflow. |
| FR12-FR14 | Profile, health-record, and consent tests verify personalization controls. |

