from flask import Flask, render_template, request, redirect, url_for
import joblib
import pandas as pd
import numpy as np


df = pd.read_csv('knn_adult.csv')


app = Flask(__name__)

# Load model and features
model = joblib.load('salary_model.pkl')
model_features = joblib.load('model_features.pkl')

# Mock job suggestion list
job_suggestions = [
    "Data Analyst", "Software Developer", "Project Manager", "HR Specialist",
    "Marketing Manager", "Financial Advisor", "Business Analyst"
]

# Resume tips
resume_tips = [
    "Tailor your resume to each job.",
    "Use clear section headings.",
    "Quantify achievements with numbers.",
    "Keep it concise and relevant.",
    "Proofread to avoid grammatical errors."
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        age = int(request.form['age'])
        education_num = int(request.form['education_num'])
        capital_gain = float(request.form['capital_gain'])
        capital_loss = float(request.form['capital_loss'])
        hours_per_week = int(request.form['hours_per_week'])

        categorical_fields = ['workclass', 'education', 'marital_status', 'occupation',
                              'relationship', 'race', 'gender', 'native_country']
        input_data = {
            'age': [age],
            'educational-num': [education_num],
            'capital-gain': [capital_gain],
            'capital-loss': [capital_loss],
            'hours-per-week': [hours_per_week]
        }

        # Add one-hot encoded categorical features
        for field in categorical_fields:
            value = request.form[field]
            key = f"{field.replace('_', '-')}_{value}"
            input_data[key] = [1]

        # Fill missing features with 0
        df_input = pd.DataFrame(columns=model_features)
        df_input.loc[0] = 0  # initialize with zeros

        for feature in input_data:
            if feature in df_input.columns:
                df_input.at[0, feature] = input_data[feature][0]

        prediction = model.predict(df_input)[0]
        result = "> $50K" if prediction == 1 else "<= $50K"

        return render_template("result.html",
                               result=result,
                               suggestions=job_suggestions[:5],
                               resume_tips=resume_tips[:5])
    except Exception as e:
        return f"An error occurred: {e}"

@app.route('/visualize')
def visualize():
    predicted_salary = 65000  # mock prediction value
    average_salary = 52000  # mock average

    return render_template("visualize.html",
                           predicted_salary=predicted_salary,
                           average_salary=average_salary)

if __name__ == '__main__':
    app.run(debug=True)
