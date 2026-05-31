import pytest

import app as app_module


def fake_call_model_json(prompt, system_prompt=None, required=False):
    if "care guidance" in prompt and "medication_reference" in prompt:
        return {
            "self_care": ["Rest and track symptoms."],
            "clinician_discussion": ["Ask a clinician if symptoms persist."],
            "medication_discussion": ["Discuss suitable non-prescription options with a pharmacist."],
            "monitoring": ["Track severity and new symptoms."],
            "visit_preparation": ["Bring symptom notes and medicine/allergy history."],
            "avoid": ["Avoid prescription-only medicines without clinician advice."],
            "medication_reference": [
                {
                    "option": "Clinician/pharmacist discussion option",
                    "purpose": "Symptom relief discussion",
                    "suitability": "Depends on age, allergies, pregnancy, conditions, and current medicines.",
                    "dose_boundary": app_module.DOSE_BOUNDARY_TEXT,
                    "cautions": "Read labels and consult a professional.",
                }
            ],
            "care_plan_table": [
                {
                    "priority": "Now",
                    "action": "Rest, hydrate, and monitor symptom trend.",
                    "why": "A clear timeline helps professional review.",
                    "when_to_seek_help": "Seek help if symptoms worsen or red flags appear.",
                }
            ],
            "safety_note": app_module.DISCLAIMER_TEXT,
        }
    if "symptom intake assistant" in prompt:
        complete = "No allergies or current medicines." in prompt
        return {
            "assistant_message": (
                "I have enough information to create the structured summary."
                if complete
                else "How long has the headache been happening, and did it start suddenly or gradually?"
            ),
            "complete": complete,
            "extracted": {
                "primary_symptom": "headache",
                "duration": "1 day" if complete else "",
                "severity": 4,
                "additional_context": "No fever or breathing issues. No allergies or current medicines.",
                "associated_symptoms": "No fever or breathing issues",
                "medicines_taken": "none",
                "allergies": "none",
                "relevant_history": "not specified",
                "user_concerns": "headache",
            },
            "missing_fields": [] if complete else ["duration"],
        }
    if "structured symptom summary" in prompt:
        return {"summary": "Chief complaint: headache. Duration: 1 day. Severity: 4/10. No red flags reported."}
    if "unified JSON report format" in prompt:
        return {
            "report_title": "AI Structured Health Checkup Report",
            "patient_profile": {
                "name": "not specified",
                "age": "not specified",
                "sex": "not specified",
                "allergies": "not specified",
                "current_medications": "not specified",
                "chronic_conditions": "not specified",
            },
            "checkup_info": {"checkup_date": "not specified", "institution": "not specified", "source_type": "pasted_checkup_text"},
            "vitals": {"height": "not specified", "weight": "not specified", "blood_pressure": "118/76", "heart_rate": "not specified", "bmi": "not specified"},
            "lab_results": [{"item_name": "LDL", "value": "high", "unit": "not specified", "reference_range": "not specified", "status": "abnormal", "note": "LDL high"}],
            "imaging_results": [],
            "abnormal_findings": [{"finding": "LDL high", "possible_meaning": "Needs professional interpretation.", "follow_up_suggestion": "Discuss at routine care."}],
            "summary": "LDL was flagged as high in the pasted checkup text.",
            "suggestions": ["Discuss lipid results with a clinician."],
            "data_quality": {"missing_fields": ["name"], "uncertain_items": []},
            "disclaimer": app_module.DISCLAIMER_TEXT,
        }
    if "PlantUML" in prompt:
        return {
            "diagram_type": "activity",
            "title": "AI Symptom Intake Activity Diagram",
            "plantuml": "@startuml\nstart\n:Enter symptoms;\n:Run safety checks;\n:Generate AI follow-up;\nstop\n@enduml",
            "explanation": "Shows safety validation before AI guidance.",
        }
    return {"ok": True}


@pytest.fixture()
def fake_ai(monkeypatch):
    monkeypatch.setattr(app_module, "call_model_json", fake_call_model_json)


def test_health_endpoint(client):
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"
    assert response.get_json()["ai_configured"] is False


def test_ai_models_requires_key(client):
    response = client.get("/api/ai/models")

    assert response.status_code == 400
    assert response.get_json()["error"] == "missing_api_key"


def test_ai_test_requires_key(client):
    response = client.post("/api/ai/test")

    assert response.status_code == 400
    assert response.get_json()["error"] == "missing_api_key"


def test_ai_chat_requires_live_apifree_when_no_generator(client):
    response = client.post("/api/intake-chat", json={"message": "I have a headache.", "history": []})

    assert response.status_code == 503
    assert response.get_json()["error"] == "live_ai_required"


def test_create_symptom_session_returns_followup_questions(client):
    response = client.post(
        "/api/symptoms",
        json={
            "primary_symptom": "headache",
            "duration": "2 days",
            "severity": 4,
            "additional_context": "No emergency symptoms reported.",
        },
    )

    assert response.status_code == 201
    payload = response.get_json()
    assert payload["session_id"] > 0
    assert payload["safety_triggered"] is False
    assert len(payload["questions"]) >= 3


def test_empty_symptom_input_returns_400(client):
    response = client.post("/api/symptoms", json={"duration": "today"})

    assert response.status_code == 400
    assert "primary_symptom" in response.get_json()["fields"]


def test_safety_rule_triggers_urgent_guidance(client):
    response = client.post(
        "/api/symptoms",
        json={
            "primary_symptom": "chest pain and trouble breathing",
            "duration": "10 minutes",
            "severity": 8,
            "additional_context": "Sudden onset",
        },
    )

    assert response.status_code == 201
    payload = response.get_json()
    assert payload["safety_triggered"] is True
    assert payload["triage_level"] == "urgent"
    assert "breathing" in payload["red_flags"]


def test_negated_red_flag_does_not_trigger(client):
    response = client.post(
        "/api/symptoms",
        json={
            "primary_symptom": "headache",
            "duration": "1 day",
            "severity": 4,
            "additional_context": "No chest pain and no trouble breathing.",
        },
    )

    assert response.status_code == 201
    payload = response.get_json()
    assert payload["safety_triggered"] is False


def test_followup_question_endpoint(client):
    response = client.post(
        "/api/followup-questions",
        json={
            "primary_symptom": "cough",
            "duration": "3 days",
            "severity": 3,
        },
    )

    assert response.status_code == 200
    assert len(response.get_json()["questions"]) >= 3


def test_session_followup_alias_endpoint(client):
    create_response = client.post(
        "/api/symptoms",
        json={"primary_symptom": "cough", "duration": "2 days", "severity": 3},
    )
    session_id = create_response.get_json()["session_id"]

    response = client.post(f"/api/sessions/{session_id}/followup")

    assert response.status_code == 200
    assert response.get_json()["session_id"] == session_id
    assert len(response.get_json()["questions"]) >= 3


def test_summary_endpoint(client):
    create_response = client.post(
        "/api/symptoms",
        json={
            "primary_symptom": "stomach pain",
            "duration": "since yesterday",
            "severity": 5,
            "additional_context": "Mild nausea",
        },
    )
    session_id = create_response.get_json()["session_id"]

    summary_response = client.post("/api/summary", json={"session_id": session_id, "answers": []})

    assert summary_response.status_code == 200
    payload = summary_response.get_json()
    assert payload["main_complaint"] == "stomach pain"
    assert payload["disclaimer"]


def test_session_summary_alias_endpoint(client):
    create_response = client.post(
        "/api/symptoms",
        json={"primary_symptom": "headache", "duration": "today", "severity": 4},
    )
    session_id = create_response.get_json()["session_id"]

    summary_response = client.post(f"/api/sessions/{session_id}/summary", json={"answers": []})

    assert summary_response.status_code == 200
    assert summary_response.get_json()["main_complaint"] == "headache"


def test_care_guidance_endpoint_is_non_prescriptive(client):
    create_response = client.post(
        "/api/symptoms",
        json={
            "primary_symptom": "cough",
            "duration": "3 days",
            "severity": 3,
            "additional_context": "No breathing difficulty",
        },
    )
    session_id = create_response.get_json()["session_id"]

    response = client.post("/api/care-guidance", json={"session_id": session_id})

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["medication_discussion"]
    assert payload["medication_reference"]
    assert payload["care_plan_table"]
    assert "Dose not generated" in payload["medication_reference"][0]["dose_boundary"]
    assert "prescription" in " ".join(payload["avoid"]).lower()


def test_session_care_guidance_alias_endpoint(client):
    create_response = client.post(
        "/api/symptoms",
        json={"primary_symptom": "cough", "duration": "3 days", "severity": 3},
    )
    session_id = create_response.get_json()["session_id"]
    client.post(f"/api/sessions/{session_id}/summary", json={"answers": []})

    response = client.post(f"/api/sessions/{session_id}/care-guidance")

    assert response.status_code == 200
    assert response.get_json()["care_plan_table"]


def test_removed_map_endpoints_return_not_found(client):
    assert client.get("/nearby-care").status_code == 404
    assert client.post("/api/nearby-care-links", json={}).status_code == 404
    assert client.post("/api/nearby-care/maps-links", json={}).status_code == 404
    assert client.post("/api/nearby-care/places", json={}).status_code == 404
    assert client.get("/api/saved-location").status_code == 404


def test_uml_generation_requires_live_apifree(client):
    response = client.post(
        "/api/uml/generate",
        json={"diagram_type": "activity", "business_problem": "AI symptom intake website"},
    )

    assert response.status_code == 503
    assert response.get_json()["error"] == "live_ai_required"


def test_uml_generation_endpoint_uses_model(client, fake_ai):
    response = client.post(
        "/api/uml/generate",
        json={"diagram_type": "activity", "business_problem": "AI symptom intake website"},
    )

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["plantuml"].startswith("@startuml")
    assert payload["ai_source"] == "apifree_live"


def test_profile_api_saves_history_consent(client):
    response = client.post(
        "/api/profile",
        json={
            "display_name": "Demo patient",
            "age": "22",
            "allergies": "penicillin",
            "chronic_conditions": "asthma",
            "consent_use_history": "true",
        },
    )

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["display_name"] == "Demo patient"
    assert payload["consent_use_history"] == 1
    assert payload["id"] > 0


def test_profile_context_requires_consent_and_groups_records(app):
    with app.app_context():
        blocked_id = app_module.save_profile({"display_name": "No consent"})
        blocked = app_module.build_model_profile_context(blocked_id)
        assert blocked["profile_context_allowed"] is False

        allowed_id = app_module.save_profile({"display_name": "Consent user", "consent_use_history": "true"})
        app_module.save_health_record(
            {
                "profile_id": allowed_id,
                "title": "CBC lab",
                "record_type": "lab",
                "structured_content": '{"summary": "normal"}',
            }
        )
        context = app_module.build_model_profile_context(allowed_id)

    assert context["profile_context_allowed"] is True
    assert context["record_categories"]["lab"] == 1
    assert context["categorized_recent_records"]["lab"][0]["title"] == "CBC lab"


def test_health_record_analyze_and_save(client, fake_ai):
    analyze_response = client.post(
        "/api/health-records/analyze",
        json={"source_text": "Blood pressure normal. LDL high. Glucose normal."},
    )

    assert analyze_response.status_code == 200
    structured = analyze_response.get_json()
    assert "abnormal_findings" in structured
    assert structured["report_title"] == "AI Structured Health Checkup Report"
    assert "patient_profile" in structured
    assert "lab_results" in structured
    assert "data_quality" in structured

    save_response = client.post(
        "/api/health-records",
        json={
            "title": "Demo checkup",
            "record_date": "2026-05-10",
            "source_text": "LDL high. Glucose normal.",
        },
    )

    assert save_response.status_code == 201
    assert save_response.get_json()["title"] == "Demo checkup"


def test_profile_checkup_structure_alias_endpoint(client, fake_ai):
    profile_response = client.post("/api/profile", json={"display_name": "Checkup user"})
    profile_id = profile_response.get_json()["id"]

    response = client.post(
        f"/api/profiles/{profile_id}/checkup-structure",
        json={"source_text": "Blood pressure normal. LDL high."},
    )

    assert response.status_code == 200
    assert response.get_json()["profile_id"] == profile_id
    assert "structured_record" in response.get_json()
    assert "checkup_info" in response.get_json()["structured_record"]


def test_intake_chat_asks_followup_question(client, fake_ai):
    response = client.post(
        "/api/intake-chat",
        json={"message": "I have a headache.", "history": [], "allow_model_history": True},
    )

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["complete"] is False
    assert "How long" in payload["assistant_message"]
    assert payload["ai_source"] == "ai_model"
    assert payload["ai_configured"] is False


def test_intake_chat_completes_and_returns_links(client, fake_ai):
    history = []
    for message in [
        "I have a headache.",
        "It has lasted 1 day.",
        "Severity is 4/10.",
        "No fever or breathing issues.",
        "No allergies or current medicines.",
    ]:
        response = client.post("/api/intake-chat", json={"message": message, "history": history})
        assert response.status_code == 200
        payload = response.get_json()
        history = payload["history"]

    assert payload["complete"] is True
    assert payload["session_id"] > 0
    assert payload["care_guidance_url"]


def test_intake_chat_safety_trigger(client):
    response = client.post(
        "/api/intake-chat",
        json={"message": "I have chest pain and trouble breathing.", "history": []},
    )

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["complete"] is True
    assert payload["safety_triggered"] is True
