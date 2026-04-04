import re

DISEASES = [
    {
        "name": "Migraine",
        "icd_code": "G43.9",
        "severity": "Moderate",
        "keywords": ["headache","head pain","throbbing","pulsating","nausea","vomiting","light sensitivity","photophobia","sound sensitivity","phonophobia","aura","visual disturbance","one side","unilateral","worse with movement","lasts hours","lasts days"],
        "risk_factors": ["female","stress","sleep deprivation","hormonal","caffeine","alcohol","chocolate","bright lights","loud noise"],
        "matched_symptoms": [],
        "missing_symptoms": ["aura","visual zig-zag","vomiting"],
        "recommended_tests": ["Neurological examination","MRI brain (to rule out secondary causes)","CT scan if first severe headache","CBC and metabolic panel"],
        "treatment_overview": "NSAIDs (ibuprofen), triptans (sumatriptan) for acute attacks. Preventive: propranolol, amitriptyline. Avoid known triggers.",
        "followup_question": "Does the headache worsen with physical activity and is it on one side of the head?",
        "urgency": "Soon",
        "lifestyle_advice": ["Maintain regular sleep schedule","Keep a headache diary to identify triggers","Stay well hydrated","Limit caffeine and alcohol intake","Practice stress-reduction techniques"],
        "when_to_seek_emergency": "Sudden worst headache of your life, headache with fever and stiff neck, headache after head injury, or headache with confusion or vision loss — go to ER immediately."
    },
    {
        "name": "Tension-Type Headache",
        "icd_code": "G44.2",
        "severity": "Mild",
        "keywords": ["headache","head pain","pressure","tight band","both sides","bilateral","neck pain","shoulder tension","stress","mild nausea","dull ache","squeezing"],
        "risk_factors": ["stress","poor posture","long screen time","anxiety","fatigue","dehydration"],
        "matched_symptoms": [],
        "missing_symptoms": ["nausea","vomiting"],
        "recommended_tests": ["Clinical examination","Blood pressure check","Eye examination"],
        "treatment_overview": "Paracetamol (acetaminophen) or ibuprofen. Relaxation techniques. Address posture and stress.",
        "followup_question": "Is the headache like a tight band around the whole head rather than one side?",
        "urgency": "Routine",
        "lifestyle_advice": ["Take regular breaks from screens","Check and correct posture","Stay hydrated","Practice neck stretches daily","Manage stress with breathing exercises"],
        "when_to_seek_emergency": "Sudden severe headache, headache with fever or stiff neck, or headache with neurological symptoms such as weakness or slurred speech."
    },
    {
        "name": "Common Cold (Viral Upper Respiratory Infection)",
        "icd_code": "J00",
        "severity": "Mild",
        "keywords": ["runny nose","stuffy nose","blocked nose","congestion","sneezing","sore throat","cough","mild fever","fatigue","watery eyes","hoarse voice","nasal discharge","mucus"],
        "risk_factors": ["contact with infected person","cold weather","low immunity","stress","children","crowded places"],
        "matched_symptoms": [],
        "missing_symptoms": ["high fever","body aches"],
        "recommended_tests": ["Clinical diagnosis — no tests usually needed","Throat swab if bacterial infection suspected","CBC if symptoms persist beyond 10 days"],
        "treatment_overview": "Rest, fluids, saline nasal spray, paracetamol for fever/pain. Antibiotics are NOT indicated for viral infections.",
        "followup_question": "Do symptoms include fever above 38.5°C or severe body aches suggesting flu rather than a cold?",
        "urgency": "Routine",
        "lifestyle_advice": ["Rest and sleep as much as possible","Drink warm fluids — water, herbal tea, soups","Wash hands frequently","Avoid spreading to others","Eat vitamin C-rich foods"],
        "when_to_seek_emergency": "Difficulty breathing, chest pain, high fever above 39.5°C that does not respond to medication, or symptoms lasting more than 10 days."
    },
    {
        "name": "Influenza (Flu)",
        "icd_code": "J11.1",
        "severity": "Moderate",
        "keywords": ["fever","high fever","body ache","muscle pain","myalgia","fatigue","tiredness","headache","chills","sore throat","cough","dry cough","sudden onset","weakness","loss of appetite"],
        "risk_factors": ["flu season","unvaccinated","elderly","children","immunocompromised","crowded places"],
        "matched_symptoms": [],
        "missing_symptoms": ["chills","sudden onset","severe fatigue"],
        "recommended_tests": ["Rapid influenza diagnostic test (RIDT)","RT-PCR for influenza","Chest X-ray if pneumonia suspected","CBC"],
        "treatment_overview": "Oseltamivir (Tamiflu) within 48 hours of onset for high-risk patients. Rest, fluids, paracetamol/ibuprofen for fever and pain.",
        "followup_question": "Did the illness start suddenly within hours, with high fever and severe body aches?",
        "urgency": "Soon",
        "lifestyle_advice": ["Complete bed rest until fever-free for 24 hours","Drink plenty of fluids","Get vaccinated annually for prevention","Avoid contact with vulnerable people","Eat light nutritious meals"],
        "when_to_seek_emergency": "Difficulty breathing, persistent chest pain, confusion, severe vomiting, or bluish discoloration of skin — seek emergency care immediately."
    },
    {
        "name": "COVID-19",
        "icd_code": "U07.1",
        "severity": "Moderate",
        "keywords": ["fever","cough","dry cough","fatigue","loss of smell","anosmia","loss of taste","ageusia","sore throat","shortness of breath","breathlessness","headache","body ache","diarrhoea","chest pain","runny nose","chills","conjunctivitis"],
        "risk_factors": ["contact with covid patient","unvaccinated","elderly","diabetes","hypertension","obesity","immunocompromised"],
        "matched_symptoms": [],
        "missing_symptoms": ["loss of smell","loss of taste","shortness of breath"],
        "recommended_tests": ["RT-PCR nasal swab","Rapid antigen test","SpO2 monitoring","Chest X-ray or CT scan","CBC, CRP, D-dimer, ferritin"],
        "treatment_overview": "Isolation, rest, fluids. Paracetamol for fever. Antivirals (nirmatrelvir/ritonavir) for high-risk. Oxygen if SpO2 falls below 94%.",
        "followup_question": "Have you lost your sense of smell or taste, and have you been in contact with a COVID-positive person recently?",
        "urgency": "Soon",
        "lifestyle_advice": ["Isolate immediately until test result is known","Monitor oxygen saturation with pulse oximeter","Stay well hydrated","Eat nutritious food","Ventilate your room properly"],
        "when_to_seek_emergency": "SpO2 below 94%, persistent chest pain or pressure, confusion, inability to stay awake, or bluish lips — call emergency services immediately."
    },
    {
        "name": "Gastroenteritis (Stomach Flu)",
        "icd_code": "A09",
        "severity": "Moderate",
        "keywords": ["diarrhoea","diarrhea","vomiting","nausea","stomach pain","abdominal pain","stomach cramps","loose stools","watery stool","fever","loss of appetite","dehydration","weakness","bloating"],
        "risk_factors": ["contaminated food","contaminated water","poor hygiene","travel","viral infection","bacterial infection"],
        "matched_symptoms": [],
        "missing_symptoms": ["blood in stool","severe dehydration"],
        "recommended_tests": ["Stool culture","CBC","Electrolytes panel","Stool microscopy for parasites if prolonged"],
        "treatment_overview": "Oral rehydration salts (ORS), clear fluids, BRAT diet (banana, rice, applesauce, toast). Antiemetics if needed. Antibiotics only for confirmed bacterial cause.",
        "followup_question": "Did the symptoms start after eating a particular food, or is there blood in your stool?",
        "urgency": "Soon",
        "lifestyle_advice": ["Drink ORS frequently in small sips","Avoid dairy, fatty and spicy foods until recovered","Wash hands thoroughly before eating","Eat plain rice, banana, or toast","Rest completely"],
        "when_to_seek_emergency": "Signs of severe dehydration (no urine for 8+ hours, sunken eyes, dry mouth), blood in vomit or stool, high fever, or symptoms in infants and elderly."
    },
    {
        "name": "Urinary Tract Infection (UTI)",
        "icd_code": "N39.0",
        "severity": "Moderate",
        "keywords": ["burning urination","painful urination","dysuria","frequent urination","urgency","urge to urinate","cloudy urine","blood in urine","haematuria","lower abdominal pain","pelvic pain","foul smelling urine","dark urine","lower back pain"],
        "risk_factors": ["female","sexual activity","catheter use","diabetes","poor hygiene","dehydration","menopause","pregnancy","urinary tract anomaly"],
        "matched_symptoms": [],
        "missing_symptoms": ["fever","back pain"],
        "recommended_tests": ["Urine dipstick test","Urine microscopy and culture","CBC if pyelonephritis suspected","Ultrasound kidney-bladder if recurrent"],
        "treatment_overview": "Antibiotics: trimethoprim-sulfamethoxazole or nitrofurantoin for uncomplicated UTI (3-7 days). Increase fluid intake. Pyridium for pain relief.",
        "followup_question": "Is there fever, flank pain, or back pain that could suggest the infection has spread to the kidneys?",
        "urgency": "Soon",
        "lifestyle_advice": ["Drink 2-3 litres of water daily","Urinate after sexual intercourse","Wipe front to back","Avoid harsh soaps in the genital area","Complete the full antibiotic course"],
        "when_to_seek_emergency": "High fever with chills, severe back or flank pain, nausea and vomiting with UTI symptoms, or symptoms in pregnant women — these indicate possible kidney infection."
    },
    {
        "name": "Hypertensive Crisis / High Blood Pressure",
        "icd_code": "I10",
        "severity": "Severe",
        "keywords": ["high blood pressure","hypertension","severe headache","dizziness","blurred vision","chest pain","shortness of breath","nosebleed","palpitations","anxiety","confusion","neck stiffness","sweating"],
        "risk_factors": ["obesity","salt intake","stress","family history","age","smoking","alcohol","diabetes","kidney disease","sedentary lifestyle"],
        "matched_symptoms": [],
        "missing_symptoms": ["chest pain","confusion","blurred vision"],
        "recommended_tests": ["Blood pressure measurement (both arms)","ECG","Urine albumin","Renal function tests","Fundoscopy","Chest X-ray","CBC and metabolic panel"],
        "treatment_overview": "Lifestyle modifications first. Antihypertensives: amlodipine, lisinopril, losartan, or hydrochlorothiazide based on patient profile.",
        "followup_question": "What is your blood pressure reading right now, and do you have a history of hypertension?",
        "urgency": "Urgent",
        "lifestyle_advice": ["Reduce salt intake below 5g per day","Exercise 30 minutes on most days","Maintain healthy weight","Avoid alcohol and smoking","Monitor BP daily at home"],
        "when_to_seek_emergency": "BP above 180/120 mmHg with symptoms of chest pain, shortness of breath, blurred vision, or confusion — go to ER immediately."
    },
    {
        "name": "Type 2 Diabetes Mellitus",
        "icd_code": "E11.9",
        "severity": "Moderate",
        "keywords": ["increased thirst","polydipsia","frequent urination","polyuria","fatigue","tiredness","blurred vision","slow healing","weight loss","hunger","tingling","numbness","dry mouth","recurrent infections","dark skin patches"],
        "risk_factors": ["obesity","family history","sedentary lifestyle","age over 45","gestational diabetes","prediabetes","polycystic ovary","high blood pressure","high cholesterol"],
        "matched_symptoms": [],
        "missing_symptoms": ["blurred vision","numbness in feet","slow wound healing"],
        "recommended_tests": ["Fasting blood glucose","HbA1c (glycated haemoglobin)","Oral glucose tolerance test","Urine microalbumin","Lipid profile","Kidney function tests","Eye examination"],
        "treatment_overview": "Lifestyle changes, metformin as first-line pharmacotherapy. SGLT2 inhibitors or GLP-1 agonists for additional benefit. Monitor HbA1c every 3 months.",
        "followup_question": "Have you had a fasting blood sugar test recently, and do you have a family history of diabetes?",
        "urgency": "Soon",
        "lifestyle_advice": ["Follow a low-glycaemic diet — reduce refined carbs and sugar","Exercise at least 150 minutes per week","Monitor blood glucose regularly","Maintain healthy body weight","Quit smoking and limit alcohol"],
        "when_to_seek_emergency": "Extremely high blood sugar (above 400 mg/dL) with confusion or vomiting, or very low blood sugar with sweating, shaking, and loss of consciousness."
    },
    {
        "name": "Anxiety Disorder / Panic Attack",
        "icd_code": "F41.1",
        "severity": "Moderate",
        "keywords": ["anxiety","worry","panic","racing heart","palpitations","sweating","trembling","shaking","shortness of breath","chest tightness","dizziness","lightheadedness","nausea","fear","restlessness","sleep problems","insomnia","irritability","muscle tension"],
        "risk_factors": ["stress","trauma","family history","chronic illness","caffeine","substance use","major life changes","isolation"],
        "matched_symptoms": [],
        "missing_symptoms": ["chest pain","trembling","sense of doom"],
        "recommended_tests": ["Clinical psychological assessment","Thyroid function tests (to rule out hyperthyroidism)","ECG (to rule out cardiac cause)","CBC","Blood glucose"],
        "treatment_overview": "Cognitive behavioural therapy (CBT) as first-line. SSRIs (sertraline, escitalopram) for pharmacotherapy. Benzodiazepines short-term only.",
        "followup_question": "Do these episodes come on suddenly, peak within minutes, and make you feel like something terrible is about to happen?",
        "urgency": "Soon",
        "lifestyle_advice": ["Practice deep breathing — 4-7-8 technique","Limit caffeine and alcohol","Exercise regularly — reduces anxiety significantly","Maintain consistent sleep schedule","Consider mindfulness or meditation apps"],
        "when_to_seek_emergency": "If you cannot distinguish a panic attack from a heart attack — chest pain with radiation to arm or jaw, or sudden loss of consciousness, go to ER."
    },
    {
        "name": "Iron-Deficiency Anaemia",
        "icd_code": "D50.9",
        "severity": "Mild",
        "keywords": ["fatigue","tiredness","weakness","pale skin","pallor","shortness of breath","dizziness","lightheadedness","headache","cold hands","cold feet","brittle nails","hair loss","pica","craving ice","fast heartbeat","palpitations","poor concentration","brain fog"],
        "risk_factors": ["female","menstruation","pregnancy","vegetarian","vegan","poor diet","blood loss","malabsorption","chronic disease","frequent blood donation"],
        "matched_symptoms": [],
        "missing_symptoms": ["pale conjunctiva","brittle nails","pica"],
        "recommended_tests": ["CBC with differential","Serum ferritin","Serum iron and TIBC","Peripheral blood smear","Reticulocyte count","Stool for occult blood"],
        "treatment_overview": "Oral iron supplementation (ferrous sulphate 200mg TDS). Vitamin C enhances absorption. Treat underlying cause. IV iron if oral not tolerated.",
        "followup_question": "Do you have heavy menstrual periods, or have you noticed your nails becoming brittle or spoon-shaped?",
        "urgency": "Routine",
        "lifestyle_advice": ["Eat iron-rich foods — spinach, lentils, meat, fortified cereals","Take iron supplements with vitamin C","Avoid tea or coffee with meals — they block iron absorption","Cook in cast iron pots","Get regular haemoglobin checks"],
        "when_to_seek_emergency": "Severe breathlessness at rest, chest pain, rapid heart rate above 120, or fainting — these may indicate severe anaemia requiring transfusion."
    },
    {
        "name": "Gastroesophageal Reflux Disease (GERD)",
        "icd_code": "K21.0",
        "severity": "Mild",
        "keywords": ["heartburn","acid reflux","chest burn","burning sensation","regurgitation","sour taste","bitter taste","chest pain","difficulty swallowing","dysphagia","bloating","belching","burping","hoarseness","throat clearing","cough after eating","worse lying down","worse after meals"],
        "risk_factors": ["obesity","pregnancy","hiatal hernia","spicy food","fatty food","alcohol","smoking","caffeine","lying down after meals","large meals","stress"],
        "matched_symptoms": [],
        "missing_symptoms": ["regurgitation","difficulty swallowing"],
        "recommended_tests": ["Clinical diagnosis","Upper GI endoscopy if alarm symptoms","24-hour pH monitoring","Oesophageal manometry","H. pylori test"],
        "treatment_overview": "Lifestyle changes, antacids for immediate relief. Proton pump inhibitors (omeprazole, pantoprazole) for regular use. H2 blockers (ranitidine) as alternative.",
        "followup_question": "Does the burning sensation get worse when you lie down or bend over, and does it improve with antacids?",
        "urgency": "Routine",
        "lifestyle_advice": ["Avoid eating within 3 hours of bedtime","Elevate head of bed by 15-20 cm","Lose weight if overweight","Avoid spicy, fatty, and acidic foods","Eat smaller, more frequent meals"],
        "when_to_seek_emergency": "Vomiting blood, black tarry stools, severe chest pain, sudden difficulty swallowing, or unexplained weight loss — these require immediate evaluation."
    },
    {
        "name": "Asthma",
        "icd_code": "J45.9",
        "severity": "Moderate",
        "keywords": ["wheezing","shortness of breath","breathlessness","chest tightness","cough","dry cough","nighttime cough","cough worse at night","triggered by exercise","triggered by allergens","difficulty breathing","whistling sound","wheeze","breathless after activity","pollen allergy"],
        "risk_factors": ["family history","allergies","eczema","hay fever","air pollution","smoking","dust mites","pet dander","cold air","exercise","obesity","respiratory infections"],
        "matched_symptoms": [],
        "missing_symptoms": ["wheezing","nighttime cough","trigger-related symptoms"],
        "recommended_tests": ["Spirometry","Peak expiratory flow measurement","Bronchodilator reversibility test","Allergy skin prick test","Chest X-ray","FeNO test","CBC with eosinophils"],
        "treatment_overview": "Short-acting beta-agonist (salbutamol) for rescue. Inhaled corticosteroids (beclomethasone) for maintenance. Step-up therapy per GINA guidelines.",
        "followup_question": "Do your breathing symptoms worsen at night, after exercise, or when exposed to dust, pollen, or cold air?",
        "urgency": "Soon",
        "lifestyle_advice": ["Identify and avoid your personal triggers","Keep rescue inhaler always accessible","Monitor peak flow regularly","Use allergen-proof mattress covers","Never smoke and avoid passive smoke"],
        "when_to_seek_emergency": "Severe breathlessness that prevents speaking in full sentences, no improvement with rescue inhaler, lips or fingernails turning blue — call 112 immediately."
    },
    {
        "name": "Depression (Major Depressive Disorder)",
        "icd_code": "F32.9",
        "severity": "Moderate",
        "keywords": ["sadness","low mood","depression","hopelessness","helplessness","loss of interest","anhedonia","fatigue","sleep problems","insomnia","oversleeping","weight change","appetite change","poor concentration","worthlessness","guilt","thoughts of death","suicidal thoughts","crying","withdrawal","isolation"],
        "risk_factors": ["family history","trauma","chronic illness","loss","loneliness","substance abuse","hormonal changes","postpartum","stress"],
        "matched_symptoms": [],
        "missing_symptoms": ["loss of interest","hopelessness","sleep disturbance"],
        "recommended_tests": ["PHQ-9 depression screening questionnaire","Thyroid function tests","CBC","Blood glucose","Clinical psychiatric assessment"],
        "treatment_overview": "Psychotherapy (CBT) as first-line. SSRIs (sertraline, fluoxetine) for pharmacotherapy. Combination therapy most effective. Regular follow-up essential.",
        "followup_question": "Have you lost interest in things you used to enjoy, and have you had these low mood symptoms for more than 2 weeks?",
        "urgency": "Soon",
        "lifestyle_advice": ["Maintain daily routine even when difficult","Exercise at least 30 minutes daily — proven antidepressant effect","Connect with trusted friends or family","Limit alcohol completely","Seek professional help — therapy works"],
        "when_to_seek_emergency": "If you have thoughts of harming yourself or others, or have made plans for suicide — call a crisis helpline or go to the nearest emergency department immediately."
    },
    {
        "name": "Dengue Fever",
        "icd_code": "A90",
        "severity": "Severe",
        "keywords": ["fever","high fever","sudden fever","severe headache","eye pain","behind eyes","bone pain","joint pain","muscle pain","rash","skin rash","nausea","vomiting","fatigue","bleeding gums","nose bleed","bruising","low platelet","petechiae","dengue","mosquito bite"],
        "risk_factors": ["tropical region","monsoon season","mosquito exposure","travel to endemic area","india","southeast asia","dengue outbreak"],
        "matched_symptoms": [],
        "missing_symptoms": ["rash","pain behind eyes","bleeding"],
        "recommended_tests": ["NS1 antigen test (days 1-5)","Dengue IgM/IgG antibody","CBC — platelet count and haematocrit","Liver function tests","Urine analysis"],
        "treatment_overview": "No specific antiviral. Paracetamol for fever — avoid aspirin and ibuprofen (increase bleeding risk). IV fluids for severe cases. Monitor platelet count daily.",
        "followup_question": "Do you have pain behind your eyes, and have you been exposed to mosquitoes in the last 2 weeks?",
        "urgency": "Urgent",
        "lifestyle_advice": ["Complete bed rest","Drink plenty of fluids — coconut water, ORS","Use paracetamol only — never ibuprofen or aspirin","Use mosquito repellent and nets","Monitor for warning signs daily"],
        "when_to_seek_emergency": "Severe abdominal pain, persistent vomiting, rapid breathing, bleeding from gums or nose, blood in stool or vomit, or extreme fatigue — go to hospital immediately."
    },
    {
        "name": "Appendicitis",
        "icd_code": "K37",
        "severity": "Severe",
        "keywords": ["right lower abdominal pain","appendix pain","abdominal pain","pain around navel","pain moves to right","nausea","vomiting","fever","loss of appetite","rebound tenderness","pain worsens with movement","worse when walking","mcburney point"],
        "risk_factors": ["age 10-30","male","family history","diet low in fibre","constipation"],
        "matched_symptoms": [],
        "missing_symptoms": ["pain moving to right lower quadrant","rebound tenderness","fever"],
        "recommended_tests": ["Ultrasound abdomen","CT scan abdomen (gold standard)","CBC — elevated WBC","CRP","Urine analysis to rule out UTI"],
        "treatment_overview": "Surgical emergency — appendectomy (laparoscopic preferred). IV antibiotics pre-operatively. Do not eat or drink if appendicitis suspected.",
        "followup_question": "Did the pain start around the navel and then move to the lower right side of the abdomen?",
        "urgency": "Emergency",
        "lifestyle_advice": ["Do NOT eat or drink if appendicitis is suspected","Do NOT take painkillers before a medical assessment — they can mask signs","Go to hospital without delay","High-fibre diet may reduce risk in the long term"],
        "when_to_seek_emergency": "ANY suspected appendicitis is a medical emergency. If you have right lower abdominal pain with fever, nausea, and vomiting — go to ER immediately without delay."
    },
    {
        "name": "Typhoid Fever",
        "icd_code": "A01.0",
        "severity": "Severe",
        "keywords": ["prolonged fever","step-ladder fever","stomach pain","abdominal pain","headache","weakness","fatigue","loss of appetite","diarrhoea","constipation","rose spots","rash","spleen enlarged","liver enlarged","nausea","typhoid","contaminated water","contaminated food"],
        "risk_factors": ["contaminated water","contaminated food","poor sanitation","travel to endemic area","india","south asia","young adults","children"],
        "matched_symptoms": [],
        "missing_symptoms": ["prolonged fever","rose spots rash","constipation with fever"],
        "recommended_tests": ["Widal test","Blood culture (gold standard in first week)","Typhidot IgM test","CBC — low WBC (leukopenia)","Liver function tests","Stool and urine culture"],
        "treatment_overview": "Antibiotics: azithromycin (first-line), ceftriaxone for severe cases. Course of 7-14 days. Adequate fluids and rest. Avoid raw food until recovered.",
        "followup_question": "Has the fever been gradually increasing over several days, worse in the evenings, and do you have abdominal discomfort or headache?",
        "urgency": "Urgent",
        "lifestyle_advice": ["Drink only boiled or bottled water","Eat only freshly cooked hot food","Maintain strict hand hygiene","Complete the full antibiotic course","Consider typhoid vaccination"],
        "when_to_seek_emergency": "Severe abdominal pain, intestinal perforation signs, or very high fever with confusion — go to hospital immediately."
    },
    {
        "name": "Pneumonia",
        "icd_code": "J18.9",
        "severity": "Severe",
        "keywords": ["cough","productive cough","yellow sputum","green sputum","chest pain","breathing difficulty","shortness of breath","fever","high fever","chills","fatigue","sweating","rusty sputum","pleuritic pain","pain breathing","confusion","rapid breathing"],
        "risk_factors": ["elderly","children","immunocompromised","diabetes","smoking","alcohol","recent viral infection","hospitalization","aspiration"],
        "matched_symptoms": [],
        "missing_symptoms": ["productive cough","pleuritic chest pain","high fever with chills"],
        "recommended_tests": ["Chest X-ray","CBC — elevated WBC","Sputum culture and sensitivity","Blood culture","CRP","Procalcitonin","Pulse oximetry","Urine Legionella antigen"],
        "treatment_overview": "Community-acquired: amoxicillin-clavulanate plus azithromycin. Hospitalised: IV ceftriaxone plus azithromycin. Oxygen if SpO2 below 94%.",
        "followup_question": "Do you have a productive cough with coloured sputum, fever, and does your chest hurt when you take a deep breath?",
        "urgency": "Urgent",
        "lifestyle_advice": ["Complete bed rest","Stay well hydrated","Use a humidifier if air is dry","Complete the full antibiotic course","Get pneumococcal and flu vaccine for prevention"],
        "when_to_seek_emergency": "Rapid breathing, SpO2 below 94%, confusion, inability to keep fluids down, high fever above 39.5°C that is not responding to medication."
    }
]


def normalize(text):
    return re.sub(r'[^a-z0-9 ]', ' ', text.lower())


def score_disease(disease, symptom_text, age, sex, medical_history, medications, allergies):
    text = normalize(symptom_text + " " + medical_history)
    risk_text = normalize(symptom_text + " " + medical_history + " " + (sex or "") + " " + str(age or ""))

    keyword_hits = []
    for kw in disease["keywords"]:
        if kw.lower() in text:
            keyword_hits.append(kw)

    risk_hits = sum(1 for rf in disease["risk_factors"] if rf.lower() in risk_text)

    if not keyword_hits:
        return None

    base_score = (len(keyword_hits) / max(len(disease["keywords"]), 1)) * 70
    risk_bonus  = min(risk_hits * 4, 20)
    length_bonus = min(len(symptom_text.split()) * 0.3, 10)

    raw = base_score + risk_bonus + length_bonus
    prob = max(10, min(int(round(raw)), 97))

    return {
        "name":               disease["name"],
        "icd_code":           disease["icd_code"],
        "probability":        prob,
        "severity":           disease["severity"],
        "description":        build_description(disease, keyword_hits, age, sex),
        "matched_symptoms":   keyword_hits[:6],
        "missing_symptoms":   disease["missing_symptoms"],
        "recommended_tests":  disease["recommended_tests"],
        "treatment_overview": disease["treatment_overview"],
        "followup_question":  disease["followup_question"],
        "urgency":            disease["urgency"],
        "lifestyle_advice":   disease["lifestyle_advice"],
        "when_to_seek_emergency": disease["when_to_seek_emergency"]
    }


def build_description(disease, hits, age, sex):
    name  = disease["name"]
    count = len(hits)
    sample = ", ".join(hits[:3]) if hits else "reported symptoms"
    age_str = f" in a {age}-year-old" if age else ""
    sex_str = f" {sex}" if sex else ""
    return (
        f"{name} is consistent with the presenting picture{age_str}{sex_str}, "
        f"with {count} matching indicator{'s' if count != 1 else ''} including {sample}. "
        f"{disease['treatment_overview'][:80]}..."
    )


def detect_red_flags(symptom_text):
    text = normalize(symptom_text)
    flags = []
    checks = [
        (["chest pain","chest tightness","left arm pain","jaw pain"], "Possible cardiac event — chest pain with radiation requires immediate evaluation"),
        (["shortness of breath","difficulty breathing","cannot breathe"], "Acute respiratory distress — monitor oxygen saturation immediately"),
        (["confusion","disoriented","unconscious","unresponsive"], "Altered level of consciousness — neurological emergency"),
        (["sudden severe headache","worst headache"], "Thunderclap headache — rule out subarachnoid haemorrhage"),
        (["blood in stool","blood in urine","vomiting blood","coughing blood"], "Active bleeding detected — requires urgent investigation"),
        (["suicidal","want to die","end my life","self harm"], "Mental health crisis — immediate psychiatric evaluation required"),
        (["high fever","fever above 40","temperature 40"], "Hyperpyrexia — fever above 40°C requires emergency management"),
        (["severe abdominal pain","rigid abdomen","board-like abdomen"], "Acute abdomen — possible surgical emergency"),
    ]
    for triggers, message in checks:
        if any(t in text for t in triggers):
            flags.append(message)
    return flags


def generate_summary(diagnoses, symptom_text, age, sex):
    if not diagnoses:
        return "No conditions could be matched with the provided symptom profile. Please provide more detailed symptom information."
    top = diagnoses[0]
    count = len(diagnoses)
    age_str = f" A {age}-year-old" if age else "The patient"
    sex_str = f" {sex}" if sex else ""
    return (
        f"{age_str}{sex_str} presents with symptoms most consistent with {top['name']} "
        f"({top['probability']}% probability match). "
        f"A total of {count} differential diagnoses have been identified and ranked by symptom overlap. "
        f"The top condition has an urgency level of '{top['urgency']}'. "
        f"Clinical correlation and professional medical evaluation are strongly recommended."
    )


def analyze_symptoms(symptoms, age, sex, medical_history, medications, allergies, duration_val, duration_unit):
    results = []
    for disease in DISEASES:
        scored = score_disease(disease, symptoms, age, sex, medical_history, medications, allergies)
        if scored:
            results.append(scored)

    results.sort(key=lambda x: x["probability"], reverse=True)
    top = results[:6]

    red_flags = detect_red_flags(symptoms)
    summary   = generate_summary(top, symptoms, age, sex)

    all_lifestyle = []
    seen = set()
    for d in top[:2]:
        for tip in d.get("lifestyle_advice", []):
            if tip not in seen:
                all_lifestyle.append(tip)
                seen.add(tip)

    emergency_advice = top[0]["when_to_seek_emergency"] if top else "Seek medical attention if symptoms worsen or new symptoms develop."

    for d in top:
        del d["lifestyle_advice"]
        del d["when_to_seek_emergency"]

    return {
        "summary":                summary,
        "red_flags":              red_flags,
        "diagnoses":              top,
        "lifestyle_advice":       all_lifestyle,
        "when_to_seek_emergency": emergency_advice
    }