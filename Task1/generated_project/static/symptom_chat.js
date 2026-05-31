const chatMessages = document.querySelector("[data-chat-messages]");
const chatForm = document.querySelector("[data-chat-form]");
const chatInput = document.querySelector("[data-chat-input]");
const chatStatus = document.querySelector("[data-chat-status]");
const chatActions = document.querySelector("[data-chat-actions]");
const allowHistory = document.querySelector("[data-allow-history]");
const chatPanel = document.querySelector("[data-chat-panel]");
const aiProviderPanel = document.querySelector("[data-ai-provider-panel]");
const aiHealthSummary = document.querySelector("[data-ai-health-summary]");
const aiHealthDetail = document.querySelector("[data-ai-health-detail]");
const aiTestButton = document.querySelector("[data-ai-test-button]");
const aiTestResult = document.querySelector("[data-ai-test-result]");
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
            payload.message || "Live APIFree is required for this answer.",
            `Current model: ${payload.ai_model || "not configured"}`,
            `Last error: ${payload.ai_last_error || "not available"}`,
            "Restart the server with scripts/start_apifree.bat, paste a valid APIFree key, then reload this page."
        ].join("\n");
    }
    return payload.message || payload.error || fallback;
}

function setChatStatus(text, state) {
    chatStatus.textContent = text;
    chatStatus.dataset.state = state;
}

async function refreshAiHealth() {
    if (!aiHealthSummary || !aiHealthDetail) {
        return;
    }
    try {
        const response = await fetch("/api/health");
        const health = await response.json();
        const apifreeReady = health.ai_provider === "APIFree" && health.ai_configured && !health.ai_last_error;
        aiProviderPanel.classList.toggle("warning", !apifreeReady);
        aiProviderPanel.classList.toggle("connected", apifreeReady);
        if (apifreeReady) {
            aiHealthSummary.textContent = "APIFree model ready";
            aiHealthDetail.textContent = `Live model: ${health.ai_model} via ${health.ai_base_url}`;
            setChatStatus("APIFree is configured. Use Test APIFree before the demo, then start chatting.", "success");
        } else if (health.ai_configured) {
            aiHealthSummary.textContent = "APIFree needs testing";
            aiHealthDetail.textContent = `Configured model: ${health.ai_model}. Last error: ${health.ai_last_error || "not tested yet"}`;
            setChatStatus("The app will require a live APIFree response. Click Test APIFree to confirm the key/model.", "warning");
        } else {
            aiHealthSummary.textContent = "APIFree key not configured";
            aiHealthDetail.textContent = "Restart with scripts/start_apifree.ps1 and paste your APIFree key to enable live model answers.";
            setChatStatus("APIFree is not connected. AI chat will ask you to configure the key instead of using fixed fallback text.", "warning");
        }
    } catch (error) {
        setChatStatus("Could not check AI connection. Make sure Flask is running.", "error");
    }
}

async function testAiConnection() {
    if (!aiTestButton || !aiTestResult) {
        return;
    }
    aiTestButton.disabled = true;
    aiTestResult.textContent = "Testing live model...";
    try {
        const response = await fetch("/api/ai/test", { method: "POST" });
        const payload = await response.json();
        if (!response.ok || payload.ok === false) {
            throw new Error(payload.message || payload.error || "Model test failed.");
        }
        aiTestResult.textContent = `Connected: ${payload.provider} / ${payload.model}`;
        setChatStatus("APIFree model test passed. New chat answers will use the live model.", "success");
        await refreshAiHealth();
    } catch (error) {
        aiTestResult.textContent = error.message;
        setChatStatus("APIFree test failed. Check that the server was started with APIFREE_API_KEY.", "error");
    } finally {
        aiTestButton.disabled = false;
    }
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

if (aiTestButton) {
    aiTestButton.addEventListener("click", testAiConnection);
}

refreshAiHealth();
