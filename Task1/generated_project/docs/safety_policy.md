# Safety Policy

## Safety Boundary

This project is a symptom intake and triage-support website. It is not a diagnosis tool, does not replace a doctor, and does not provide prescriptions.

## Safety Rules

The app checks initial symptom text and severity before generating ordinary follow-up questions. If emergency-like terms appear, the app redirects to a safety notice.

Example safety triggers:

- chest pain or chest pressure
- trouble breathing or severe shortness of breath
- sudden weakness, numbness, facial droop, or speech difficulty
- confusion, fainting, or inability to wake
- uncontrolled bleeding
- self-harm language
- blue lips or blue/gray skin
- very high severity score

## AI Guardrails

- The model prompt forbids diagnosis and prescriptions.
- The care-guidance prompt forbids exact drug doses, prescription instructions, antibiotics recommendations, and personalized medication choices.
- The app requests JSON-only output for predictable parsing.
- Provider failures fall back to deterministic local logic.
- A persistent disclaimer appears on all pages.

## Medication Boundary

The website may suggest general self-care and questions to ask a clinician or pharmacist. It must not tell a user to take a specific medicine, change a dose, stop prescribed treatment, combine medicines, or use someone else's prescription.

## Conversation Boundary

The conversational intake feature is designed to gather context, not to diagnose. It asks follow-up questions and then generates a structured summary and care guidance. Safety-rule triggers interrupt the normal chat flow and redirect to urgent guidance.

## Privacy Boundary

The coursework project should use anonymous demonstration inputs only. Real patient identifiers, medical record numbers, phone numbers, and private records should not be submitted to model providers or stored in the repository.

## Personalization Boundary

Profile details and pasted checkup records are for local demonstration only. The model may use previous chat turns and saved profile context only when the user enables the history/context option. The app must not treat profile or checkup text as a confirmed diagnosis.
