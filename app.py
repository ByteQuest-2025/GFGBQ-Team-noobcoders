import streamlit as st
import pickle
import numpy as np


st.set_page_config(
    page_title="Maitri – Silent Disease Risk Engine",
    layout="wide"
)


if "detected_diseases" not in st.session_state:
    st.session_state.detected_diseases = []

if "selected_disease" not in st.session_state:
    st.session_state.selected_disease = None


st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top, #0f172a, #020617);
    color: white;
}

.header {
    text-align: center;
    padding: 40px 20px;
}
.header h1 {
    font-size: 42px;
}
.header p {
    color: #cbd5f5;
}

.risk-card {
    background: linear-gradient(180deg, #0f172a, #020617);
    border-left: 6px solid;
    padding: 22px;
    border-radius: 16px;
    margin-bottom: 18px;
    box-shadow: 0 12px 30px rgba(0,0,0,0.7);
}
.risk-high { border-color: #ef4444; }
.risk-medium { border-color: #fb923c; }
.risk-ok { border-color: #22c55e; }

.risk-card * {
    color: #e5e7eb !important;
}

.info-box {
    background: #020617;
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px;
    padding: 24px;
    margin-top: 20px;
}

.footer {
    text-align: center;
    color: #94a3b8;
    font-size: 13px;
    margin-top: 50px;
}
</style>
""", unsafe_allow_html=True)


st.markdown("""
<div class="header">
    <h1>🩺 Welcome to Maitri</h1>
    <p><b>Your Health Companion for Early Disease Detection</b></p>
    <p>Detect risks early. Act before symptoms begin.</p>
</div>
""", unsafe_allow_html=True)


@st.cache_resource
def load_model(path):
    with open(path, "rb") as f:
        return pickle.load(f)

def predict_risk(model, features):
    X = np.array(features).reshape(1, -1)
    return round(model.predict_proba(X)[0][1] * 100, 2)


st.sidebar.header("📥 Enter Your Health Details")

age = st.sidebar.number_input("Age", 15, 100)
gender = st.sidebar.selectbox("Gender", [0, 1], format_func=lambda x: "Female" if x == 0 else "Male")
bmi = st.sidebar.number_input("BMI", 10.0, 50.0)
sleep = st.sidebar.slider("Sleep Hours", 0, 12)
screen = st.sidebar.slider("Screen Time (hours)", 0, 15)
stress = st.sidebar.slider("Stress Level (1–10)", 1, 10)
activity = st.sidebar.slider("Physical Activity Level (1–10)", 1, 10)
water = st.sidebar.slider("Water Intake (glasses)", 0, 15)
fatigue = st.sidebar.slider("Fatigue Level (1–10)", 1, 10)
sun = st.sidebar.slider("Sun Exposure (1–10)", 1, 10)
hydration = st.sidebar.slider("Hydration Level (1–10)", 1, 10)
diabetes_score = st.sidebar.slider("Diabetes Risk Score", 0, 100)
anemia = st.sidebar.selectbox("Do you have Anemia?", [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")

analyze = st.sidebar.button("🧠 Analyze My Health")


diseases = {
    "Diabetes": {"model": "diabetes_model.pkl", "features": [bmi, screen, fatigue, age]},
    "Hypertension": {"model": "hypertension_model.pkl", "features": [stress, sleep]},
    "Dyslipidemia": {"model": "dyslipidemia_model.pkl", "features": [fatigue, hydration, activity]},
    "Anemia": {"model": "anemia_model.pkl", "features": [age, gender, bmi, sleep, stress, activity, water, fatigue]},
    "Vitamin D Deficiency": {"model": "vitaminD_model.pkl", "features": [sun, activity, water, hydration]},
    "Early Cardiovascular Risk": {
        "model": "cardio_model.pkl",
        "features": [age, bmi, sleep, screen, stress, activity, fatigue, hydration, diabetes_score, anemia]
    },
    "Chronic Kidney Disease": {
        "model": "kidney_model.pkl",
        "features": [hydration, water, stress, activity, fatigue]
    }
}


disease_info = {
    "Diabetes": {
        "causes": "Insulin resistance, obesity, sedentary lifestyle, genetics.",
        "prevention": "Regular exercise, weight management, balanced diet.",
        "diet": "Whole grains, vegetables, low-sugar foods."
    },
    "Hypertension": {
        "causes": "High salt intake, stress, obesity, inactivity.",
        "prevention": "Low salt diet, exercise, stress control.",
        "diet": "Leafy greens, bananas, oats, low-fat dairy."
    },
    "Dyslipidemia": {
        "causes": "Unhealthy diet, lack of exercise, smoking, genetics.",
        "prevention": "Physical activity, healthy fats, avoid smoking.",
        "diet": "Fruits, vegetables, nuts, omega-3 rich foods."
    },
    "Anemia": {
        "causes": "Iron deficiency, poor nutrition, blood loss.",
        "prevention": "Iron-rich foods, vitamin supplementation.",
        "diet": "Spinach, beetroot, legumes, dates."
    },
    "Vitamin D Deficiency": {
        "causes": "Low sun exposure, poor diet.",
        "prevention": "Sunlight exposure, supplements.",
        "diet": "Milk, eggs, fatty fish."
    },
    "Early Cardiovascular Risk": {
        "causes": "Poor lifestyle, diabetes, stress.",
        "prevention": "Exercise, healthy diet, stress management.",
        "diet": "Low-fat foods, fruits, whole grains."
    },
    "Chronic Kidney Disease": {
        "causes": "Diabetes, hypertension, dehydration.",
        "prevention": "Hydration, BP control, healthy lifestyle.",
        "diet": "Low sodium foods, controlled protein intake."
    }
}


if analyze:
    st.subheader("🧠 Health Risk Analysis")
    st.session_state.detected_diseases = []
    st.session_state.selected_disease = None

    for disease, info in diseases.items():
        model = load_model(info["model"])
        if len(info["features"]) != model.n_features_in_:
            continue

        risk = predict_risk(model, info["features"])

        if risk >= 40:
            st.session_state.detected_diseases.append(disease)
            css = "risk-high" if risk >= 70 else "risk-medium"

            st.markdown(f"""
            <div class="risk-card {css}">
                <h4>{disease}</h4>
                <p><b>Estimated Risk:</b> {risk}%</p>
            </div>
            """, unsafe_allow_html=True)

    if not st.session_state.detected_diseases:
        st.markdown("""
        <div class="risk-card risk-ok">
            <h4>✅ No Major Health Risks Detected</h4>
            <p>Maintain a healthy lifestyle and regular checkups.</p>
        </div>
        """, unsafe_allow_html=True)


if st.session_state.detected_diseases:
    st.subheader("📚 Learn About Detected Conditions")

    cols = st.columns(len(st.session_state.detected_diseases))
    for i, d in enumerate(st.session_state.detected_diseases):
        if cols[i].button(d):
            st.session_state.selected_disease = d

if st.session_state.selected_disease:
    info = disease_info.get(st.session_state.selected_disease)
    if info:
        st.markdown(f"""
        <div class="info-box">
            <h3>{st.session_state.selected_disease}</h3>
            <p><b>Causes:</b> {info['causes']}</p>
            <p><b>Preventive Tips:</b> {info['prevention']}</p>
            <p><b>Recommended Diet:</b> {info['diet']}</p>
        </div>
        """, unsafe_allow_html=True)


st.markdown("""
<div class="footer">
⚠ Educational purpose only. Not a medical diagnosis.<br>
Maitri helps you act early — not replace doctors.
</div>
""", unsafe_allow_html=True)
