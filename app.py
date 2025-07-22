import streamlit as st
import pandas as pd
import joblib
import time
from PIL import Image
import os

# --- Configuration ---
# Set page config
st.set_page_config(
    page_title="💼 Salary Prediction App", # Keep page icon for browser tab
    page_icon="📊",
    layout="centered", # 'centered' or 'wide'
    initial_sidebar_state="collapsed"
)

# Load model (ensure 'model/salary_model.pkl' exists in your project structure)
try:
    model = joblib.load("model/salary_model.pkl")
    # Note: If you see InconsistentVersionWarning, it means the model was saved
    # with a different scikit-learn version. It's recommended to retrain and save
    # your model with the currently installed scikit-learn version to avoid potential issues.
except FileNotFoundError:
    st.error("Error: Model file 'model/salary_model.pkl' not found. Please ensure it's in the correct path.")
    st.stop()

# --- Custom CSS for Professional UI ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif;
        color: #334155; /* Slightly darker slate gray for general text */
    }

    body {
        background-color: #fcfcfc; /* Very subtle off-white background */
        /* New subtle background pattern for texture */
        background-image: url("data:image/svg+xml,%3Csvg width='6' height='6' viewBox='0 0 6 6' xmlns='http://www.w3.org/2000/svg'%3E%3Ccircle cx='3' cy='3' r='0.5' fill='%23e0e7ef' fill-opacity='0.2'/%3E%3C/svg%3E");
        background-repeat: repeat;
        background-size: 6px 6px; /* Adjusted size for the new pattern */
        background-attachment: fixed; /* Keeps pattern fixed when scrolling */
    }

    /* Main app container */
    .stApp {
        background: transparent;
    }

    /* Header styling */
    .header-container {
        text-align: center;
        padding: 4.5rem 0 3.5rem; /* More vertical padding */
        margin-bottom: 2.5rem; /* More space below header */
    }
    .header-title {
        font-size: 4.5rem; /* Larger title */
        font-weight: 800; /* Extra bold */
        color: #1a202c; /* Near black */
        background: -webkit-linear-gradient(45deg, #6b46c1, #4c51bf, #3182ce); /* Vibrant gradient */
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1.2rem; /* More space below title */
        letter-spacing: -0.07em; /* Tighter letter spacing for impact */
    }
    .header-subtitle {
        font-size: 1.8rem; /* Larger subtitle */
        color: #64748b; /* Slate gray for subtitle */
        margin-top: 1.2rem;
        line-height: 1.6;
        max-width: 750px; /* Constrain width for readability */
        margin-left: auto;
        margin-right: auto;
    }

    /* Card-like containers (main Streamlit block) */
    .st-emotion-cache-z5fcl4 { /* Target Streamlit's main block container */
        background-color: #ffffff;
        border-radius: 1.75rem; /* Slightly less rounded, more refined */
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.1), 0 15px 30px -8px rgba(0, 0, 0, 0.05); /* Softer, more subtle shadow */
        padding: 4rem; /* Consistent padding */
        margin-bottom: 3.5rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); /* Smoother transition */
        border: 1px solid #e2e8f0; /* Subtle light border */
    }
    .st-emotion-cache-z5fcl4:hover {
        transform: translateY(-5px); /* Gentle lift on hover */
        box-shadow: 0 30px 60px -15px rgba(0, 0, 0, 0.12), 0 18px 36px -9px rgba(0, 0, 0, 0.06);
    }

    /* Prediction Button styling (New Color) */
    .stButton > button {
        background-color: #0d9488; /* Teal 600 - New primary button color */
        background-image: none; /* Ensure no gradient */
        color: white;
        font-weight: 600; /* Semi-bold */
        padding: 1rem 2.2rem; /* Adjusted padding */
        border-radius: 0.75rem; /* Refined rounded corners */
        border: none;
        transition: all 0.2s ease-in-out;
        box-shadow: 0 6px 12px rgba(13, 148, 136, 0.3); /* Softer shadow matching new color */
        cursor: pointer;
        width: auto;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 0.6rem; /* Space between text and icon */
        font-size: 1.1rem; /* Slightly smaller font for balance */
    }
    .stButton > button:hover {
        background-color: #0f766e; /* Darker teal on hover */
        transform: translateY(-2px); /* Subtle lift */
        box-shadow: 0 8px 16px rgba(13, 148, 136, 0.4);
    }
    .stButton > button:active {
        transform: translateY(0);
        box-shadow: 0 4px 8px rgba(13, 148, 136, 0.2);
    }

    /* Secondary button style (for "Back to Home") */
    .stButton.secondary > button {
        background-color: #f1f5f9; /* Light gray */
        color: #475569; /* Slate gray text */
        box-shadow: none;
        border: none;
        font-size: 0.95rem; /* Slightly smaller */
        padding: 0.7rem 1.4rem;
    }
    .stButton.secondary > button:hover {
        background-color: #e2e8f0; /* Slightly darker gray */
        transform: translateY(-1px);
    }

    /* Input field styling */
    .st-emotion-cache-1cyp85f, .st-emotion-cache-13ejs7j, .st-emotion-cache-1v0mbdj { /* Targets for various input types */
        border-radius: 0.75rem; /* More refined rounded corners */
        border: 1px solid #e2e8f0; /* Slightly darker light border */
        box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.03); /* Very subtle inner shadow */
        padding: 0.8rem 1.1rem; /* Adjusted padding */
        transition: all 0.2s ease-in-out;
        font-size: 1rem;
        color: #334155;
    }
    .st-emotion-cache-1cyp85f:focus-within, .st-emotion-cache-13ejs7j:focus-within, .st-emotion-cache-1v0mbdj:focus-within {
        border-color: #0d9488; /* Teal on focus */
        box-shadow: 0 0 0 3px rgba(13, 148, 136, 0.15); /* Softer focus ring */
    }

    /* Selectbox dropdown arrow */
    .st-emotion-cache-1v0mbdj .st-emotion-cache-1v1w777 { /* Target the dropdown arrow */
        color: #0d9488; /* Color the arrow to match button */
    }

    /* Section titles */
    .section-title {
        font-size: 2.5rem; /* Adjusted font size */
        font-weight: 700; /* Bold */
        color: #1e293b; /* Darker slate for titles */
        margin-top: 5rem; /* More space above */
        margin-bottom: 2.5rem; /* More space below */
        text-align: center;
        position: relative;
        padding-bottom: 0.4rem; /* Reduce padding for less pronounced underline */
    }
    .section-title::after {
        content: '';
        position: absolute;
        left: 50%;
        transform: translateX(-50%);
        bottom: 0;
        width: 70px; /* Shorter underline */
        height: 4px; /* Thinner underline */
        background-image: linear-gradient(to right, #0d9488, #2dd4bf); /* Teal gradient underline */
        border-radius: 2px;
    }

    /* Keyframe for slide-in effect */
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* Content Box for sections (New Color & Animation) */
    .content-section-box {
        background-color: #ffffff; /* Pure white background */
        border-radius: 1.25rem; /* Refined rounded corners */
        padding: 2.5rem; /* Generous padding */
        margin-top: 1.5rem; /* Space below the section title */
        margin-bottom: 3rem; /* Space before the next section title */
        box-shadow: 0 6px 18px rgba(0,0,0,0.03); /* Softer, blurrier shadow */
        border: 1px solid #e2e8f0; /* Subtle light border */
        animation: slideInUp 0.6s ease-out forwards; /* Apply animation */
        opacity: 0; /* Start invisible for animation */
    }
    /* Staggered animation delays */
    .content-section-box:nth-of-type(1) { animation-delay: 0.1s; }
    .content-section-box:nth-of-type(2) { animation-delay: 0.2s; }
    .content-section-box:nth-of-type(3) { animation-delay: 0.3s; }
    .content-section-box:nth-of-type(4) { animation-delay: 0.4s; }
    .content-section-box:nth-of-type(5) { animation-delay: 0.5s; }

    .content-section-box ul, .content-section-box ol {
        padding-left: 2rem; /* Indent lists within the box */
        margin-bottom: 0; /* Remove default bottom margin */
        text-align: left; /* Ensure lists are left-aligned */
    }
    .content-section-box li {
        margin-bottom: 0.7rem; /* Adjust list item spacing */
    }
    .content-section-box strong {
        color: #1e293b; /* Darker bold text for emphasis */
    }


    /* Tip box styling (New Color) */
    .tip-box {
        background-color: #fff7ed; /* Very light orange background */
        border: 1px solid #fed7aa; /* Soft orange border */
        border-left: 6px solid #fdba74; /* More prominent left border */
        padding: 2rem; /* More padding */
        border-radius: 1rem; /* Refined rounded corners */
        margin-top: 2.5rem;
        font-size: 1.05rem; /* Slightly larger font */
        line-height: 1.6;
        color: #9a3412; /* Darker text for contrast */
        box-shadow: 0 4px 10px rgba(0,0,0,0.05); /* Softer shadow */
        animation: slideInUp 0.7s ease-out forwards; /* Apply animation */
        opacity: 0; /* Start invisible for animation */
        animation-delay: 0.6s; /* Delay for tip box */
    }
    .tip-box ul {
        list-style-type: none;
        padding-left: 0;
    }
    .tip-box li {
        margin-bottom: 0.7rem; /* More space between list items */
    }

    /* Footer styling */
    footer {
        visibility: hidden;
    }
    .custom-footer {
        text-align: center;
        padding: 4rem 0 3rem; /* More padding */
        color: #94a3b8; /* Lighter gray for footer text */
        font-size: 0.95rem;
    }
    .custom-footer a {
        color: #0d9488; /* Teal */
        text-decoration: none;
        font-weight: 600;
        transition: color 0.2s ease-in-out;
    }
    .custom-footer a:hover {
        color: #0f766e; /* Darker teal */
    }

    /* Prediction result styling (New Color) */
    .prediction-result {
        background-color: #ecfdf5; /* Light green for success */
        border: 1px solid #34d399; /* Green border */
        color: #065f46; /* Dark green text */
        padding: 2.2rem; /* Adjusted padding */
        border-radius: 1rem; /* Refined rounded corners */
        margin-top: 3rem; /* More space above */
        text-align: center;
        font-size: 2rem; /* Adjusted font size for result */
        font-weight: 700;
        box-shadow: 0 8px 16px rgba(0,0,0,0.08); /* Softer shadow */
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1rem; /* Adjusted space around emoji */
    }
    .prediction-result .emoji {
        font-size: 2.5rem; /* Adjusted emoji size */
    }
    .prediction-error {
        background-color: #fee2e2; /* Light red for error */
        border: 1px solid #ef4444; /* Red border */
        color: #991b1b; /* Dark red text */
        padding: 1.6rem; /* Adjusted padding */
        border-radius: 1rem; /* Refined rounded corners */
        margin-top: 3rem;
        text-align: center;
        font-size: 1.3rem;
        font-weight: 500;
        box-shadow: 0 4px 8px rgba(0,0,0,0.08); /* Softer shadow */
    }

    /* Image styling */
    .stImage {
        display: flex;
        justify-content: center;
        margin-bottom: 3.5rem; /* More space below image */
    }
    .stImage img {
        border-radius: 1.5rem; /* Refined rounded image corners */
        box-shadow: 0 15px 25px -5px rgba(0, 0, 0, 0.08), 0 8px 15px -5px rgba(0, 0, 0, 0.04); /* Softer, more pronounced shadow */
    }

    /* Expander styling */
    .st-emotion-cache-1ft0x26 { /* Target Streamlit's expander header */
        background-color: #f7fafc; /* Very light gray background */
        border-radius: 0.8rem; /* Refined rounded corners */
        padding: 0.9rem 1.2rem; /* Adjusted padding */
        font-weight: 600;
        color: #334155;
        border: 1px solid #e2e8f0;
        transition: all 0.2s ease-in-out;
    }
    .st-emotion-cache-1ft0x26:hover {
        background-color: #edf2f7;
        border-color: #cbd5e0;
    }

    /* Dataframe styling */
    .stDataFrame {
        border-radius: 0.8rem; /* Refined rounded corners */
        overflow: hidden;
        border: 1px solid #e2e8f0; /* Add border to dataframe */
    }

    /* General text styling */
    p, li {
        font-size: 1.08rem; /* Slightly larger base font size */
        line-height: 1.8; /* Adjusted line height for readability */
        color: #4b5563; /* Slate gray for general text */
    }
    strong {
        color: #1f2937; /* Make bold text darker for emphasis */
    }

    /* Streamlit specific adjustments for padding/margin */
    .st-emotion-cache-10qj90z { /* Main content padding */
        padding-top: 0rem;
        padding-bottom: 0rem;
    }
    .st-emotion-cache-1y4pm8v { /* Column padding */
        padding-left: 2rem; /* Adjusted column padding */
        padding-right: 2rem;
    }

    </style>
""", unsafe_allow_html=True)

# --- Navigation State ---
if "page" not in st.session_state:
    st.session_state.page = "home"

def go_to_prediction():
    st.session_state.page = "predict"

def go_to_home():
    st.session_state.page = "home"

# --- HOME PAGE ---
if st.session_state.page == "home":
    st.markdown(
        """
        <div class="header-container">
            <h1 class="header-title">Salary Prediction App</h1>
            <p class="header-subtitle">Predict your potential income based on key professional and demographic factors. Get insights into your career path.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Centered image with improved styling
    st.markdown(
        """
        <div style="display: flex; justify-content: center; margin-bottom: 3.5rem;">
            <img src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png" width="180" style="border-radius: 1.75rem; box-shadow: 0 20px 30px -5px rgba(0, 0, 0, 0.1), 0 10px 15px -5px rgba(0, 0, 0, 0.05);">
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("""
    <div style='text-align:center; font-size:1.15rem; margin-top:10px; color: #475569; line-height: 1.7;'>
        This application uses Machine Learning to predict whether your salary is more than $50K based on your professional profile.<br>
        Built with Streamlit and a trained ML model.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='section-title'>Tech Stack Used</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="content-section-box">
        <ul style="list-style-type: none; padding-left: 0;">
            <li style="margin-bottom: 0.8rem; font-size: 1.1rem;"><strong>ML:</strong> scikit-learn, pandas, joblib</li>
            <li style="margin-bottom: 0.8rem; font-size: 1.1rem;"><strong>Frontend:</strong> Streamlit</li>
            <li style="font-size: 1.1rem;"><strong>Deployment:</strong> Streamlit Cloud</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='section-title'>How It Works</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="content-section-box">
        <ol style="list-style-type: decimal; padding-left: 2.5rem; font-size: 1.1rem; color: #475569;">
            <li style="margin-bottom: 0.8rem;">Enter your professional profile information in the prediction form.</li>
            <li style="margin-bottom: 0.8rem;">Our machine learning model processes your inputs to make a prediction.</li>
            <li>It then predicts whether your annual income is likely to be > $50K or ≤ $50K.</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='section-title'>Key Features</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="content-section-box">
        <ul style="list-style-type: disc; padding-left: 2.5rem; font-size: 1.1rem; color: #475569;">
            <li style="margin-bottom: 0.8rem;">Clean, intuitive, and responsive user interface.</li>
            <li style="margin-bottom: 0.8rem;">Real-time machine learning prediction.</li>
            <li style="margin-bottom: 0.8rem;">User-friendly input form for various demographic and professional factors.</li>
            <li style="margin-bottom: 0.8rem;">Clear display of inputs and prediction results.</li>
            <li>Includes helpful resume tips and career advice.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='section-title'>Model Information</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="content-section-box">
        <ul style="list-style-type: disc; padding-left: 2.5rem; font-size: 1.1rem; color: #475569;">
            <li style="margin-bottom: 0.8rem;"><strong>Dataset:</strong> Based on the <a href="https://archive.ics.uci.edu/ml/datasets/adult" target="_blank" style="color: #0d9488; text-decoration: none;">Adult Census Income dataset</a> (UCI Machine Learning Repository).</li>
            <li style="margin-bottom: 0.8rem;"><strong>Task:</strong> Binary classification (predicting whether income is `>50K` or `≤50K`).</li>
            <li style="margin-bottom: 0.8rem;"><strong>Features:</strong> Utilizes various features such as Age, Education Level, Occupation, Marital Status, and more.</li>
            <li><strong>Algorithms:</strong> The model is trained using a classification algorithm (e.g., Logistic Regression or Random Forest, depending on what's in your `salary_model.pkl`).</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='section-title'>Occupation-wise Salary Distribution</div>", unsafe_allow_html=True)
    chart_image_path = "job_vs_salary_chart.png"
    if os.path.exists(chart_image_path):
        try:
            chart_img = Image.open(chart_image_path)
            st.image(chart_img, caption="Income by Occupation", use_column_width=True)
        except Exception as e:
            st.info(f"Could not load chart image: {e}. Please ensure '{chart_image_path}' is a valid image file.")
    else:
        st.info(f"Chart image '{chart_image_path}' not found. Please ensure it's in the correct directory.")


    st.markdown("<div class='section-title'>Resume Tips & Career Advice</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='tip-box'>
    <ul style="list-style-type: none; padding-left: 0;">
        <li style="margin-bottom: 0.8rem;"><strong>Tailor your resume:</strong> Customize your resume and cover letter for each job application.</li>
        <li style="margin-bottom: 0.8rem;"><strong>Quantify achievements:</strong> Use numbers and data to highlight your accomplishments (e.g., “Improved efficiency by 20%”).</li>
        <li style="margin-bottom: 0.8rem;"><strong>Network actively:</strong> Stay engaged on professional platforms like LinkedIn and attend industry events.</li>
        <li style="margin-bottom: 0.8rem;"><strong>Continuous learning:</strong> Complete relevant online certifications or courses to enhance your skills.</li>
        <li><strong>Practice interview skills:</strong> Regularly prepare for common interview questions and practice mock interviews.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.button("🚀 Start Prediction", on_click=go_to_prediction)

# --- PREDICTION PAGE ---
elif st.session_state.page == "predict":
    st.markdown(
        """
        <div class="header-container">
            <h1 class="header-title">Predict Your Income</h1>
            <p class="header-subtitle">Fill in your details to get a personalized salary prediction.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.button("🔙 Back to Home", on_click=go_to_home, key="back_button", help="Go back to the main page.", type="secondary")

    st.markdown("<br>", unsafe_allow_html=True) # Add some space

    # Input form laid out in two columns for better organization
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Personal & Work Details")
        age = st.number_input("Age", 18, 90, 30, help="Your age in years.")
        workclass = st.selectbox("Workclass", [
            'Private', 'Self-emp-not-inc', 'Local-gov', 'State-gov',
            'Federal-gov', 'Self-emp-inc', 'Without-pay', 'Never-worked'
        ], help="The type of employer or work arrangement.")
        education = st.selectbox("Education Level", [
            'Bachelors', 'HS-grad', '11th', 'Assoc-acdm', 'Some-college', 'Masters',
            '7th-8th', 'Doctorate', 'Prof-school', 'Assoc-voc', '9th', '5th-6th',
            '10th', '1st-4th', 'Preschool', '12th'
        ], help="Your highest level of education attained.")
        marital_status = st.selectbox("Marital Status", [
            'Married-civ-spouse', 'Divorced', 'Never-married',
            'Separated', 'Widowed', 'Married-spouse-absent'
        ], help="Your current marital status.")
        occupation = st.selectbox("Occupation", [
            'Tech-support', 'Craft-repair', 'Other-service', 'Sales', 'Exec-managerial',
            'Prof-specialty', 'Handlers-cleaners', 'Machine-op-inspct', 'Adm-clerical',
            'Farming-fishing', 'Transport-moving', 'Priv-house-serv', 'Protective-serv', 'Armed-Forces'
        ], help="Your primary occupation.")

    with col2:
        st.markdown("### Demographic & Financial Details")
        relationship = st.selectbox("Relationship", [
            'Wife', 'Own-child', 'Husband', 'Not-in-family', 'Other-relative', 'Unmarried'
        ], help="Your relationship status within a family context.")
        race = st.selectbox("Race", [
            'White', 'Black', 'Asian-Pac-Islander', 'Amer-Indian-Eskimo', 'Other'
        ], help="Your racial background.")
        gender = st.selectbox("Gender", ['Male', 'Female'], help="Your gender.")
        hours_per_week = st.slider("Hours per Week", 1, 99, 40, help="Average number of hours worked per week.")
        native_country = st.selectbox("Country", [
            'United-States', 'India', 'Mexico', 'Philippines', 'Germany', 'Canada',
            'England', 'China', 'Cuba', 'Other' # 'Other' for countries not explicitly listed
        ], help="Your country of origin.")
        capital_gain = st.number_input("Capital Gain", value=0, min_value=0, help="Income from investments, excluding salary/wages.")
        capital_loss = st.number_input("Capital Loss", value=0, min_value=0, help="Losses from investments.")

    # Map education level to numerical value as per your model's requirement
    edu_map = {
        'Preschool': 1, '1st-4th': 2, '5th-6th': 3, '7th-8th': 4, '9th': 5, '10th': 6,
        '11th': 7, '12th': 8, 'HS-grad': 9, 'Some-college': 10, 'Assoc-voc': 11,
        'Assoc-acdm': 12, 'Bachelors': 13, 'Masters': 14, 'Prof-school': 15, 'Doctorate': 16
    }
    educational_num = edu_map.get(education, 0) # Default to 0 if education not found

    st.markdown("<br>", unsafe_allow_html=True) # Add some space before the button

    if st.button("🔍 Predict Salary", key="predict_button"):
        # Create a DataFrame for prediction
        input_df = pd.DataFrame([{
            'age': age,
            'workclass': workclass,
            'fnlwgt': 0, # Assuming 'fnlwgt' is a placeholder or not used by model, as it's not an input
            'education': education,
            'educational-num': educational_num,
            'marital-status': marital_status,
            'occupation': occupation,
            'relationship': relationship,
            'race': race,
            'gender': gender,
            'capital-gain': capital_gain,
            'capital-loss': capital_loss,
            'hours-per-week': hours_per_week,
            'native-country': native_country
        }])

        with st.spinner("Analyzing your profile..."):
            time.sleep(1.5) # Simulate processing time
            try:
                prediction = model.predict(input_df)[0]
                label = "> $50K" if prediction == 1 else "≤ $50K"
                emoji = "💰" if prediction == 1 else "📉" # Keep emojis here for visual feedback
                st.markdown(f"<div class='prediction-result'><span class='emoji'>{emoji}</span> **Predicted Income:** {label}</div>", unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f"<div class='prediction-error'>❌ Prediction Error: {e}. Please check your model and inputs.</div>", unsafe_allow_html=True)

        with st.expander("View your inputs"):
            st.dataframe(input_df)

# --- Custom Footer ---
st.markdown("---")
st.markdown("""
<div class="custom-footer">
    Made by <b>Bhavini Joshi</b> with ❤️ ·
    <a href='https://github.com/bhavjsh' target='_blank'>GitHub</a> ·
    <a href='https://linkedin.com/in/bhavjsh/' target='_blank'>LinkedIn</a>
</div>
""", unsafe_allow_html=True)
