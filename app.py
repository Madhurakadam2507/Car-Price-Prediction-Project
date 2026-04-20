

# -------- IMPORT LIBRARIES --------
import streamlit as st
import pandas as pd
import pickle as pkl
import base64
import os

# Safe PDF import
try:
    from reportlab.pdfgen import canvas
    pdf_enabled = True
except ImportError:
    pdf_enabled = False

# -------- PAGE CONFIGURATION --------
st.set_page_config(
    page_title="Car Price Predictor",
    page_icon="🚗",
    layout="wide"
)

# -------- LOAD ML MODEL + DATASET --------
pipe = pkl.load(open("CPP.pkl", "rb"))
ds = pd.read_csv("clean_data.csv")

# -------- FUNCTION: CONVERT IMAGE TO BASE64 --------
def get_base64(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# -------- BACKGROUND IMAGE --------
bg_image = get_base64("my car.jpg")

# -------- CUSTOM CSS / UI DESIGN --------
st.markdown(f"""
<style>
html, body, [class*="css"] {{
    color: white;
}}

.stApp {{
    background: linear-gradient(rgba(10,18,32,0.65), rgba(10,18,32,0.65)),
                url("data:image/jpg;base64,{bg_image}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

.hero-banner {{
    text-align: center;
    padding: 20px 0 30px 0;
}}

.hero-title {{
    font-size: 3.8rem;
    font-weight: 800;
    background: linear-gradient(90deg, #38BDF8, #06B6D4, #8B5CF6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 4px 18px rgba(0,0,0,0.4);
}}

.hero-subtitle {{
    font-size: 1.2rem;
    color: rgba(255,255,255,0.95);
    margin-top: 8px;
}}

label {{
    color: white !important;
    font-weight: 600;
}}

.stSelectbox div[data-baseweb="select"] > div,
.stNumberInput input {{
    background: rgba(15,23,42,0.65) !important;
    color: white !important;
    border-radius: 16px !important;
    border: 1px solid rgba(255,255,255,0.18) !important;
}}

div[role="listbox"] {{
    background: rgba(15,23,42,0.94) !important;
    border-radius: 18px !important;
}}

li[role="option"] {{
    color: white !important;
}}

.stButton > button {{
    display: block;
    margin: auto;
    width: 260px;
    height: 70px;
    border-radius: 18px;
    border: 2px solid rgba(255,255,255,0.35);
    background: linear-gradient(135deg, #111827, #000000) !important;
    color: white !important;
    font-size: 20px;
    font-weight: 700;
    text-align: center;
    white-space: nowrap;
    box-shadow: 0 8px 24px rgba(0,0,0,0.35);
    transition: all 0.3s ease;
}}

.stButton > button:hover {{
    transform: translateY(-3px) scale(1.03);
    box-shadow: 0 12px 30px rgba(6,182,212,0.35);
    border: 2px solid #06B6D4;
}}

.result-box {{
    background: linear-gradient(135deg, rgba(0,0,0,0.72), rgba(17,24,39,0.78));
    border-radius: 18px;
    padding: 24px;
    text-align: center;
    font-size: 26px;
    font-weight: 700;
    color: white;
    margin-top: 20px;
}}

section[data-testid="stSidebar"] {{
    background: rgba(15,23,42,0.92);
}}

section[data-testid="stSidebar"] * {{
    color: white !important;
}}

.info-box {{
    background: rgba(255,255,255,0.08);
    padding: 15px;
    border-radius: 15px;
    margin-top: 15px;
    color: white;
}}
</style>
""", unsafe_allow_html=True)

# -------- SIDEBAR --------
st.sidebar.title("🚘 Explore App")
st.sidebar.markdown("""
### 🌟 Features:
- 🔍 Predict resale car price instantly
- 📊 ML based smart estimation
- 📄 Download PDF report
- 🚗 Multiple car brands supported
- ⛽ Fuel type wise analysis
""")

info_option = st.sidebar.radio(
    "📌 Learn More",
    ["How it Works", "Supported Features", "Tips"]
)

if info_option == "How it Works":
    st.sidebar.markdown("""
    <div class='info-box'>
    This app uses a trained Machine Learning model.<br><br>
    Enter:
    - Company<br>
    - Car Model<br>
    - Year<br>
    - KM Driven<br>
    - Fuel Type<br><br>
    and get an estimated resale price.
    </div>
    """, unsafe_allow_html=True)

elif info_option == "Supported Features":
    st.sidebar.markdown("""
    <div class='info-box'>
    ✔ Premium UI<br>
    ✔ Real-time prediction<br>
    ✔ Download PDF report<br>
    ✔ Attractive design<br>
    ✔ Easy to use
    </div>
    """, unsafe_allow_html=True)

elif info_option == "Tips":
    st.sidebar.markdown("""
    <div class='info-box'>
    💡 Enter accurate details for better prediction.<br><br>
    💡 Check KM driven carefully.<br><br>
    💡 Choose correct fuel type.
    </div>
    """, unsafe_allow_html=True)

# -------- HERO SECTION --------
st.markdown("""
<div class='hero-banner'>
    <div class='hero-title'>🚗 Car Price Predictor</div>
    <div class='hero-subtitle'>
       welcome...
    </div>
</div>
""", unsafe_allow_html=True)

# -------- MAIN FORM --------
companies = sorted(ds["company"].dropna().unique())
company = st.selectbox("🏢 Select Company", companies)

names = sorted(ds[ds["company"] == company]["name"].dropna().unique())
name = st.selectbox("🚘 Select Model", names)

col1, col2 = st.columns(2)

with col1:
    year = st.number_input("📅 Year", min_value=1995, max_value=2025, step=1)

with col2:
    kms_driven = st.number_input("🛣️ KM Driven", min_value=0, step=100)

fuel_types = sorted(ds["fuel_type"].dropna().unique())
fuel_type = st.selectbox("⛽ Fuel Type", fuel_types)

# -------- SPACE BEFORE BUTTON --------
st.markdown("<br><br><br><br>", unsafe_allow_html=True)

# -------- CENTER BUTTON --------
left, center, right = st.columns([1, 2, 1])

with center:
    predict_btn = st.button("🔍 Predict Price")

# -------- PREDICTION --------
if predict_btn:
    input_df = pd.DataFrame(
        [[name, company, year, kms_driven, fuel_type]],
        columns=['name', 'company', 'year', 'kms_driven', 'fuel_type']
    )

    with st.spinner("Analyzing car details..."):
        result = pipe.predict(input_df)

    price = int(result.flatten()[0])

    # Show result
    st.markdown(
        f"<div class='result-box'>💰 Estimated Price: ₹ {price:,}</div>",
        unsafe_allow_html=True
    )

    # Save history
    history_file = "prediction_history.csv"

    new_data = pd.DataFrame([{
        "Company": company,
        "Model": name,
        "Year": year,
        "KM Driven": kms_driven,
        "Fuel Type": fuel_type,
        "Predicted Price": price
    }])

    if os.path.exists(history_file):
        old_data = pd.read_csv(history_file)
        updated_data = pd.concat([old_data, new_data], ignore_index=True)
    else:
        updated_data = new_data

    updated_data.to_csv(history_file, index=False)

    # PDF Report
    if pdf_enabled:
        pdf_file = "car_price_report.pdf"

        c = canvas.Canvas(pdf_file)
        c.setFont("Helvetica-Bold", 20)
        c.drawString(140, 800, "Car Price Prediction Report")

        c.setFont("Helvetica", 13)
        c.drawString(100, 740, f"Company: {company}")
        c.drawString(100, 710, f"Model: {name}")
        c.drawString(100, 680, f"Year: {year}")
        c.drawString(100, 650, f"KM Driven: {kms_driven}")
        c.drawString(100, 620, f"Fuel Type: {fuel_type}")

        c.setFont("Helvetica-Bold", 15)
        c.drawString(100, 570, f"Estimated Price: ₹ {price:,}")

        c.setFont("Helvetica-Oblique", 10)
        c.drawString(100, 500, "Generated using Car Price Predictor")

        c.save()

        with open(pdf_file, "rb") as pdf:
            st.download_button(
                label="📄 Download Prediction Report (PDF)",
                data=pdf,
                file_name="car_price_report.pdf",
                mime="application/pdf"
            )
    else:
        st.warning("PDF download unavailable. Install ReportLab: pip install reportlab")

    st.success("Prediction saved in prediction_history.csv")

# -------- FOOTER --------
st.markdown(
    "<p style='text-align:center; color:white; margin-top:30px;'>Thank You </p>",
    unsafe_allow_html=True
)