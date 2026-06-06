const chatMessages = document.querySelector("[data-chat-messages]");
const chatForm = document.querySelector("[data-chat-form]");
const chatInput = document.querySelector("[data-chat-input]");
const chatStatus = document.querySelector("[data-chat-status]");
const chatActions = document.querySelector("[data-chat-actions]");
const allowHistory = document.querySelector("[data-allow-history]");
const chatPanel = document.querySelector("[data-chat-panel]");
const profileId = chatPanel ? chatPanel.dataset.profileId : "";
const sendButton = chatForm ? chatForm.querySelector("button[type='submit']") : null;
let chatHistory = [];

function addMessage(role, content) {
    const message = document.createElement("article");
    message.className = `chat-message ${role}`;
    const title = role === "user" ? "You" : "Assistant";
    const heading = document.createElement("strong");
    heading.textContent = title;
    const paragraph = document.createElement("p");
    paragraph.textContent = content;
    message.append(heading, paragraph);
    chatMessages.appendChild(message);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function formatApiFailure(payload, fallback) {
    if (!payload) {
        return fallback;
    }
    if (payload.error === "live_ai_required") {
        return [
            "The AI service is not ready for this answer.",
            "Please restart the Flask server with the configured API key, then reload this page."
        ].join("\n");
    }
    return payload.message || payload.error || fallback;
}

function setChatStatus(text, state) {
    chatStatus.textContent = text;
    chatStatus.dataset.state = state;
}

function showCompletionActions(payload) {
    chatActions.hidden = false;
    chatActions.innerHTML = `
        <a class="button primary" href="${payload.next_url}">View Summary</a>
        <a class="button secondary" href="${payload.care_guidance_url}">Care Guidance</a>
    `;
}

chatForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const message = chatInput.value.trim();
    if (!message) {
        return;
    }
    addMessage("user", message);
    chatInput.value = "";
    setChatStatus("Thinking and checking safety rules...", "loading");
    if (sendButton) {
        sendButton.disabled = true;
    }

    try {
        const response = await fetch("/api/intake-chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                message,
                history: chatHistory,
                allow_model_history: Boolean(allowHistory && allowHistory.checked),
                profile_id: profileId || null,
            }),
        });
        const payload = await response.json();
        if (!response.ok) {
            const apiMessage = formatApiFailure(payload, "Chat request failed.");
            addMessage("assistant", apiMessage);
            throw new Error(apiMessage);
        }
        chatHistory = payload.history || chatHistory;
        addMessage("assistant", payload.assistant_message);
        const sourceLabel = payload.ai_source === "ai_model" ? "APIFree model" : "local safety rule";
        if (payload.complete) {
            chatForm.hidden = true;
            showCompletionActions(payload);
            setChatStatus(payload.safety_triggered ? "Safety notice triggered." : `Intake complete using ${sourceLabel}. Review summary and care guidance.`, payload.safety_triggered ? "warning" : "success");
        } else {
            const state = payload.ai_source === "ai_model" ? "success" : "warning";
            const detail = payload.ai_configured ? "" : " APIFree is not configured, so this is not a live model answer.";
            setChatStatus(`Answer the follow-up question above. Source: ${sourceLabel}.${detail}`, state);
        }
    } catch (error) {
        setChatStatus(error.message, "error");
    } finally {
        if (sendButton) {
            sendButton.disabled = false;
        }
    }
});

chatInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        chatForm.requestSubmit();
    }
});

setChatStatus("Ready. Describe your symptom to start the AI-guided intake.", "success");
