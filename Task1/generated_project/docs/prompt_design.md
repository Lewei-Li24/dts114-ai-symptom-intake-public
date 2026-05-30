# Prompt Design Record

## Prompt Goal

Use AI as a generation engine for a safe symptom intake workflow: requirements, UML, Flask backend, frontend pages, tests, follow-up question prompts, structured summary prompts, and homepage image prompt.

## Runtime Prompt Template

```text
You support a non-diagnostic symptom intake workflow.
Return valid JSON only.
Never provide diagnosis, prescriptions, or certainty claims.
Given the symptom input, generate concise follow-up questions or a structured summary.
Always keep wording suitable for sharing with a healthcare professional.
```

## Care Guidance Prompt Template

```text
Create safe, non-diagnostic care guidance for a symptom-intake website.
Return JSON with keys: self_care, clinician_discussion, medication_discussion,
monitoring, visit_preparation, avoid, safety_note.
Do not diagnose. Do not prescribe. Do not give exact drug doses.
Medication discussion must be phrased as questions to ask a licensed clinician or pharmacist.
```

## Conversational Intake Prompt Template

```text
You are a safe AI symptom intake assistant.
Ask one concise follow-up question at a time until enough context is collected.
Return JSON with assistant_message, complete, and extracted fields.
Do not diagnose, prescribe, give exact medication doses, or claim certainty.
Ask about duration, severity, associated symptoms, current medicines, allergies,
pregnancy if relevant, and existing conditions before completing.
```

## Personalization Prompt Template

```text
Use saved profile and recent health records only when the user has enabled history/context consent.
Treat profile data as background context, not proof of a diagnosis.
Ask clarifying questions when allergies, current medicines, chronic conditions, or abnormal checkup findings may matter.
Do not prescribe, change medicine, or give exact doses.
```

## Health Record Structuring Prompt Template

```text
Structure this user-provided checkup or health record text as JSON.
Return keys: title, record_date, abnormal_findings, normal_findings, medicines_mentioned,
conditions_mentioned, follow_up_questions, safety_note.
Do not diagnose or prescribe.
Keep uncertain fields as "not specified".
```

## Why This Prompt Works

- It limits the model to intake support rather than diagnosis.
- It requires JSON so the Flask app can parse outputs reliably.
- It makes safety constraints explicit in every model call.
- It keeps model output short and structured for a web form.
- It keeps medication-related content in a professional-discussion format instead of an instruction format.
- It separates profile consent from the chat flow so the user controls whether saved context is sent to the model.

## Output Validation Rules

- Follow-up generation must return a `questions` array.
- Summary generation must return a `summary` field.
- The app must fall back to deterministic text if the provider fails.
- The safety-rule layer must run independently from the AI model.
- Care guidance must avoid exact dosing, prescription instructions, or personalized medication commands.
- Chat intake must create a session only after enough context is collected or when a safety trigger requires urgent guidance.
- Health-record structuring must return JSON and must describe uncertain or missing fields as not specified.
- Saved profile and record context may be included in model prompts only when the consent toggle is enabled.

## Common Failure Cases

- Model returns prose instead of JSON.
- Model gives diagnostic language.
- Model provider is unavailable.
- User enters emergency-like symptoms that should not enter ordinary follow-up flow.

## Image Prompt

The homepage banner prompt requested a clean healthcare intake interface, symptom questionnaire cards, a calm clinic reception setting, and privacy-conscious non-identifiable silhouettes. It avoided diagnosis labels, prescriptions, logos, and identifiable faces.
