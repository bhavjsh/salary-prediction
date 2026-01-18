Salary Prediction Web Application

This repository contains a Streamlit-based web application that predicts whether an individual’s annual income is greater than $50,000 or less than or equal to $50,000, based on professional and demographic attributes.

The application uses a pre-trained machine learning classification model to deliver real-time predictions through a clean and user-friendly interface.

Features
Interactive User Interface

Clean and responsive UI built using Streamlit.

Real-Time Predictions

Instant salary classification based on user input.

Comprehensive Input Parameters

The model uses the following features:

Age

Workclass

Education

Marital Status

Occupation

Relationship

Race

Gender

Hours per Week

Capital Gain

Capital Loss

Native Country

Model Information

Provides details about the machine learning model and dataset.

Career Guidance

Includes resume tips and general career advice.

Data Visualization

Occupation-wise salary distribution chart (job_vs_salary_chart.png).

Technology Stack
Machine Learning

scikit-learn

pandas

joblib

Frontend

Streamlit

Deployment

Streamlit Cloud

Model Information

The application uses a supervised classification algorithm trained on the Adult Census Income Dataset from the UCI Machine Learning Repository.

Prediction Classes:

Income > $50,000

Income ≤ $50,000

How to Run Locally
1. Clone the Repository
git clone https://github.com/bhavjsh/salary-prediction.git
cd salary-prediction

2. Create a Virtual Environment (Recommended)
python -m venv venv


Activate the environment:

Windows

venv\Scripts\activate


macOS / Linux

source venv/bin/activate

3. Install Dependencies

Create a requirements.txt file:

streamlit
pandas
scikit-learn
joblib
Pillow


Install dependencies:

pip install -r requirements.txt

4. Verify Required Files

Ensure the following files exist:

model/salary_model.pkl
job_vs_salary_chart.png
app.py

5. Run the Application
streamlit run app.py

Deployment

This application can be deployed on Streamlit Cloud by connecting the GitHub repository and selecting app.py as the entry point.

Contributing

Contributions are welcome.

Open an issue for feature requests or bug reports

Submit a pull request for improvements

Author

GitHub: https://github.com/bhavjsh

LinkedIn: https://www.linkedin.com/in/bhavjsh/
