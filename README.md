Overview
This Streamlit web application predicts whether an individual's annual income is > $50,000 or ≤ $50,000, based on professional and demographic factors. It uses a pre-trained machine learning model for real-time predictions via an intuitive UI.

Features
Interactive UI: Clean, responsive interface built with Streamlit.

Real-time Predictions: Instant salary predictions.

Comprehensive Inputs: Collects age, workclass, education, marital status, occupation, relationship, race, gender, hours per week, capital gain/loss, and native country.

Model Info: Details on the ML model and dataset.

Career Tips: Resume and general career advice.

Visualizations: Occupation-wise salary distribution chart (job_vs_salary_chart.png).

🛠️ Tech Stack
ML: scikit-learn, pandas, joblib

Frontend: Streamlit

Deployment: Streamlit Cloud

📊 Model Information
The model is a classification algorithm trained on the Adult Census Income dataset (UCI Machine Learning Repository) to predict >50K or ≤50K income.

🚀 How to Run Locally
Clone: git clone https://github.com/bhavjsh/salary-prediction.git && cd salary-prediction

Virtual Env (Recommended): python -m venv venv (then activate)

Install Packages: Create requirements.txt (see below) and pip install -r requirements.txt

Files: Ensure salary_model.pkl is in model/ and job_vs_salary_chart.png is in the root.

Run: streamlit run app.py

requirements.txt content:
streamlit
pandas
scikit-learn
joblib
Pillow

☁️ Deployment
Easily deployable on Streamlit Cloud by connecting your GitHub repository.

🤝 Contributing
Contributions are welcome! Open an issue or submit a pull request for improvements.


📧 Contact
Bhavini Joshi

GitHub Profile https://github.com/bhavjsh

LinkedIn Profile https://www.linkedin.com/in/bhavjsh/
