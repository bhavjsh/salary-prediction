# Salary Prediction Web Application

This repository contains a Streamlit-based web application that predicts whether an individual’s annual income is **greater than $50,000** or **less than or equal to $50,000**, based on professional and demographic attributes.

The application uses a **pre-trained machine learning classification model** to deliver real-time predictions through a clean and user-friendly interface.

---

## Features

### Interactive User Interface
- Clean and responsive UI built using Streamlit.

### Real-Time Predictions
- Instant salary classification based on user input.

### Comprehensive Input Parameters
The model uses the following features:
- Age
- Workclass
- Education
- Marital Status
- Occupation
- Relationship
- Race
- Gender
- Hours per Week
- Capital Gain
- Capital Loss
- Native Country

### Model Information
- Provides details about the machine learning model and dataset.

### Career Guidance
- Includes resume tips and general career advice.

### Data Visualization
- Occupation-wise salary distribution chart (`job_vs_salary_chart.png`).

---

## Technology Stack

### Machine Learning
- scikit-learn
- pandas
- joblib

### Frontend
- Streamlit

### Deployment
- Streamlit Cloud

---

## Model Information

The application uses a supervised classification algorithm trained on the **Adult Census Income Dataset** from the UCI Machine Learning Repository.

**Prediction Classes:**
- Income > $50,000
- Income ≤ $50,000

---

## How to Run Locally

Clone the Repository
git clone https://github.com/bhavjsh/salary-prediction.git
cd salary-prediction

Create a Virtual Environment
python -m venv venv

Activate the environment:

Windows
venv\Scripts\activate

macOS / Linux
source venv/bin/activate

Install Dependencies
pip install -r requirements.txt

Run the Application
streamlit run app.py


Contributions are welcome.
Please open an issue or submit a pull request.

Author
GitHub: https://github.com/bhavjsh
LinkedIn: https://www.linkedin.com/in/bhavjsh/
