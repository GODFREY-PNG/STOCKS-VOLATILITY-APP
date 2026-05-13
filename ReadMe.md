# GARCH Volatility Forecasting Platform

A financial risk forecasting application that predicts stock price volatility using GARCH(p,q) models. Users can train models on any publicly listed stock, generate multi-day volatility forecasts, and compare risk levels across different equities.

---

## What It Does

Stock markets are uncertain. Before making investment decisions, traders and analysts need to understand how volatile — how "risky" — a stock is likely to be in the coming days.

This platform solves that problem by:

- Fetching real historical stock price data from the Alpha Vantage API
- Training a GARCH statistical model that learns how volatility clusters over time
- Generating volatility forecasts for 1 to 30 business days ahead
- Assigning a risk level (Low / Moderate / High) to each forecast
- Allowing side-by-side comparison of two stocks

It is built for finance students, data scientists, quant researchers, and anyone who wants to understand stock risk without relying on black-box tools.

---

## Features

- Train a GARCH(p,q) model on any stock ticker (AAPL, TSLA, MSFT, etc.)
- Fetch live data from Alpha Vantage or use locally cached data
- Forecast volatility across a custom horizon (1–30 days)
- Interactive Plotly charts with colour-coded risk bands
- Automatic risk classification: Low / Moderate / High
- Compare two stocks on the same chart with risk summary
- Download forecast results as a CSV file
- Backend connection status indicator in the sidebar
- AIC and BIC model quality metrics displayed after training
- Dark-themed, professional Streamlit interface

---

## Tech Stack

| Layer     | Technology                          |
|-----------|-------------------------------------|
| Frontend  | Streamlit, Plotly                   |
| Backend   | FastAPI, Uvicorn                    |
| Model     | ARCH library (GARCH implementation) |
| Data      | Alpha Vantage API, Pandas           |
| Storage   | SQLite                              |
| Utilities | Pydantic, Joblib, Python-dotenv     |

---

## Project Structure

```
STOCKS-VOLATILITY-APP/
│
├── Backend/
│   ├── main.py          # FastAPI server — /fit and /predict endpoints
│   ├── model.py         # GarchModel class — training, forecasting, save/load
│   ├── data.py          # AlphaVantageAPI and SQLRepository classes
│   ├── config.py        # Settings loaded from .env file
│   ├── requirements.txt # Backend dependencies
│   └── .env.example     # Template for environment variables
│
├── Frontend/
│   ├── app.py           # Streamlit app — all pages and UI
│   └── requirements.txt # Frontend dependencies
│
├── Visualizations/      # Sample charts from exploratory analysis
├── Garch.ipynb          # Research notebook — model development and testing
└── README.md
```

---

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/GODFREY-PNG/STOCKS-VOLATILITY-APP.git
cd STOCKS-VOLATILITY-APP
```

### 2. Set up environment variables

```bash
cd Backend
cp .env.example .env
```

Open `.env` and add your Alpha Vantage API key:

```
ALPHA_API_KEY=your_api_key_here
DB_NAME=stocks.db
MODEL_DIRECTORY=./models
```

Get a free API key at [alphavantage.co](https://www.alphavantage.co/support/#api-key)

### 3. Install backend dependencies

```bash
cd Backend
pip install -r requirements.txt
```

### 4. Start the FastAPI backend

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`
API docs (auto-generated): `http://localhost:8000/docs`

### 5. Install frontend dependencies

Open a new terminal:

```bash
cd Frontend
pip install -r requirements.txt
```

### 6. Start the Streamlit frontend

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## How to Use

**Step 1 — Train a model**

1. Open the app and navigate to **Train Model** in the sidebar
2. Enter a stock ticker (e.g. `AAPL`)
3. Enable "Fetch latest data" on your first run
4. Set GARCH parameters — start with p=1, q=1
5. Click **Train Model**
6. You will see AIC and BIC scores confirming the model was saved

**Step 2 — Generate a forecast**

1. Navigate to **Forecast** in the sidebar
2. Enter the same ticker
3. Select your forecast horizon (e.g. 5 days)
4. Click **Generate Forecast**
5. View the chart, risk level, and daily breakdown table
6. Download results as CSV if needed

**Step 3 — Compare two stocks (optional)**

1. Navigate to **Compare Stocks**
2. Enter two tickers that both have trained models
3. Select the forecast horizon
4. Click **Compare** to see side-by-side volatility and risk levels

---

## API Endpoints

| Method | Endpoint  | Description                              |
|--------|-----------|------------------------------------------|
| GET    | `/hello`  | Health check                             |
| POST   | `/fit`    | Train a GARCH model for a stock ticker   |
| POST   | `/predict`| Generate a volatility forecast           |

**Example — Train a model:**

```bash
curl -X POST "http://localhost:8000/fit" \
  -H "Content-Type: application/json" \
  -d '{"ticker": "AAPL", "use_new_data": true, "n_observations": 500, "p": 1, "q": 1}'
```

**Example — Get a forecast:**

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"ticker": "AAPL", "n_days": 5}'
```

---

## Sample Visualizations

**Apple daily returns vs 2SD conditional volatility (training set)**

![Apple daily returns vs conditional volatility](Visualizations/Apple%20daily%20returns%20vs%202SD%20conditional%20volatility.png)

**Apple return vs predicted volatility (test data)**

![Apple return vs predicted volatility](Visualizations/Apple%20return%20vs%202SD%20predicted%20volatility%20(test%20data%20plot).png)

**Tesla vs Apple closing prices**

![Tesla vs Apple](Visualizations/Tesla_vs_Apple_Closing_Price.png)

---

## Understanding the Model

GARCH (Generalized Autoregressive Conditional Heteroskedasticity) is a statistical model designed specifically for financial time series. It captures a key pattern in markets: **volatility clustering** — periods of high volatility tend to be followed by more high volatility, and calm periods tend to persist.

The GARCH(1,1) model (the default p=1, q=1) has three parameters:

- **ω (omega)** — the long-run average variance
- **α (alpha)** — how much yesterday's shock affects today's variance
- **β (beta)** — how much yesterday's variance persists into today

The model predicts **conditional volatility** — not whether the price goes up or down, but how much it is expected to move.

---

## Risk Classification

| Level    | Volatility Range | Interpretation                                      |
|----------|-----------------|-----------------------------------------------------|
| 🟢 Low   | < 1.5% per day  | Stable period. Suitable for conservative positions. |
| 🟡 Moderate | 1.5–2.5%  | Normal market conditions.                           |
| 🔴 High  | > 2.5% per day  | Elevated risk. Consider hedging or reduced exposure.|

---

## Future Improvements

- Add user authentication and saved session history
- Support for EGARCH and GJR-GARCH model variants
- Portfolio-level volatility aggregation across multiple stocks
- Email or webhook alerts when volatility crosses a threshold
- Deployment to a cloud platform (Render, Railway, or AWS)
- Historical backtest view showing model accuracy on past data

---

## Author

**Adembesa Godfrey**
Data Scientist

- GitHub: [github.com/GODFREY-PNG](https://github.com/GODFREY-PNG)

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.