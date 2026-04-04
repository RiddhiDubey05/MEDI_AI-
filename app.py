import os
import json
import uuid
from datetime import datetime
from pathlib import Path
from flask import Flask, render_template, request, jsonify
from engine import analyze_symptoms

app = Flask(__name__)

DATA_FILE = Path("data/patients.json")
DATA_FILE.parent.mkdir(exist_ok=True)
if not DATA_FILE.exists():
    DATA_FILE.write_text("[]")


def read_patients():
    return json.loads(DATA_FILE.read_text())


def write_patients(patients):
    DATA_FILE.write_text(json.dumps(patients, indent=2))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/analyze", methods=["POST"])
def analyze():
    body = request.get_json()
    symptoms      = body.get("symptoms", "").strip()
    name          = body.get("name", "").strip()
    age           = body.get("age", "")
    sex           = body.get("sex", "")
    duration_val  = body.get("durationVal", "")
    duration_unit = body.get("durationUnit", "days")
    medical_history = body.get("medicalHistory", "").strip()
    medications   = body.get("medications", "").strip()
    allergies     = body.get("allergies", "").strip()

    if not symptoms:
        return jsonify({"error": "Please describe the patient symptoms."}), 400

    result = analyze_symptoms(symptoms, age, sex, medical_history, medications, allergies, duration_val, duration_unit)
    return jsonify(result)


from engine import normalize

# In-memory session state for chat (simplified)
chat_session = {"active_pt_id": None}

@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        body    = request.get_json()
        message = body.get("message", "").strip().lower()
        
        patients = read_patients()
        
        # helper to find patient with PRIORITY on exact matches
        def find_pt(text, pts):
            text_norm = normalize(text)
            # Priority 1: Exact Name Match (case-insensitive)
            for p in pts:
                p_name_norm = normalize(p.get("name", ""))
                if p_name_norm == text_norm:
                    return p
            
            # Priority 2: Name exists within the message (for queries like "details of geetika")
            for p in pts:
                p_name_norm = normalize(p.get("name", ""))
                if p_name_norm and p_name_norm in text_norm:
                    return p
            return None

        # Step 1: Check for Patient List
        if "patient list" in message or "show all patients" in message:
            if not patients:
                return jsonify({"reply": "I don't have any patient records stored yet."})
            names = [p.get("name", "Unnamed") for p in patients]
            return jsonify({"reply": f"Stored Patients: {', '.join(names)}\n\nType a name to select a patient."})

        # Step 2: Extract patient from message or use active one
        pt = find_pt(message, patients)
        
        # Logic Fix: If user typed a name-like message but it didn't match any patient,
        # we should NOT use the old active_pt_id. We should warn them.
        is_name_query = len(message.split()) <= 2 # Simple heuristic for "is this just a name?"
        
        if pt:
            chat_session["active_pt_id"] = pt.get("id")
        else:
            # If no name-match found in this message, check if we should keep focus or error out
            if is_name_query and len(message) > 2:
                # User likely tried to type a name but failed
                return jsonify({"reply": "Patient not found. Please check the name or type 'patient list'."})
            
            if chat_session["active_pt_id"]:
                pt = next((p for p in patients if p["id"] == chat_session["active_pt_id"]), None)

        # Step 3: Handle queries for the selected patient
        if pt:
            name = pt.get("name", "this patient")
            
            # Specific Query: Allergies
            if "allergies" in message or "allergy" in message:
                val = pt.get("allergies") or "No known allergies"
                return jsonify({"reply": f"Allergies for {name}: {val}"})
            
            # Specific Query: History / Symptoms + Diagnosis
            if "history" in message or "symptoms" in message or "diagnosis" in message:
                syms = pt.get("symptoms", "Not recorded")
                diag = "No diagnosis yet"
                results = pt.get("results")
                if results:
                    if isinstance(results, dict) and "diagnoses" in results:
                        diag = results["diagnoses"][0]["name"] if results["diagnoses"] else "No match"
                    elif isinstance(results, list):
                        diag = results[0].get("disease", "No match") if results else "No match"
                
                return jsonify({"reply": f"Medical History for {name}:\nSymptoms: {syms}\nTop Diagnosis: {diag}"})
            
            # Specific Query: Details / Info
            if "details" in message or "info" in message or "more about" in message:
                age = pt.get("age", "?")
                sex = pt.get("sex", "?")
                phone = pt.get("phone", "Not provided")
                next_v = pt.get("nextVisit", "None scheduled")
                hist = pt.get("medicalHistory", "None")
                return jsonify({
                    "reply": f"Details for {name}:\nAge: {age}\nSex: {sex}\nPhone: {phone}\nMedical History: {hist}\nAllergies: {pt.get('allergies', 'None')}\nNext Appointment: {next_v}"
                })

            # Default: If name was matched exactly, show full summary
            if pt and normalize(pt.get("name","")) in normalize(message):
                syms = pt.get("symptoms", "Not recorded")
                results = pt.get("results")
                diag = "N/A"
                if results:
                    if isinstance(results, dict) and "diagnoses" in results:
                        diag = results["diagnoses"][0]["name"] if results["diagnoses"] else "No match"
                    elif isinstance(results, list):
                        diag = results[0].get("disease", "No match") if results else "No match"
                
                return jsonify({"reply": f"Selected Patient: {name}\n\nSymptoms: {syms}\nDiagnosis: {diag}\n\nYou can now ask about their allergies, history, or info."})

        # Generic fallback
        responses = {
            "emergency": "If you experience severe chest pain or difficulty breathing, call 112 immediately.",
            "doctor": "I am an AI assistant. Please consult a licensed professional for medical advice.",
            "hi": "Hello! List patients by typing 'patient list' or select one by name.",
            "hello": "Hello! Type a patient's name to see their history.",
            "help": "Try: 'patient list' or '[patient name]'. Once selected, you can ask for 'allergies' or 'history'.",
        }

        for keyword, response in responses.items():
            if keyword in message:
                return jsonify({"reply": response})

        if not pt:
            return jsonify({"reply": "I couldn't find that patient. Try 'patient list' to see all stored names."})
        else:
            return jsonify({"reply": f"I'm now focused on {pt.get('name')}. Ask for 'allergies', 'history', or 'details'."})
            
    except Exception as e:
        print(f"Chat error: {e}")
        return jsonify({"reply": "I'm sorry, I'm having trouble responding right now. Please try asking about 'patient list'."})
            
    except Exception as e:
        print(f"Chat error: {e}")
        return jsonify({"reply": "I'm sorry, I'm having trouble responding right now. Please try asking about 'patient list'."})


@app.route("/api/patients", methods=["GET"])
def get_patients():
    return jsonify(read_patients())


@app.route("/api/patients", methods=["POST"])
def save_patient():
    body       = request.get_json()
    patients   = read_patients()
    patient_id = body.get("id")
    existing   = next((p for p in patients if p["id"] == patient_id), None)

    record = {
        "id":             patient_id or str(uuid.uuid4()),
        "name":           body.get("name") or "Unnamed Patient",
        "age":            body.get("age", ""),
        "sex":            body.get("sex", ""),
        "symptoms":       body.get("symptoms", ""),
        "durationVal":    body.get("durationVal", ""),
        "durationUnit":   body.get("durationUnit", "days"),
        "medicalHistory": body.get("medicalHistory", ""),
        "medications":    body.get("medications", ""),
        "allergies":      body.get("allergies", ""),
        "phone":          body.get("phone", ""),
        "nextVisit":      body.get("nextVisit", ""),
        "date":           body.get("date") or datetime.now().isoformat(),
        "results":        body.get("results", {})
    }

    if existing:
        patients = [record if p["id"] == patient_id else p for p in patients]
    else:
        patients.insert(0, record)

    write_patients(patients)
    return jsonify(record)


@app.route("/api/patients/<patient_id>", methods=["DELETE"])
def delete_patient(patient_id):
    patients = [p for p in read_patients() if p["id"] != patient_id]
    write_patients(patients)
    return jsonify({"success": True})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
