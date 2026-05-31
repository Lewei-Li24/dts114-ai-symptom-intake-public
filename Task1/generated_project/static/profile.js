const analyzeRecordButton = document.querySelector("[data-analyze-record]");
const sourceText = document.querySelector("[data-record-source]");
const preview = document.querySelector("[data-record-preview]");
const profileForm = document.querySelector("[data-profile-form]");
const demoButton = document.querySelector("[data-load-demo-profile]");
let latestStructuredRecord = null;

function apiErrorMessage(payload, fallback) {
    if (!payload) {
        return fallback;
    }
    const details = payload.ai_last_error ? ` Last error: ${payload.ai_last_error}` : "";
    return `${payload.message || payload.error || fallback}${details}`;
}

function collectProfilePayload() {
    const payload = {};
    new FormData(profileForm).forEach((value, key) => {
        payload[key] = value;
    });
    const profileId = document.querySelector("[data-profile-id]");
    if (profileId) {
        payload.profile_id = profileId.value;
    }
    if (latestStructuredRecord) {
        payload.structured_checkup_report = latestStructuredRecord;
    }
    payload.consent_use_history = profileForm.querySelector("[name='consent_use_history']")?.checked || false;
    return payload;
}

analyzeRecordButton.addEventListener("click", async () => {
    const text = sourceText.value.trim();
    if (!text) {
        preview.textContent = "Paste checkup text first.";
        return;
    }
    preview.textContent = "Structuring record...";
    const profileId = document.querySelector("[data-profile-id]")?.value;
    const endpoint = profileId ? `/api/profiles/${profileId}/checkup-structure` : "/api/health-records/analyze";
    const response = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ source_text: text }),
    });
    const payload = await response.json();
    if (!response.ok) {
        latestStructuredRecord = null;
        preview.textContent = apiErrorMessage(payload, "AI record structuring failed.");
        return;
    }
    latestStructuredRecord = payload.structured_record || payload;
    preview.textContent = JSON.stringify(latestStructuredRecord, null, 2);
});

demoButton.addEventListener("click", () => {
    const demo = {
        display_name: "Demo Patient A",
        age: "29",
        sex: "Female",
        height_cm: "165",
        weight_kg: "58",
        emergency_contact: "Demo contact",
        allergies: "No known drug allergies",
        current_medications: "Occasional OTC pain relief, not taken today",
        chronic_conditions: "Migraine history",
        past_history: "No recent surgery. Previous migraine episodes during exam stress.",
        family_history: "Family history of hypertension",
        source_text: "Annual checkup 2026-05-10. Blood pressure 118/76 normal. LDL mildly high. Glucose normal. Vitamin D low.",
        record_title: "Demo annual checkup",
    };
    Object.entries(demo).forEach(([name, value]) => {
        const field = profileForm.querySelector(`[name="${name}"]`);
        if (field) {
            field.value = value;
        }
    });
    const consent = profileForm.querySelector("[name='consent_use_history']");
    if (consent) {
        consent.checked = true;
    }
    preview.textContent = "Demo profile loaded. You can save it or run Auto-structure Preview on the pasted checkup text.";
});
