import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"  # your local FastAPI URL

st.title("GARCH Model App")

page = st.sidebar.selectbox("Pages", ["Fit Model", "Predict Volatility"])

# -------------------------
# FIT MODEL PAGE
# -------------------------
if page == "Fit Model":
    st.header("Fit a GARCH Model")

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

                # -------------------------
                # Display historical data plot
                # -------------------------
                # Request historical data from FastAPI backend
                data_response = requests.get(f"{API_URL}/hello").json()  # placeholder if you have endpoint to fetch data
                # For now we fetch directly from AlphaVantage API if endpoint exists
                # If backend exposes a /data endpoint, replace this with actual endpoint

                # Example: simulate fetching last n_observations of close prices
                # This assumes your backend stores data in SQLite and you can fetch it
                try:
                    import sqlite3
                    from config import settings
                    from data import SQLRepository

                    conn = sqlite3.connect(settings.db_name, check_same_thread=False)
                    repo = SQLRepository(conn)
                    df = repo.read_table(ticker, limit=n_observations)
                    st.subheader("Historical Close Prices")
                    st.line_chart(df["close"])
                except Exception as e:
                    st.warning(f"Could not load historical prices for plot: {e}")

            else:
                st.error(response["message"])
        except Exception as e:
            st.error(f"Error connecting to API: {e}")

# -------------------------
# PREDICT PAGE
# -------------------------
else:
    st.header("Predict Volatility")

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
            st.error(f"Error connecting to API: {e}")
