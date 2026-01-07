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
body { background-color: #0e1117; }
.main-title { font-size: 40px; font-weight: 700; color: #4cc9f0; }
.sub-title { font-size: 16px; color: #c7c7c7; }
.section-title { font-size: 24px; font-weight: 600; margin-top: 10px; }
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
st.sidebar.caption(f"API: {API_URL}")
st.write(f"Using backend API URL: {API_URL}")  # Show for debugging

# ------------------------------------------
# Sidebar
# ------------------------------------------
st.sidebar.markdown("## 📊 GARCH Volatility App")
page = st.sidebar.selectbox("Pages", ["Fit Model", "Predict Volatility"])
st.sidebar.markdown("---")
st.sidebar.caption("Powered by FastAPI + ARCH + Streamlit")

# ------------------------------------------
# Header
# ------------------------------------------
st.markdown('<div class="main-title">GARCH Volatility Modeling Platform</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Professional financial risk forecasting</div>', unsafe_allow_html=True)
st.markdown("---")

# ------------------------------------------
# FIT MODEL
# ------------------------------------------
if page == "Fit Model":
    st.markdown('<div class="section-title">Model Training</div>', unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)

    ticker = st.text_input("Stock Ticker", "AAPL")
    use_new_data = st.checkbox("Fetch latest market data", value=True)
    n_observations = st.number_input("Observations", 50, 5000, 300)
    p = st.number_input("p", 1, 10, 1)
    q = st.number_input("q", 1, 10, 1)

    if st.button("🚀 Train Model"):
        payload = dict(
            ticker=ticker,
            use_new_data=use_new_data,
            n_observations=n_observations,
            p=p,
            q=q
        )

        try:
            response = requests.post(f"{API_URL}/fit", json=payload)
            try:
                data = response.json()
                if data.get("success"):
                    st.success(data["message"])
                else:
                    st.error(data.get("message", "Unknown error"))
            except:
                st.error("Backend returned non-JSON response")
                st.text(response.text)

        except Exception as e:
            st.error(f"Connection error: {e}")

    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------
# PREDICT
# ------------------------------------------
else:
    st.markdown('<div class="section-title">Volatility Forecast</div>', unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)

    ticker = st.text_input("Stock Ticker", "AAPL")
    n_days = st.number_input("Forecast Days", 1, 365, 5)

    if st.button("📊 Generate Forecast"):
        try:
            response = requests.post(f"{API_URL}/predict", json={"ticker": ticker, "n_days": n_days})
            try:
                data = response.json()
                if data.get("success"):
                    df = pd.DataFrame(data["forecast"].items(), columns=["Date", "Volatility"])
                    df["Date"] = pd.to_datetime(df["Date"])
                    df.set_index("Date", inplace=True)
                    st.subheader("Predicted Volatility")
                    st.dataframe(df)
                    st.subheader("Forecast Chart")
                    st.line_chart(df["Volatility"])
                else:
                    st.error(data.get("message", "Unknown error"))
            except:
                st.error("Backend returned non-JSON response")
                st.text(response.text)

        except Exception as e:
            st.error(f"Connection error: {e}")

    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------
# Footer
# ------------------------------------------
st.markdown("---")
st.markdown('<div class="footer">© 2026 | Adembesa Godfrey</div>', unsafe_allow_html=True)
