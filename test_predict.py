from app import app
import json

client = app.test_client()

patients = [
    {'text':'I have loose motions and tummy pain','patient':{'name':'Riddhi','age':20,'gender':'Female','conditions':['typhoid']}},
    {'text':'Severe headache and nausea','patient':{'name':'Amit','age':35,'gender':'Male'}},
    {'text':'random text with no sense','patient':{'name':'Unknown'}}
]

results = {}
for i,p in enumerate(patients):
    r = client.post('/predict',json=p)
    results[f'r{i+1}'] = r.get_json()

with open('test_predict_out.json','w') as f:
    json.dump(results,f,indent=2)