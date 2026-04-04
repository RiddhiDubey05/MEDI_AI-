import pandas as pd
import json

out = []
def log(s):
    print(s)
    out.append(str(s))

try:
    log("Reading final_symptoms_to_disease.csv...")
    df_sym = pd.read_csv("archive (4)/final_symptoms_to_disease.csv")
    log(f"Columns: {df_sym.columns.tolist()}")
    log(f"Number of diseases: {df_sym['diseases'].nunique()}")
    log(f"First 10 diseases: {df_sym['diseases'].unique()[:10]}")

    log("\nReading data.csv (sample)...")
    df_data = pd.read_csv("archive (4)/data.csv", nrows=1000)
    
    unique_diseases_data = df_data['diseases'].unique()
    log(f"Data columns (first 20): {df_data.columns.tolist()[:20]}")
    log(f"Total columns: {len(df_data.columns)}")
    log(f"Unique diseases in top 1000 rows: {unique_diseases_data}")
    
    with open("dataset_info.txt", "w") as f:
        f.write("\n".join(out))
    
except Exception as e:
    import traceback
    traceback.print_exc()
