import streamlit as st
import requests
import pandas as pd
import os

# ------------------------------------------
# Page Configuration
# ------------------------------------------
st.set_page_config(
    page_title="GARCH Volatility Platform",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------------------------
# Custom CSS Styling
# ------------------------------------------
st.markdown("""
<style>
body {
    background-color: #0e1117;
}
.main-title {
    font-size: 40px;
    font-weight: 700;
    color: #4cc9f0;
}
.sub-title {
    font-size: 16px;
    color: #c7c7c7;
}
.section-title {
    font-size: 24px;
    font-weight: 600;
    margin-top: 10px;
}
.card {
    background-color: #1c1f26;
    padding: 25px;
    border-radius: 12px;
    margin-bottom: 20px;
}
.footer {
    text-align: center;
    color: #888;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------
# Backend URL
# ------------------------------------------
API_URL = os.getenv("API_URL", "http://localhost:8000")

# ------------------------------------------
# Sidebar
# ------------------------------------------
st.sidebar.markdown("## 📊 GARCH Volatility App")
st.sidebar.markdown("Professional risk modeling platform")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    ["📈 Fit Model", "🔮 Predict Volatility"]
)

st.sidebar.markdown("---")
st.sidebar.caption("Powered by FastAPI + ARCH + Streamlit")

# ------------------------------------------
# Header
# ------------------------------------------
st.markdown('<div class="main-title">GARCH Volatility Modeling Platform</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">A professional financial volatility forecasting system using GARCH models</div>',
    unsafe_allow_html=True
)
st.markdown("---")

# ------------------------------------------
# FIT MODEL PAGE
# ------------------------------------------
if page == "📈 Fit Model":
    st.markdown('<div class="section-title">Model Training</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            ticker = st.text_input("Stock Ticker", "AAPL")
            use_new_data = st.checkbox("Fetch latest market data", value=True)
            n_observations = st.number_input("Number of observations", 50, 5000, 300)

        with col2:
            p = st.number_input("GARCH p (ARCH term)", 1, 10, 1)
            q = st.number_input("GARCH q (GARCH term)", 1, 10, 1)

        if st.button("🚀 Train Model", use_container_width=True):
            payload = {
                "ticker": ticker,
                "use_new_data": use_new_data,
                "n_observations": n_observations,
                "p": p,
                "q": q
            }

            try:
                response = requests.post(f"{API_URL}/fit", json=payload).json()
                if response["success"]:
                    st.success(response["message"])
                else:
                    st.error(response["message"])
            except Exception as e:
                st.error(f"Backend connection error: {e}")

        st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------
# PREDICT PAGE
# ------------------------------------------
else:
    st.markdown('<div class="section-title">Volatility Forecast</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)

        col1, col2 = st.columns([2, 1])

        with col1:
            ticker = st.text_input("Stock Ticker", "AAPL")

        with col2:
            n_days = st.number_input("Forecast Horizon (days)", 1, 365, 5)

        if st.button("📊 Generate Forecast", use_container_width=True):
            payload = {"ticker": ticker, "n_days": n_days}

            try:
                response = requests.post(f"{API_URL}/predict", json=payload).json()
                if response["success"]:
                    forecast_df = pd.DataFrame(
                        response["forecast"].items(),
                        columns=["Date", "Volatility"]
                    )
                    forecast_df["Date"] = pd.to_datetime(forecast_df["Date"])
                    forecast_df.set_index("Date", inplace=True)

                    st.subheader("Predicted Volatility")
                    st.dataframe(forecast_df, use_container_width=True)

                    st.subheader("Forecast Chart")
                    st.line_chart(forecast_df["Volatility"])

                else:
                    st.error(response["message"])
            except Exception as e:
                st.error(f"Backend connection error: {e}")

        st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------
# Footer
# ------------------------------------------
st.markdown("---")
st.markdown(
    '<div class="footer">© 2026 | Developed by <b>Adembesa Godfrey</b> | '
    'Financial Risk & Volatility Modeling</div>',
    unsafe_allow_html=True
)
