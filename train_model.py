import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

def main():
    df = pd.read_csv('dataset.csv')
    X = df.drop('disease', axis=1)
    y = df['disease']
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    joblib.dump(model, 'model.pkl')
    joblib.dump(X.columns.tolist(), 'columns.pkl')

if __name__ == '__main__':
    main()
