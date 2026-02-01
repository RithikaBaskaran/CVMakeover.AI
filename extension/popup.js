// ==============================
// CVMakeover.AI - popup.js (UPDATED)
// - Upload profile JSON + store locally
// - Load bundled example profile
// - Generate using stored profile + scraped JD
// ==============================

const apiBaseEl = document.getElementById("apiBase");
const generateBtn = document.getElementById("generate");
const downloadBtn = document.getElementById("download");
const statusEl = document.getElementById("status");
const outputEl = document.getElementById("output");

// NEW UI elements (make sure popup.html has these IDs)
const profileFileEl = document.getElementById("profileFile");
const loadExampleBtn = document.getElementById("loadExample");
const profileStatusEl = document.getElementById("profileStatus");

let latestLatex = "";

console.log("✅ popup.js loaded"); // DEBUG

function setStatus(msg) {
    console.log("ℹ️ STATUS:", msg); // DEBUG
    statusEl.textContent = msg;
}

function setProfileStatus(msg) {
    if (!profileStatusEl) return;
    profileStatusEl.textContent = msg;
}

async function getActiveTab() {
    console.log("🔍 Getting active tab"); // DEBUG
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    console.log("✅ Active tab:", tab?.id, tab?.url); // DEBUG
    return tab;
}

function downloadTex(filename, content) {
    console.log("⬇️ Downloading LaTeX file:", filename); // DEBUG
    const blob = new Blob([content], { type: "text/plain" });
    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    a.click();

    URL.revokeObjectURL(url);
}

async function saveProfile(profileObj) {
    await chrome.storage.local.set({ resumeProfile: profileObj });
    setProfileStatus("Profile loaded ✅");
}

async function getSavedProfile() {
    const data = await chrome.storage.local.get(["resumeProfile"]);
    return data.resumeProfile || null;
}

async function loadSettings() {
    console.log("🔍 Loading saved settings"); // DEBUG
    const data = await chrome.storage.local.get(["apiBase", "resumeProfile"]);
    apiBaseEl.value = data.apiBase || "https://localhost:8000/*";
    console.log("✅ apiBase set to:", apiBaseEl.value); // DEBUG

    if (data.resumeProfile) setProfileStatus("Profile loaded ✅");
    else setProfileStatus("No profile loaded");
}

// Save backend URL
apiBaseEl.addEventListener("change", async () => {
    console.log("✏️ Backend URL changed:", apiBaseEl.value); // DEBUG
    await chrome.storage.local.set({ apiBase: apiBaseEl.value.trim() });
});

// Download output
downloadBtn.onclick = () => {
    console.log("⬇️ Download button clicked"); // DEBUG
    downloadTex("CVMakeover_resume.tex", latestLatex);
};

// Upload profile JSON -> store locally
if (profileFileEl) {
    profileFileEl.addEventListener("change", async () => {
        const file = profileFileEl.files?.[0];
        if (!file) return;

        try {
            const text = await file.text();
            const parsed = JSON.parse(text);

            if (!parsed || typeof parsed !== "object") throw new Error("Invalid JSON object");

            // Light validation for sanity (not strict)
            if (!parsed.name) console.warn("Profile missing 'name' (still OK for demo).");
            if (!parsed.skills) console.warn("Profile missing 'skills' (still OK for demo).");

            await saveProfile(parsed);
            setStatus("Profile saved locally ✅");
            console.log("✅ Stored resumeProfile in chrome.storage.local"); // DEBUG
        } catch (e) {
            console.error("❌ Profile upload failed:", e);
            setProfileStatus("Invalid profile JSON ❌");
            setStatus("Error: Could not read profile JSON");
        }
    });
}

// Load bundled example profile (must be inside extension/ as profile.example.json)
if (loadExampleBtn) {
    loadExampleBtn.addEventListener("click", async () => {
        try {
            setStatus("Loading example profile...");
            const url = chrome.runtime.getURL("profile.example.json");
            console.log("📦 Loading example profile from:", url); // DEBUG

            const res = await fetch(url);
            if (!res.ok) throw new Error(`Fetch failed: ${res.status}`);

            const exampleProfile = await res.json();
            await saveProfile(exampleProfile);

            setStatus("Loaded example profile ✅");
        } catch (e) {
            console.error("❌ Failed to load example profile:", e);
            setStatus("Error: couldn't load example profile");
        }
    });
}

// Generate -> uses saved profile + scraped JD
generateBtn.onclick = async () => {
    console.log("▶️ Generate button clicked"); // DEBUG

    setStatus("Reading job description from page...");
    outputEl.value = "";
    downloadBtn.disabled = true;

    try {
        const apiBase = apiBaseEl.value.trim();
        if (!apiBase) {
            setStatus("Set backend URL first.");
            return;
        }

        // Get stored profile
        const profile = await getSavedProfile();
        if (!profile) {
            setProfileStatus("No profile loaded ❌");
            setStatus("Upload a Profile JSON (or click 'Load Example Profile') first.");
            return;
        }

        // Get JD from content script
        const tab = await getActiveTab();
        console.log("📨 Sending GET_JD_TEXT to content script"); // DEBUG

        const response = await chrome.tabs.sendMessage(tab.id, { type: "GET_JD_TEXT" });
        const jdText = response?.jdText || "";

        console.log("📄 JD length:", jdText.length); // DEBUG
        if (!jdText) {
            setStatus("Could not extract job description.");
            return;
        }

        setStatus("Calling backend to generate LaTeX...");
        console.log("🌐 Calling backend:", `${apiBase}/generate`); // DEBUG

        const res = await fetch(`${apiBase}/generate`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ profile, job_description: jdText }),
        });

        console.log("📡 Backend response status:", res.status); // DEBUG

        if (!res.ok) {
            const t = await res.text();
            throw new Error(`Backend error: ${res.status} ${t}`);
        }

        const data = await res.json();
        latestLatex = data.latex || "";

        console.log("📄 LaTeX length:", latestLatex.length); // DEBUG

        outputEl.value = latestLatex;
        downloadBtn.disabled = !latestLatex;
        setStatus("Done ✅");
    } catch (err) {
        console.error("❌ Error during generation:", err); // DEBUG
        setStatus(`Error: ${err.message}`);
    }
};

loadSettings();
