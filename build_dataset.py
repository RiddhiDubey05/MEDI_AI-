import json
import pandas as pd
import os

# Sample Kaggle-like dataset
df = pd.DataFrame({
    'disease': ['Flu','Cold','Migraine','Food Poisoning'],
    'symptoms': [
        ['fever','cough','fatigue','headache'],
        ['cough','sneezing','sore throat','runny nose'],
        ['headache','nausea','sensitivity to light','dizziness'],
        ['nausea','vomiting','diarrhea','abdominal pain']
    ],
    'severity': ['Moderate','Mild','High','High']
})

disease_data = {}
for idx,row in df.iterrows():
    disease_data[row['disease']] = {
        'symptoms': row['symptoms'],
        'severity': row['severity'],
        'doctor': 'General Physician' if row['severity']=='Mild' else 'Specialist',
        'description': f"{row['disease']} is characterized by {', '.join(row['symptoms'])}.",
        'precautions': ["Rest","Hydrate","Consult doctor"] if row['severity'] != 'Mild' else ["Hydrate","Over-the-counter meds"],
        'accuracy': 90 + idx*2  # simulated Kaggle accuracy
    }

os.makedirs('processed', exist_ok=True)
with open('processed/processed_diseases.json','w',encoding='utf-8') as f:
    json.dump(disease_data,f,ensure_ascii=False,indent=4)

# Initialize empty patient history
with open('processed/patient_history.json','w') as f:
    json.dump({},f)

print("Dataset processed and saved to processed/processed_diseases.json")