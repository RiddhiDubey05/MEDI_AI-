// =====================
// GLOBAL STORAGE (PERSISTENT)
// =====================
let patients = JSON.parse(localStorage.getItem("patients")) || [];

// =====================
// ANALYSIS ENGINE (KEEP YOUR LIST SAME)
// =====================
function analyzeSymptoms(symptoms) {

    const text = symptoms.toLowerCase();

    const diseases = [ /* KEEP YOUR FULL DISEASE ARRAY HERE */];

    let results = [];

    diseases.forEach(d => {
        let score = 0;

        d.symptoms.forEach(sym => {
            if (text.includes(sym)) score++;
        });

        if (score > 0) {
            results.push({
                disease: d.name,
                probability: Math.min(95, score * 30),
                severity: d.severity,
                matched: score
            });
        }
    });

    if (results.length === 0) {
        results.push({
            disease: "General Condition",
            probability: 50,
            severity: "Unknown",
            matched: 0
        });
    }

    results.sort((a, b) => b.probability - a.probability);
    return results.slice(0, 5);
}

// =====================
// ANALYZE BUTTON (SAVE FULL DATA)
// =====================
document.getElementById("analyzeBtn").onclick = function () {

    const name = document.getElementById("patientName").value || "Unknown";
    const symptoms = document.getElementById("symptoms").value;

    if (!symptoms) {
        alert("Enter symptoms");
        return;
    }

    const results = analyzeSymptoms(symptoms);

    const patient = {
        name,
        age: document.getElementById("age")?.value || "N/A",
        gender: document.getElementById("gender")?.value || "N/A",
        history: document.getElementById("history")?.value || "None",
        medications: document.getElementById("medications")?.value || "None",
        allergies: document.getElementById("allergies")?.value || "None",
        symptoms,
        results,
        date: new Date().toLocaleString()
    };

    patients.unshift(patient);

    // SAVE TO LOCAL STORAGE
    localStorage.setItem("patients", JSON.stringify(patients));

    displayResults(results);
    updatePatientList();
};

// =====================
// DISPLAY RESULTS
// =====================
function displayResults(results) {

    let html = `<div class="grid-header">
        <h2>Diagnosis Results</h2>
        <div class="badge">Top Matches</div>
    </div>`;

    results.forEach(r => {

        let severityClass = "sev-mild";
        if (r.severity === "Moderate") severityClass = "sev-moderate";
        if (r.severity === "Serious") severityClass = "sev-severe";
        if (r.severity === "Critical") severityClass = "sev-critical";

        html += `
        <div class="dx-card">
            <div class="dx-top">
                <div class="dx-left">
                    <div class="dx-name">${r.disease}</div>
                </div>
                <div class="dx-right">
                    <div class="prob-num">${r.probability}%</div>
                    <div class="sev-pill ${severityClass}">${r.severity}</div>
                </div>
            </div>
            <div class="dx-desc">
                Matches ${r.matched} symptoms
            </div>
        </div>`;
    });

    document.getElementById("resultsPanel").innerHTML = html;
}

// =====================
// PATIENT LIST + DELETE
// =====================
function updatePatientList() {

    let container = document.getElementById("ptList");

    if (patients.length === 0) {
        container.innerHTML = `<div>No records yet.</div>`;
        return;
    }

    let html = "";

    patients.forEach((p, i) => {
        html += `
        <div class="pt-item">
            <div onclick="loadPatient(${i})">
                <div>${p.name}</div>
                <small>${p.date}</small>
            </div>
            <button onclick="deletePatient(${i})">❌</button>
        </div>`;
    });

    container.innerHTML = html;
}

function loadPatient(i) {
    const p = patients[i];

    document.getElementById("patientName").value = p.name;
    document.getElementById("symptoms").value = p.symptoms;

    displayResults(p.results);
}

// =====================
// DELETE PATIENT
// =====================
function deletePatient(index) {

    if (!confirm("Delete this patient record?")) return;

    patients.splice(index, 1);

    localStorage.setItem("patients", JSON.stringify(patients));

    updatePatientList();

    document.getElementById("resultsPanel").innerHTML =
        `<div>Record deleted.</div>`;
}

// =====================
// NEW BUTTON FIX
// =====================
document.getElementById("newBtn").onclick = function () {

    document.getElementById("patientName").value = "";
    document.getElementById("symptoms").value = "";

    document.getElementById("resultsPanel").innerHTML =
        `<div>Ready for new diagnosis</div>`;
};

function processChat(msg) {

    if (patients.length === 0) {
        return "No patient records found.";
    }

    // ✅ Patient list
    if (msg.includes("patient") && msg.includes("list")) {
        return "Stored Patients: " + patients.map(p => p.name).join(", ") +
            "\n\nType a name to view full details.";
    }

    // ✅ EXACT NAME MATCH (MOST IMPORTANT FIX)
    let exactMatch = patients.find(p => p.name.toLowerCase() === msg);

    if (exactMatch) {
        return `
Name: ${exactMatch.name}
Age: ${exactMatch.age}
Gender: ${exactMatch.gender}
History: ${exactMatch.history}
Medications: ${exactMatch.medications}
Allergies: ${exactMatch.allergies}
Symptoms: ${exactMatch.symptoms}
Top Disease: ${exactMatch.results?.[0]?.disease || "N/A"}
        `;
    }

    // ✅ FIND NAME INSIDE SENTENCE (like "details of priya")
    let found = patients.find(p => msg.includes(p.name.toLowerCase()));

    if (!found) {
        return "Patient not found. Try: 'patient list' or 'details of name'";
    }

    // ✅ FULL DETAILS
    if (msg.includes("details") || msg.includes("history")) {
        return `
Name: ${found.name}
Age: ${found.age}
Gender: ${found.gender}
History: ${found.history}
Medications: ${found.medications}
Allergies: ${found.allergies}
Symptoms: ${found.symptoms}
Top Disease: ${found.results?.[0]?.disease || "N/A"}
        `;
    }

    // ✅ Allergies
    if (msg.includes("allerg")) {
        return `${found.name}'s allergies: ${found.allergies}`;
    }

    // ✅ Medications
    if (msg.includes("medication")) {
        return `${found.name}'s medications: ${found.medications}`;
    }

    // ✅ Age
    if (msg.includes("age")) {
        return `${found.name} is ${found.age} years old`;
    }

    // ✅ Symptoms
    if (msg.includes("symptom")) {
        return `${found.name}'s symptoms: ${found.symptoms}`;
    }

    // ✅ Diagnosis
    if (msg.includes("disease") || msg.includes("diagnosis")) {
        return `Top disease for ${found.name}: ${found.results?.[0]?.disease || "N/A"}`;
    }

    return "Try: 'patient list', 'details of name', or type patient name";
}
// =====================
// LOAD DATA ON START
// =====================
updatePatientList();

// =====================
// EMERGENCY (UNCHANGED)
// =====================
document.getElementById("sosBtn").onclick = function () {
    document.getElementById("sosModal").classList.add("open");
};

document.getElementById("closeSosBtn").onclick = function () {
    document.getElementById("sosModal").classList.remove("open");
};