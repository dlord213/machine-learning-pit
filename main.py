from flask import Flask, render_template, request
import pickle
import pandas as pd

# Load the model
with open('./final_model.pkl', 'rb') as file:
    loaded_model = pickle.load(file)

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template('fields.html')


# Predict from submitted form
@app.route("/predict", methods=["POST"])
def predict():
    error = None
    try:
        vip = 1 if request.form.get('is_vip') else 0
        gender = 0 if request.form.get('gender') == 'Male' else 1

        # Construct input DataFrame
        data = pd.DataFrame([{
            'Income': int(request.form['income']),
            'Children': int(request.form['children']),
            'Age': int(request.form['age']),
            'Attractiveness': int(request.form['attractiveness']),
            'PurchasedVIP': vip,
            'Gender': gender
        }])

        # Prediction
        predictions = loaded_model.predict(data)
        matches = predictions[0]

        # Render template with result
        return render_template('index.html', person={
            "name": request.form['name'],
            "age": int(request.form['age']),
            "income": request.form['income'],
            "is_vip": bool(request.form.get('is_vip')),
            "children": request.form['children'],
            "attractiveness": int(request.form['attractiveness']),
            "gender": request.form['gender'],
            "bio": request.form.get('bio', "")
        }, matches=matches)

    except Exception as e:
        error = str(e)
        return render_template('index.html', person=None, matches=None, error=error)

