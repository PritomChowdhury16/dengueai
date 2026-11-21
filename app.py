
import streamlit as st
import pandas as pd
import joblib
from pathlib import Path

st.set_page_config(
    page_title="DENGUARD AI",
    page_icon="🦟",
    layout="wide"
)

# Project folder
BASE_DIR = Path(__file__).parent

# Load dataset
@st.cache_data
def load_data():
    data = pd.read_csv(BASE_DIR / "data" / "dengue_features.csv")
    data["date"] = pd.to_datetime(data["date"])
    return data

# Load trained models
@st.cache_resource
def load_models():
    return joblib.load(
        BASE_DIR / "models" / "dengue_models.joblib"
    )

df = load_data()
saved_data = load_models()

regression_model = saved_data["regression_model"]
risk_model = saved_data["risk_model"]
features = saved_data["features"]

# Dashboard title


st.title("🦟 DENGUARD AI")
st.subheader("Urban Dengue Early Warning System")

st.caption("AI-powered Ward-Level Dengue Risk Prediction")

st.warning(
    "Historical demonstration only. "
    "Dataset ends on 29 December 2025. "
    "This is not a live 2026 outbreak forecast."
)

# Remove rows without required input features
df = df.dropna(subset=features)

# Sidebar selection
st.sidebar.title("Select Area")

cities = sorted(df["city"].unique())

selected_city = st.sidebar.selectbox(
    "Select City",
    cities
)

city_data = df[df["city"] == selected_city]

wards = sorted(city_data["ward_id"].unique())

selected_ward = st.sidebar.selectbox(
    "Select Ward",
    wards
)

ward_data = city_data[
    city_data["ward_id"] == selected_ward
]

dates = sorted(ward_data["date"].unique())

date_options = [
    pd.Timestamp(d).strftime("%Y-%m-%d")
    for d in dates
]

selected_date = st.sidebar.selectbox(
    "Select Historical Week",
    date_options,
    index=len(date_options) - 1
)

selected_date = pd.to_datetime(selected_date)

# Get selected ward data
row = ward_data[
    ward_data["date"] == selected_date
].iloc[0]

# Prepare model input
input_data = pd.DataFrame(
    [row[features].to_dict()],
    columns=features
)

# Make predictions
predicted_cases = regression_model.predict(
    input_data
)[0]

predicted_cases = max(0, predicted_cases)

predicted_risk = risk_model.predict(
    input_data
)[0]

# Prediction results
st.divider()

st.subheader("Dengue Prediction")

col1, col2, col3 = st.columns(3)

col1.metric("Selected City", selected_city)

col2.metric("Selected Ward", selected_ward)

col3.metric("Forecast Period", "Weeks 2–4")

col4, col5 = st.columns(2)

col4.metric(
    "Predicted Dengue Cases",
    round(predicted_cases, 1)
)

col5.metric(
    "Risk Category",
    predicted_risk
)

st.info(
    "Case count and risk category are produced by "
    "two separately trained models."
)

# Historical actual outcome
if pd.notna(row.get("target_next_2_4w")):
    st.metric(
        "Observed Future Cases (Historical)",
        int(row["target_next_2_4w"])
    )
else:
    st.info(
        "Historical future outcome is not available "
        "for this selected week."
    )

# Weather information
st.divider()

st.subheader("Weather Analysis")

weather_data = pd.DataFrame({
    "Weather Feature": [
        "Rainfall (mm)",
        "Average Temperature (°C)",
        "Maximum Temperature (°C)",
        "Minimum Temperature (°C)",
        "Humidity (%)"
    ],
    "Value": [
        row["rainfall_mm"],
        row["avg_temp_c"],
        row["max_temp_c"],
        row["min_temp_c"],
        row["relative_humidity_pct"]
    ]
})

st.dataframe(weather_data, hide_index=True)

# Rainfall lag chart
st.subheader("Multi-Week Rainfall Analysis")

rainfall_data = pd.DataFrame({
    "Period": [
        "Selected Week",
        "1 Week Ago",
        "2 Weeks Ago",
        "3 Weeks Ago",
        "4 Weeks Ago"
    ],
    "Rainfall (mm)": [
        row["rainfall_mm"],
        row["rainfall_lag_1w"],
        row["rainfall_lag_2w"],
        row["rainfall_lag_3w"],
        row["rainfall_lag_4w"]
    ]
})

st.bar_chart(
    rainfall_data.set_index("Period")
)

# Global feature importance
st.divider()

st.subheader("Main Model Drivers")

importance_data = pd.DataFrame({
    "Feature": features,
    "Importance": risk_model.feature_importances_
})

importance_data = importance_data.sort_values(
    "Importance",
    ascending=False
).head(5)

st.bar_chart(
    importance_data.set_index("Feature")
)

st.caption(
    "Feature importance shows global model reliance. "
    "It does not prove causation or explain an individual prediction."
)

# Footer
st.divider()

st.caption(
    "DENGUARD AI | Machine Learning Prototype | "
    "Historical Data: 2016–2025"
)
