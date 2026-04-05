# MediAI – Disease Prediction Web App

MediAI is a simple web app I built to predict possible diseases based on symptoms entered by the user. It gives a quick idea of what might be happening and helps decide if medical attention is needed.

---

## What it does

* Takes symptoms as input
* Predicts likely diseases
* Shows results instantly
* Stores basic patient records

---

## Tech Used

* Python
* Flask
* Machine Learning
* HTML, CSS

---

## Project Structure

```id="7bn3kq"
app.py
engine.py
train_model.py
build_dataset.py
templates/
static/
```

---

## How to Run

**1. Clone the repo**

```id="k9f2ds"
git clone https://github.com/RiddhiDubey05/MEDI_AI-.git
```

**2. Go to the folder**

```id="v8p1xm"
cd MEDI_AI-
```

**3. Install dependencies**

```id="s3dfw0"
pip install -r requirements.txt
```

**4. Run the app**

```id="p4mz9q"
python app.py
```

---

## How it works

You enter symptoms → the model checks patterns → predicts the most likely disease → result is shown on screen.

