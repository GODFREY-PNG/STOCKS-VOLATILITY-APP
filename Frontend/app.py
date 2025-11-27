import streamlit as st
import requests
import pandas as pd

# ------------------------------------------
# Backend URL
# ------------------------------------------
import os

# Use environment variable if set, otherwise default to localhost
API_URL = os.getenv("API_URL", "http://localhost:8000")


# -------------------------
# Streamlit App Layout
# -------------------------
st.set_page_config(page_title="GARCH Volatility App", layout="wide")

# Header
st.title("GARCH Volatility Model App")
st.markdown("**Designed by:** Data Scientist **Adembesa Godfrey**")
st.markdown("**Tested with backtesting techniques**")

# Sidebar page selector
page = st.sidebar.selectbox("Pages", ["Fit Model", "Predict Volatility"])

# -------------------------
# FIT MODEL PAGE
# -------------------------
if page == "Fit Model":
    st.header("Fit a GARCH Model")

    # User input for model parameters
    ticker = st.text_input("Ticker:", "AAPL")
    use_new_data = st.checkbox("Use new data", value=True)
    n_observations = st.number_input("Number of observations", 50, 5000, 300)
    p = st.number_input("p", 1, 10, 1)
    q = st.number_input("q", 1, 10, 1)

    if st.button("Fit Model"):
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
            st.error(f"Error connecting to backend: {e}")

# -------------------------
# PREDICT VOLATILITY PAGE
# -------------------------
else:
    st.header("Predict Volatility")

    # User input for prediction
    ticker = st.text_input("Ticker:", "AAPL")
    n_days = st.number_input("Days to forecast:", 1, 365, 5)

    if st.button("Predict"):
        payload = {"ticker": ticker, "n_days": n_days}

        try:
            response = requests.post(f"{API_URL}/predict", json=payload).json()
            if response["success"]:
                st.success("Forecast:")

                # Convert forecast dict to DataFrame for plotting
                forecast_dict = response["forecast"]
                forecast_df = pd.DataFrame(list(forecast_dict.items()), columns=["Date", "Volatility"])
                forecast_df["Date"] = pd.to_datetime(forecast_df["Date"])
                forecast_df.set_index("Date", inplace=True)

                # Display forecast table
                st.subheader("Predicted Volatility")
                st.dataframe(forecast_df)

                # Display forecast chart
                st.line_chart(forecast_df["Volatility"])
            else:
                st.error(response["message"])
        except Exception as e:
            st.error(f"Error connecting to backend: {e}")

# -------------------------
# Footer
# -------------------------
st.markdown("---")
st.markdown("**Contact:** godfreyimbindi@gmail.com")
