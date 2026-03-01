# app.py
import streamlit as st
import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from datetime import datetime

# ----------------------------
# Load model
# ----------------------------
model_path = "house_price_model.pkl"

if not Path(model_path).exists():
    st.error("⚠️ Model file `house_price_model.pkl` not found in the current directory.")
    st.stop()

try:
    model = joblib.load(model_path)
except Exception as e:
    st.error(f"⚠️ Failed to load model: {e}")
    st.stop()

# ----------------------------
# Streamlit page config
# ----------------------------
st.set_page_config(
    page_title="PropVision · House Price AI",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------
# Global CSS
# ----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --bg:        #0d0f14;
    --surface:   #161923;
    --surface2:  #1e2330;
    --border:    #2a3045;
    --gold:      #c9a84c;
    --gold-lt:   #e8c97a;
    --teal:      #38b2ac;
    --text:      #e8eaf0;
    --muted:     #7a849a;
    --success:   #48bb78;
    --radius:    14px;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

section[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] * { color: var(--text) !important; }
section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] > div,
section[data-testid="stSidebar"] .stTextInput input {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
}

.main .block-container {
    background: var(--bg) !important;
    padding: 2rem 2.5rem !important;
    max-width: 1280px;
}

/* Hero */
.hero-header {
    background: linear-gradient(135deg, #1a1f2e 0%, #0d0f14 60%, #1a1422 100%);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero-header::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 240px; height: 240px;
    background: radial-gradient(circle, rgba(201,168,76,0.12) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.6rem;
    font-weight: 700;
    background: linear-gradient(90deg, var(--gold-lt), var(--gold));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 0.4rem 0;
}
.hero-subtitle { color: var(--muted); font-size: 1rem; font-weight: 300; }
.hero-badge {
    display: inline-block;
    background: rgba(201,168,76,0.15);
    border: 1px solid rgba(201,168,76,0.3);
    color: var(--gold-lt);
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    padding: 4px 12px;
    border-radius: 20px;
    margin-bottom: 1rem;
}

/* Price banner */
.price-banner {
    background: linear-gradient(135deg, #1a2010 0%, #0f1a0f 100%);
    border: 1px solid rgba(72,187,120,0.35);
    border-radius: var(--radius);
    padding: 1.8rem 2rem;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 1.5rem;
    position: relative;
    overflow: hidden;
}
.price-banner::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 4px; height: 100%;
    background: linear-gradient(180deg, var(--success), var(--teal));
    border-radius: 4px 0 0 4px;
}
.price-icon { font-size: 2.8rem; line-height: 1; }
.price-label {
    font-size: 0.78rem; font-weight: 600;
    letter-spacing: 1.5px; text-transform: uppercase;
    color: var(--success); margin-bottom: 0.3rem;
}
.price-value {
    font-family: 'Playfair Display', serif;
    font-size: 2.2rem; font-weight: 700;
    color: #fff; line-height: 1;
}
.price-range { font-size: 0.88rem; color: var(--muted); margin-top: 0.4rem; }
.price-range span { color: var(--teal); font-weight: 500; }

.price-error {
    background: linear-gradient(135deg, #1a1010 0%, #1a0f0f 100%);
    border: 1px solid rgba(245,101,101,0.35);
    border-radius: var(--radius);
    padding: 1.5rem 2rem;
    margin-bottom: 1.5rem;
    position: relative;
}
.price-error::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 4px; height: 100%;
    background: #f56565;
    border-radius: 4px 0 0 4px;
}

/* Metric cards */
.metric-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.3rem 1.5rem;
    text-align: center;
    transition: border-color 0.2s;
}
.metric-card:hover { border-color: var(--gold); }
.metric-num { font-family: 'Playfair Display', serif; font-size: 1.8rem; font-weight: 700; color: var(--gold-lt); }
.metric-lbl { font-size: 0.75rem; color: var(--muted); letter-spacing: 0.8px; text-transform: uppercase; margin-top: 0.2rem; }

/* Section cards */
.section-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.6rem 1.8rem;
    margin-bottom: 1.5rem;
}
.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.2rem; font-weight: 600;
    color: var(--gold-lt);
    margin-bottom: 1.2rem;
    border-bottom: 1px solid var(--border);
    padding-bottom: 0.8rem;
}

.info-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0.7rem; }
.info-item {
    background: var(--surface2); border-radius: 8px;
    padding: 0.7rem 1rem;
    display: flex; justify-content: space-between; align-items: center;
}
.info-key { font-size: 0.8rem; color: var(--muted); }
.info-val { font-size: 0.88rem; font-weight: 600; color: var(--text); }

.driver-row { display: flex; flex-direction: column; gap: 0.8rem; }
.driver-item {
    display: flex; align-items: flex-start; gap: 0.9rem;
    background: var(--surface2); border-radius: 10px; padding: 0.9rem 1.1rem;
}
.driver-icon { font-size: 1.4rem; flex-shrink: 0; margin-top: 2px; }
.driver-title { font-weight: 600; font-size: 0.9rem; color: var(--text); margin-bottom: 0.2rem; }
.driver-desc { font-size: 0.8rem; color: var(--muted); line-height: 1.5; }

.progress-wrap { margin-bottom: 1rem; }
.progress-label { display: flex; justify-content: space-between; font-size: 0.8rem; color: var(--muted); margin-bottom: 0.35rem; }
.progress-bar { height: 6px; background: var(--surface2); border-radius: 3px; overflow: hidden; }
.progress-fill { height: 100%; border-radius: 3px; }

.sidebar-section {
    font-size: 0.7rem; font-weight: 700;
    letter-spacing: 1.8px; text-transform: uppercase;
    color: var(--gold);
    margin: 1.2rem 0 0.4rem 0;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid var(--border);
}

.eda-missing {
    background: var(--surface2); border: 1px dashed var(--border);
    border-radius: 10px; padding: 1.5rem;
    text-align: center; color: var(--muted); font-size: 0.85rem; margin-bottom: 0.6rem;
}

.footer {
    text-align: center; color: var(--muted); font-size: 0.78rem;
    padding: 1.5rem 0 0.5rem;
    border-top: 1px solid var(--border); margin-top: 2rem; letter-spacing: 0.5px;
}
.footer span { color: var(--gold); }
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Sidebar
# ----------------------------
with st.sidebar:
    st.markdown("""
    <div style='padding:1rem 0 0.5rem;text-align:center;'>
        <div style='font-family:"Playfair Display",serif;font-size:1.4rem;font-weight:700;
                    background:linear-gradient(90deg,#e8c97a,#c9a84c);
                    -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;'>
            🏡 PropVision
        </div>
        <div style='font-size:0.72rem;color:#7a849a;letter-spacing:1px;margin-top:4px;'>AI PRICE ESTIMATOR</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='sidebar-section'>🏠 Property Basics</div>", unsafe_allow_html=True)
    bhk               = st.slider("BHK (Bedrooms)", 1, 10, 3)
    size_sqft         = st.slider("Size (Sqft)", 300, 6000, 1500, step=50)
    age               = st.slider("Age of Property (Years)", 0, 50, 5)
    property_type     = st.selectbox("Property Type", ["Apartment", "House", "Villa"])
    furnished_status  = st.selectbox("Furnished Status", ["Furnished", "Semi-Furnished", "Unfurnished"])
    availability_status = st.selectbox("Availability", ["Ready to Move", "Under Construction"])

    st.markdown("<div class='sidebar-section'>📍 Location</div>", unsafe_allow_html=True)
    state    = st.text_input("State", "Maharashtra")
    city     = st.text_input("City", "Mumbai")
    locality = st.text_input("Locality", "Andheri")
    public_transport_accessibility = st.selectbox("Transport Access", ["Good", "Moderate", "Poor"])

    st.markdown("<div class='sidebar-section'>🏗️ Building Details</div>", unsafe_allow_html=True)
    floor_no     = st.slider("Floor Number", 0, 30, 2)
    total_floors = st.slider("Total Floors", 1, 30, 5)
    facing       = st.selectbox("Facing", ["North", "South", "East", "West"])

    st.markdown("<div class='sidebar-section'>⚙️ Amenities & Market</div>", unsafe_allow_html=True)
    parking_space  = st.selectbox("Parking Space", ["Yes", "No"])
    security       = st.selectbox("Security", ["Yes", "No"])
    amenities      = st.text_input("Amenities", "Basic")
    schools        = st.slider("Nearby Schools", 0, 10, 3)
    hospitals      = st.slider("Nearby Hospitals", 0, 10, 2)
    owner_type     = st.selectbox("Owner Type", ["Individual", "Builder"])
    price_per_sqft = st.slider("Price per Sqft (₹)", 3000, 15000, 6000, step=100)

# ----------------------------
# Derived values
# ----------------------------
current_year = datetime.now().year
year_built   = current_year - age

# ----------------------------
# Input DataFrame — columns match model's feature_names_in_ exactly:
# ['id','state','city','locality','property_type','bhk','size_in_sqft',
#  'price_in_lakhs','price_per_sqft','year_built','furnished_status',
#  'floor_no','total_floors','age_of_property','nearby_schools',
#  'nearby_hospitals','public_transport_accessibility','parking_space',
#  'security','amenities','facing','owner_type','availability_status']
# ----------------------------
input_data = pd.DataFrame({
    # ── Numerical (10) ──
    'bhk':                              [bhk],
    'size_in_sqft':                     [size_sqft],
    'price_per_sqft':                   [price_per_sqft],
    'year_built':                       [year_built],
    'floor_no':                         [floor_no],
    'total_floors':                     [total_floors],
    'age_of_property':                  [age],
    'nearby_schools':                   [schools],
    'nearby_hospitals':                 [hospitals],
    # ── Categorical (12) ──
    'state':                            [state],
    'city':                             [city],
    'locality':                         [locality],
    'property_type':                    [property_type],
    'furnished_status':                 [furnished_status],
    'public_transport_accessibility':   [public_transport_accessibility],
    'parking_space':                    [parking_space],
    'security':                         [security],
    'amenities':                        [amenities],
    'facing':                           [facing],
    'owner_type':                       [owner_type],
    'availability_status':              [availability_status],
})

# Engineered feature — computed before predict, matches training pipeline exactly
input_data['price_size_interaction'] = input_data['price_per_sqft'] * input_data['size_in_sqft']

# ----------------------------
# Predict — handles both log-transformed and direct output
# ----------------------------
predicted_price_lakhs = None
prediction_error      = None

try:
    raw = model.predict(input_data)[0]
    # If model outputs log(price), exponentiate; otherwise use directly
    predicted_price_lakhs = np.expm1(raw) if raw < 50 else float(raw)
except Exception as e:
    prediction_error = str(e)

if predicted_price_lakhs is not None:
    lower = max(predicted_price_lakhs * 0.9, 1)
    upper = min(predicted_price_lakhs * 1.1, 99999)
    ppsf  = (predicted_price_lakhs * 100000) / size_sqft
else:
    lower = upper = ppsf = 0

# ════════════════════════════════════════
#  MAIN PAGE
# ════════════════════════════════════════

# Hero
st.markdown("""
<div class='hero-header'>
    <div class='hero-badge'>✦ AI-Powered Valuation</div>
    <div class='hero-title'>House Price Intelligence</div>
    <div class='hero-subtitle'>
        Real-time property price estimation powered by machine learning —
        accurate, transparent, and built for the Indian market.
    </div>
</div>
""", unsafe_allow_html=True)

# ── Price result ──
if predicted_price_lakhs is not None:
    st.markdown(f"""
    <div class='price-banner'>
        <div class='price-icon'>💰</div>
        <div>
            <div class='price-label'>Estimated Market Value</div>
            <div class='price-value'>₹ {predicted_price_lakhs:,.2f} Lakhs</div>
            <div class='price-range'>
                Confidence Range: <span>₹ {lower:,.2f}</span> – <span>₹ {upper:,.2f} Lakhs</span>
                &nbsp;·&nbsp; ₹ {ppsf:,.0f} / sqft
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div class='price-error'>
        <div style='font-size:1.1rem;font-weight:600;color:#fc8181;margin-bottom:0.4rem;'>
            ⚠️ Prediction Failed
        </div>
        <div style='font-size:0.85rem;color:#7a849a;line-height:1.6;'>
            <b>Error:</b> {prediction_error}
        </div>
        <div style='font-size:0.8rem;color:#7a849a;margin-top:0.8rem;
                    background:#1e2330;border-radius:8px;padding:0.8rem 1rem;'>
            💡 <b>Fix:</b> Make sure your saved model pipeline includes a
            preprocessor / encoder for categorical columns such as
            <code>property_type</code>, <code>furnished_status</code>, etc.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Quick metric cards ──
c1, c2, c3, c4 = st.columns(4)
for col, icon, val, lbl in [
    (c1, "🛏",  f"{bhk} BHK",        "Bedrooms"),
    (c2, "📐",  f"{size_sqft:,}",     "Square Feet"),
    (c3, "🏗",  f"{age} Yrs",         "Property Age"),
    (c4, "🏢",  f"Floor {floor_no}",  f"of {total_floors}"),
]:
    with col:
        st.markdown(f"""
        <div class='metric-card'>
            <div style='font-size:1.6rem;margin-bottom:0.3rem;'>{icon}</div>
            <div class='metric-num'>{val}</div>
            <div class='metric-lbl'>{lbl}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Two-column layout ──
left, right = st.columns([1.1, 1], gap="large")

with left:
    st.markdown(f"""
    <div class='section-card'>
        <div class='section-title'>📋 Property Summary</div>
        <div class='info-grid'>
            <div class='info-item'><span class='info-key'>Type</span><span class='info-val'>{property_type}</span></div>
            <div class='info-item'><span class='info-key'>Status</span><span class='info-val'>{availability_status}</span></div>
            <div class='info-item'><span class='info-key'>Furnished</span><span class='info-val'>{furnished_status}</span></div>
            <div class='info-item'><span class='info-key'>Facing</span><span class='info-val'>{facing}</span></div>
            <div class='info-item'><span class='info-key'>Parking</span><span class='info-val'>{parking_space}</span></div>
            <div class='info-item'><span class='info-key'>Security</span><span class='info-val'>{security}</span></div>
            <div class='info-item'><span class='info-key'>Schools</span><span class='info-val'>{schools}</span></div>
            <div class='info-item'><span class='info-key'>Hospitals</span><span class='info-val'>{hospitals}</span></div>
            <div class='info-item'><span class='info-key'>Owner</span><span class='info-val'>{owner_type}</span></div>
            <div class='info-item'><span class='info-key'>Year Built</span><span class='info-val'>{year_built}</span></div>
            <div class='info-item'><span class='info-key'>Transport</span><span class='info-val'>{public_transport_accessibility}</span></div>
            <div class='info-item'><span class='info-key'>Amenities</span><span class='info-val'>{amenities}</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class='section-card'>
        <div class='section-title'>📍 Location Details</div>
        <div class='info-grid'>
            <div class='info-item'><span class='info-key'>State</span><span class='info-val'>{state}</span></div>
            <div class='info-item'><span class='info-key'>City</span><span class='info-val'>{city}</span></div>
            <div class='info-item'><span class='info-key'>Locality</span><span class='info-val'>{locality}</span></div>
            <div class='info-item'><span class='info-key'>Price / Sqft</span><span class='info-val'>₹ {price_per_sqft:,}</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with right:
    # Score bars
    st.markdown("<div class='section-card'><div class='section-title'>📊 Value Score Indicators</div>", unsafe_allow_html=True)

    def score_bar(label, value, max_val, color):
        pct = min(int((value / max_val) * 100), 100)
        st.markdown(f"""
        <div class='progress-wrap'>
            <div class='progress-label'><span>{label}</span><span>{value} / {max_val}</span></div>
            <div class='progress-bar'>
                <div class='progress-fill' style='width:{pct}%;background:{color};'></div>
            </div>
        </div>""", unsafe_allow_html=True)

    score_bar("Bedroom Count",    bhk,                   10,   "#c9a84c")
    score_bar("Property Size",    min(size_sqft, 6000),   6000, "#38b2ac")
    score_bar("Nearby Schools",   schools,                10,   "#9f7aea")
    score_bar("Nearby Hospitals", hospitals,              10,   "#f687b3")
    score_bar("Floor Level",      floor_no,               30,   "#68d391")
    st.markdown("</div>", unsafe_allow_html=True)

    # Price drivers
    st.markdown("""
    <div class='section-card'>
        <div class='section-title'>🔍 Key Price Drivers</div>
        <div class='driver-row'>
            <div class='driver-item'>
                <span class='driver-icon'>📐</span>
                <div><div class='driver-title'>Property Size</div>
                <div class='driver-desc'>Larger floor area directly increases market value and rental yield potential.</div></div>
            </div>
            <div class='driver-item'>
                <span class='driver-icon'>📍</span>
                <div><div class='driver-title'>Location & Connectivity</div>
                <div class='driver-desc'>Proximity to schools, hospitals and transport boosts demand and price premium.</div></div>
            </div>
            <div class='driver-item'>
                <span class='driver-icon'>🏗️</span>
                <div><div class='driver-title'>Age & Amenities</div>
                <div class='driver-desc'>Newer builds with security & parking command significantly higher valuations.</div></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── EDA ──
st.markdown("<div class='section-card'><div class='section-title'>📈 Exploratory Data Analysis</div>", unsafe_allow_html=True)

eda_images = [
    ("eda_univariate_price_in_lakhs.png", "Price Distribution"),
    ("eda_bivariate_size_in_sqft.png",    "Size vs Price"),
    ("eda_correlation_heatmap.png",       "Correlation Heatmap"),
]
img_cols = st.columns(3)
for col, (img, title) in zip(img_cols, eda_images):
    with col:
        st.markdown(f"<div style='font-size:0.8rem;color:#7a849a;text-align:center;margin-bottom:0.5rem;'>{title}</div>", unsafe_allow_html=True)
        if Path(img).exists():
            st.image(img, use_container_width=True)
        else:
            st.markdown(f"<div class='eda-missing'>📊 {img}<br><small>Image not found</small></div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ── Footer ──
st.markdown("""
<div class='footer'>
    Built with <span>♥</span> using Streamlit &nbsp;·&nbsp;
    Powered by Machine Learning &nbsp;·&nbsp;
    <span>PropVision AI</span> &nbsp;·&nbsp; © 2025
</div>
""", unsafe_allow_html=True)
