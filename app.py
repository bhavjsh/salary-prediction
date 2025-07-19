import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt

# ⚙️ Configuration (must be FIRST Streamlit call)
st.set_page_config(page_title="Salary Prediction App", layout="centered")

# ✅ Load Dataset
try:
    df = pd.read_csv("adult.csv")
    st.success("✅ Dataset loaded successfully!")
except Exception as e:
    st.error(f"❌ Error reading CSV: {e}")
    df = pd.DataFrame()

# ✅ Load Model
try:
    model = joblib.load("model/salary_model.pkl")
    model_features = joblib.load("model/model_features.pkl")
except Exception as e:
    st.error(f"❌ Error loading model or features: {e}")
    model = None
    model_features = []

# 🎯 App Title
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>💼 Salary Prediction App</h1>", unsafe_allow_html=True)
st.markdown("---")

# 📋 Input Form
st.markdown("### 📋 Enter Your Details:")
with st.form("prediction_form"):
    age = st.number_input("Age", min_value=17, max_value=100, value=30)
    education = st.selectbox("Education", sorted(df["education"].dropna().unique()))
    workclass = st.selectbox("Workclass", sorted(df["workclass"].dropna().unique()))
    marital_status = st.selectbox("Marital Status", sorted(df["marital_status"].dropna().unique()))
    occupation = st.selectbox("Occupation", sorted(df["occupation"].dropna().unique()))
    relationship = st.selectbox("Relationship", sorted(df["relationship"].dropna().unique()))
    race = st.selectbox("Race", sorted(df["race"].dropna().unique()))
    sex = st.selectbox("Sex", sorted(df["sex"].dropna().unique()))
    capital_gain = st.number_input("Capital Gain", value=0.0)
    capital_loss = st.number_input("Capital Loss", value=0.0)
    hours_per_week = st.slider("Hours Per Week", 1, 100, 40)

    submitted = st.form_submit_button("🔍 Predict Salary")

# 💡 Suggestions
job_suggestions = ["Data Analyst", "Software Developer", "Project Manager", "HR Specialist", "Marketing Manager"]
resume_tips = [
    "Tailor your resume to each job.",
    "Use clear section headings.",
    "Quantify achievements with numbers.",
    "Keep it concise and relevant.",
    "Proofread to avoid grammatical errors."
]

# 🔍 Prediction Logic
if submitted:
    try:
        # Raw input dictionary
        user_input = {
            "age": age,
            "education": education,
            "workclass": workclass,
            "marital_status": marital_status,
            "occupation": occupation,
            "relationship": relationship,
            "race": race,
            "sex": sex,
            "capital_gain": capital_gain,
            "capital_loss": capital_loss,
            "hours_per_week": hours_per_week
        }

        input_df = pd.DataFrame([user_input])

        # One-hot encode using all possible features from training
        input_encoded = pd.get_dummies(input_df)

        # Align with training model features
        final_input = pd.DataFrame(columns=model_features)
        final_input = final_input.fillna(0)
        for col in input_encoded.columns:
            if col in final_input.columns:
                final_input.at[0, col] = input_encoded[col].values[0]

        # Predict
        prediction = model.predict(final_input)[0]
        result = "> $50K" if prediction == 1 else "<= $50K"

        st.success(f"💰 Predicted Salary Class: **{result}**")

        # 📈 Salary Chart
        st.markdown("### 📊 Salary Comparison")
        predicted_salary = 65000 if prediction == 1 else 35000
        average_salary = 52000
        fig, ax = plt.subplots()
        ax.bar(["Predicted", "Average"], [predicted_salary, average_salary], color=["green", "blue"])
        ax.set_ylabel("Annual Salary (USD)")
        st.pyplot(fig)

        # 💼 Job Suggestions
        st.markdown("### 💼 Job Suggestions")
        st.write(", ".join(job_suggestions))

        # 📝 Resume Tips
        st.markdown("### ✨ Resume Tips")
        for tip in resume_tips:
            st.markdown(f"- {tip}")

    except Exception as e:
        st.error(f"❌ Prediction failed: {e}")

st.markdown("---")
st.markdown("Made with ❤️ by Bhavini Joshi")
