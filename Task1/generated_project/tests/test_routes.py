def test_home_page_loads(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"AI Symptom Intake" in response.data
    assert b"Not diagnosis or prescription" in response.data


def test_symptom_input_page_loads(client):
    response = client.get("/symptom-input")

    assert response.status_code == 200
    assert b"Choose mode" in response.data
    assert b"Quick Intake" in response.data
    assert b"Manage health profiles separately" in response.data
    assert b"Create or Manage Users" not in response.data


def test_symptom_input_chat_mode_loads(client):
    response = client.get("/symptom-input?mode=quick")

    assert response.status_code == 200
    assert b"AI questions" in response.data
    assert b"symptom_chat.js" in response.data
    assert b"APIFree key not configured" in response.data


def test_safety_notice_page_loads(client):
    response = client.get("/safety-notice")

    assert response.status_code == 200
    assert b"does not provide diagnosis" in response.data


def test_admin_page_removed(client):
    response = client.get("/admin")

    assert response.status_code == 404


def test_uml_generator_page_loads(client):
    response = client.get("/uml-generator")

    assert response.status_code == 200
    assert b"UML Generator" in response.data
    assert b"uml_generator.js" in response.data


def test_about_page_loads(client):
    response = client.get("/about")

    assert response.status_code == 200
    assert b"AI Use" in response.data


def test_nearby_care_page_removed(client):
    response = client.get("/nearby-care")

    assert response.status_code == 404


def test_profile_page_loads(client):
    response = client.get("/profile")

    assert response.status_code == 200
    assert b"Health Profiles" in response.data
    assert b"Create Profile" in response.data
    assert b"Go to AI Intake" not in response.data
    assert b"Use for Intake" not in response.data


def test_new_profile_page_loads(client):
    response = client.get("/profile/new")

    assert response.status_code == 200
    assert b"Create New Profile" in response.data
    assert b"profile.js" in response.data


def test_care_guidance_page_loads_after_session(client):
    create_response = client.post(
        "/api/symptoms",
        json={
            "primary_symptom": "headache",
            "duration": "1 day",
            "severity": 4,
        },
    )
    session_id = create_response.get_json()["session_id"]
    client.post("/api/summary", json={"session_id": session_id, "answers": []})

    response = client.get(f"/care-guidance/{session_id}")

    assert response.status_code == 200
    assert b"Non-diagnostic Care Guidance" in response.data
    assert b"AI Medication Reference Table" in response.data
    assert b"AI Solution Plan Table" in response.data
