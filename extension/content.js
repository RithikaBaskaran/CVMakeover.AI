function getJobText() {
    // Simple + robust hackathon approach:
    // Grab visible text and cap to avoid huge payloads.
    const text = document.body ? document.body.innerText : "";
    return text.replace(/\s+/g, " ").trim().slice(0, 12000);
}

chrome.runtime.onMessage.addListener((req, sender, sendResponse) => {
    if (req.type === "GET_JD_TEXT") {
        sendResponse({ jdText: getJobText() });
    }
});
