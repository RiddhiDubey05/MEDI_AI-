// =====================
// ANALYZE BUTTON
// =====================
document.getElementById("analyzeBtn").onclick = async function() {
    const btn = this;
    const name = document.getElementById("patientName").value || "Unnamed Patient";
    const symptoms = document.getElementById("symptoms").value;
    const age = document.getElementById("age").value;
    const sex = document.getElementById("sex").value;
    const medicalHistory = document.getElementById("medicalHistory").value;
    const medications = document.getElementById("medications").value;
    const allergies = document.getElementById("allergies").value;
    const durationVal = document.getElementById("durationVal").value;
    const durationUnit = document.getElementById("durationUnit").value;

    if (!symptoms) {
        alert("Please enter symptoms before running diagnosis.");
        return;
    }

    const btnText = document.getElementById("btnText");
    const spinner = document.getElementById("spinner");

    btn.disabled = true;
    if(btnText) btnText.style.display = "none";
    if(spinner) spinner.style.display = "block";

    try {
        const res = await fetch("/api/analyze", {
            method: "POST",
            headers: {"Content-Type":"application/json"},
            body: JSON.stringify({
                name, age, sex, symptoms, medicalHistory, medications, allergies, durationVal, durationUnit
            })
        });
        const results = await res.json();
        
        displayResults(results);
        
        // Save to global storage via patients.js function
        if(typeof saveRecord === 'function') {
            await saveRecord({
                name, age, sex, symptoms, medicalHistory, medications, allergies, durationVal, durationUnit,
                results,
                date: new Date().toISOString()
            });
        }
    } catch (err) {
        console.error("Diagnosis error:", err);
        alert("An error occurred during diagnosis. Please try again.");
    } finally {
        btn.disabled = false;
        if(btnText) btnText.style.display = "inline";
        if(spinner) spinner.style.display = "none";
    }
};

// =====================
// DISPLAY RESULTS
// =====================
function displayResults(data) {
    const panel = document.getElementById("resultsPanel");
    if(!panel) return;

    // Handle different response formats
    const summary = data.summary || "";
    const diagnoses = data.diagnoses || (Array.isArray(data) ? data : []);
    const redFlags = data.red_flags || [];

    let html = `
        <div class="summary-card">
            <h2>Diagnosis Summary</h2>
            <p>${summary}</p>
        </div>
    `;

    if (redFlags.length > 0) {
        html += `
            <div class="red-flags-box">
                <h3>🚨 Red Flag Warnings</h3>
                <ul>${redFlags.map(f => `<li>${f}</li>`).join("")}</ul>
            </div>
        `;
    }

    html += `<div class="grid-header"><h2>Matched Conditions</h2><div class="badge">Top Matches</div></div>`;

    diagnoses.forEach(r => {
        let severityClass = "sev-mild";
        if (r.severity === "Moderate") severityClass = "sev-moderate";
        if (r.severity === "Severe" || r.severity === "High" ) severityClass = "sev-severe";
        if (r.severity === "Critical") severityClass = "sev-critical";

        html += `
        <div class="dx-card">
            <div class="dx-top">
                <div class="dx-left">
                    <div class="dx-name">${r.name || r.disease}</div>
                    <div class="dx-icd">ICD: ${r.icd_code || "N/A"}</div>
                </div>
                <div class="dx-right">
                    <div class="prob-num">${r.probability}%</div>
                    <div class="sev-pill ${severityClass}">${r.severity}</div>
                </div>
            </div>
            <p class="dx-desc">${r.description || `Based on symptoms, this condition matches ${r.matched_symptoms?.length || r.matched || 0} key indicators.`}</p>
            ${r.matched_symptoms ? `
                <div class="sec-label">Matched Symptoms</div>
                <div class="tags">${r.matched_symptoms.map(s => `<span class="tag matched">${s}</span>`).join("")}</div>
            ` : ""}
            ${r.treatment_overview ? `
                <div class="treatment-box">
                    <div class="sec-label">Treatment Overview</div>
                    ${r.treatment_overview}
                </div>
            ` : ""}
        </div>`;
    });

    panel.innerHTML = html;
    
    // Update chat context if function exists
    if(typeof updateContext === 'function') {
        const name = document.getElementById("patientName").value || "Patient";
        updateContext(data, `${name}, ${document.getElementById("age").value || "?"} ${document.getElementById("sex").value || ""}`);
    }
}

// =====================
// CHAT - Move to chat.js or keep simple here?
// I'll keep the basic chat logic here or allow chat.js to override.
// Actually, let's remove the redundant patient array management here since patients.js handles it.