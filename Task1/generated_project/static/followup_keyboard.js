const followupForm = document.querySelector("[data-followup-form]");

document.querySelectorAll("[data-followup-answer]").forEach((field) => {
    field.addEventListener("keydown", (event) => {
        if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault();
            followupForm.requestSubmit();
        }
    });
});
