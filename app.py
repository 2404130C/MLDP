import streamlit as st
import pandas as pd
import joblib
from datetime import datetime

# Set background image using custom CSS
st.markdown(
    """
    <style>
    .stApp {
        background-image: linear-gradient(to top, rgba(0,0,0,0.8), rgba(0,0,0,0.4)), 
                          url("https://www.shutterstock.com/shutterstock/videos/31835581/thumb/1.jpg?ip=x480");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Load trained model
model = joblib.load("hdb_price_model.pkl")

# Title
st.title("HDB Resale Price Predictor")
st.write("Enter your flat's details to predict the resale price.")

# Categorical features
towns = [
    'ANG MO KIO', 'BEDOK', 'BISHAN', 'BUKIT BATOK', 'BUKIT MERAH', 'BUKIT PANJANG',
    'BUKIT TIMAH', 'CENTRAL AREA', 'CHOA CHU KANG', 'CLEMENTI', 'GEYLANG', 'HOUGANG',
    'JURONG EAST', 'JURONG WEST', 'KALLANG/WHAMPOA', 'MARINE PARADE', 'PASIR RIS', 'PUNGGOL',
    'QUEENSTOWN', 'SEMBAWANG', 'SENGKANG', 'SERANGOON', 'TAMPINES', 'TOA PAYOH',
    'WOODLANDS', 'YISHUN'
]
flat_types = [
    '1 ROOM', '2 ROOM', '3 ROOM', '4 ROOM', '5 ROOM', 'EXECUTIVE', 'MULTI-GENERATION'
]
flat_models = [
    '2-room', '3Gen', 'Adjoined flat', 'Apartment', 'DBSS', 'Improved', 'Improved-Maisonette',
    'Maisonette', 'Model A', 'Model A-Maisonette', 'Model A2', 'New Generation',
    'Premium Apartment', 'Premium Apartment Loft', 'Premium Maisonette', 'Simplified',
    'Standard', 'Terrace', 'Type S1', 'Type S2'
]

selected_town = st.selectbox("Town", towns)
selected_type = st.selectbox("Flat Type", flat_types)
selected_model = st.selectbox("Flat Model", flat_models)

# Storey range dropdown (mapped to average values)
storey_options = {
    "01 TO 03": 2, "04 TO 06": 5, "07 TO 09": 8, "10 TO 12": 11
}
selected_storey_range = st.selectbox("Storey Range", list(storey_options.keys()))
storey_avg = storey_options[selected_storey_range]

# Input fields
floor_area = st.slider("Floor Area (sqm)", min_value=31.0, max_value=215.0, value=31.0)
lease_commence = st.slider("Lease Commencement Year", min_value=1960, max_value=2025, value=1960)

# Additional Configurations box for optional features
with st.expander("Additional Configurations"):
    year_config = st.slider(
        "Year of Resale",
        min_value=2017,
        max_value=datetime.now().year + 3,
        value=datetime.now().year,
    )
    year = year_config

# Feature dictionary for input
feature_dict = {
    'floor_area_sqm': floor_area,
    'lease_commence_date': lease_commence,
    'year': year,
    'storey_avg': storey_avg
}

# One-hot encoding for categorical features
for town in towns:
    feature_dict[f'town_{town}'] = (selected_town == town)

for t in flat_types:
    feature_dict[f'flat_type_{t}'] = (selected_type == t)

for m in flat_models:
    feature_dict[f'flat_model_{m}'] = (selected_model == m)

# Convert to DataFrame for prediction
input_df = pd.DataFrame([feature_dict])

# Predict button
if st.button("Predict Resale Price"):
    prediction = model.predict(input_df)
    st.success(f"Estimated Resale Price: ${int(prediction):,}")
