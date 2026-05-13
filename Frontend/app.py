import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import os
from datetime import datetime

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
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
}

/* Dark background */
.stApp {
    background-color: #080c14;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #0d1320;
    border-right: 1px solid #1e2d45;
}

/* Main title */
.main-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 2.2rem;
    font-weight: 600;
    color: #00d4ff;
    letter-spacing: -0.5px;
    line-height: 1.2;
}

.main-subtitle {
    font-size: 0.95rem;
    color: #5a7a9a;
    font-family: 'IBM Plex Mono', monospace;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-top: 4px;
}

/* Metric cards */
.metric-card {
    background: linear-gradient(135deg, #0d1a2e 0%, #112036 100%);
    border: 1px solid #1a3050;
    border-radius: 8px;
    padding: 20px 24px;
    margin-bottom: 12px;
}

.metric-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    color: #4a6a8a;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 6px;
}

.metric-value {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.6rem;
    font-weight: 600;
    color: #e8f4ff;
}

.metric-delta {
    font-size: 0.8rem;
    color: #00b894;
    margin-top: 4px;
}

/* Risk badge */
.risk-low {
    display: inline-block;
    background: rgba(0, 184, 148, 0.15);
    color: #00b894;
    border: 1px solid rgba(0, 184, 148, 0.4);
    padding: 6px 16px;
    border-radius: 4px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.85rem;
    font-weight: 600;
    letter-spacing: 1px;
}

.risk-medium {
    display: inline-block;
    background: rgba(253, 203, 110, 0.15);
    color: #fdcb6e;
    border: 1px solid rgba(253, 203, 110, 0.4);
    padding: 6px 16px;
    border-radius: 4px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.85rem;
    font-weight: 600;
    letter-spacing: 1px;
}

.risk-high {
    display: inline-block;
    background: rgba(255, 118, 117, 0.15);
    color: #ff7675;
    border: 1px solid rgba(255, 118, 117, 0.4);
    padding: 6px 16px;
    border-radius: 4px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.85rem;
    font-weight: 600;
    letter-spacing: 1px;
}

/* Section headers */
.section-header {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    color: #00d4ff;
    text-transform: uppercase;
    letter-spacing: 3px;
    border-bottom: 1px solid #1a3050;
    padding-bottom: 8px;
    margin-bottom: 20px;
    margin-top: 10px;
}

/* Info panel */
.info-panel {
    background: #0d1a2e;
    border-left: 3px solid #00d4ff;
    padding: 14px 18px;
    border-radius: 0 6px 6px 0;
    margin: 12px 0;
    font-size: 0.88rem;
    color: #8aaccc;
    line-height: 1.6;
}

/* Success panel */
.success-panel {
    background: rgba(0, 184, 148, 0.08);
    border-left: 3px solid #00b894;
    padding: 14px 18px;
    border-radius: 0 6px 6px 0;
    margin: 12px 0;
    font-size: 0.88rem;
    color: #00b894;
}

/* Error panel */
.error-panel {
    background: rgba(255, 118, 117, 0.08);
    border-left: 3px solid #ff7675;
    padding: 14px 18px;
    border-radius: 0 6px 6px 0;
    margin: 12px 0;
    font-size: 0.88rem;
    color: #ff7675;
}

/* Forecast table */
.forecast-row {
    display: flex;
    justify-content: space-between;
    padding: 10px 0;
    border-bottom: 1px solid #1a2d45;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.88rem;
}

/* Footer */
.footer {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    color: #2a4060;
    text-align: center;
    letter-spacing: 2px;
    padding-top: 20px;
    border-top: 1px solid #0f1e30;
    margin-top: 40px;
}

/* Divider */
.custom-divider {
    border: none;
    border-top: 1px solid #1a2d45;
    margin: 24px 0;
}

/* Sidebar nav */
.nav-item {
    padding: 10px 14px;
    border-radius: 6px;
    cursor: pointer;
    transition: background 0.2s;
    font-size: 0.9rem;
    color: #6a8aaa;
    font-family: 'IBM Plex Mono', monospace;
}

/* Input label override */
label {
    color: #6a8aaa !important;
    font-size: 0.82rem !important;
    font-family: 'IBM Plex Mono', monospace !important;
    letter-spacing: 1px !important;
}

/* Ticker badge */
.ticker-badge {
    display: inline-block;
    background: rgba(0, 212, 255, 0.1);
    color: #00d4ff;
    border: 1px solid rgba(0, 212, 255, 0.3);
    padding: 4px 12px;
    border-radius: 4px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.1rem;
    font-weight: 600;
    letter-spacing: 2px;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------
# Backend URL
# ------------------------------------------
API_URL = os.getenv("API_URL", "http://localhost:8000")

# ------------------------------------------
# Helper functions
# ------------------------------------------
def get_risk_label(avg_volatility):
    """Return risk level based on average forecast volatility."""
    if avg_volatility < 1.5:
        return "low", "LOW RISK", "🟢"
    elif avg_volatility < 2.5:
        return "medium", "MODERATE RISK", "🟡"
    else:
        return "high", "HIGH RISK", "🔴"

def build_forecast_chart(df, ticker):
    """Build a rich Plotly forecast chart with risk bands."""
    avg = df["Volatility"].mean()
    risk_level, _, _ = get_risk_label(avg)

    color_map = {"low": "#00b894", "medium": "#fdcb6e", "high": "#ff7675"}
    bar_color = color_map[risk_level]

    fig = make_subplots(
        rows=2, cols=1,
        row_heights=[0.7, 0.3],
        shared_xaxes=True,
        vertical_spacing=0.06,
        subplot_titles=("", "")
    )

    # Risk band fills
    fig.add_hrect(y0=0, y1=1.5, fillcolor="rgba(0,184,148,0.06)",
                  line_width=0, row=1, col=1)
    fig.add_hrect(y0=1.5, y1=2.5, fillcolor="rgba(253,203,110,0.06)",
                  line_width=0, row=1, col=1)
    fig.add_hrect(y0=2.5, y1=max(df["Volatility"].max() * 1.4, 4),
                  fillcolor="rgba(255,118,117,0.06)",
                  line_width=0, row=1, col=1)

    # Risk zone lines
    fig.add_hline(y=1.5, line_dash="dot", line_color="rgba(0,184,148,0.4)",
                  line_width=1, row=1, col=1)
    fig.add_hline(y=2.5, line_dash="dot", line_color="rgba(253,203,110,0.4)",
                  line_width=1, row=1, col=1)

    # Bar chart
    fig.add_trace(
        go.Bar(
            x=df.index.strftime("%b %d"),
            y=df["Volatility"],
            marker=dict(
                color=df["Volatility"],
                colorscale=[[0, "#00b894"], [0.5, "#fdcb6e"], [1.0, "#ff7675"]],
                line=dict(width=0),
            ),
            name="Forecast Volatility",
            hovertemplate="<b>%{x}</b><br>Volatility: %{y:.3f}%<extra></extra>",
        ),
        row=1, col=1
    )

    # Line overlay
    fig.add_trace(
        go.Scatter(
            x=df.index.strftime("%b %d"),
            y=df["Volatility"],
            mode="lines+markers",
            line=dict(color="#00d4ff", width=2),
            marker=dict(size=7, color="#00d4ff",
                        line=dict(color="#080c14", width=2)),
            name="Trend",
            hovertemplate="<b>%{x}</b><br>Volatility: %{y:.3f}%<extra></extra>",
        ),
        row=1, col=1
    )

    # Deviation bar (bottom panel)
    avg_val = df["Volatility"].mean()
    deviation = df["Volatility"] - avg_val
    dev_colors = ["#00b894" if v <= 0 else "#ff7675" for v in deviation]

    fig.add_trace(
        go.Bar(
            x=df.index.strftime("%b %d"),
            y=deviation,
            marker_color=dev_colors,
            name="vs Average",
            hovertemplate="<b>%{x}</b><br>Δ from avg: %{y:.3f}%<extra></extra>",
        ),
        row=2, col=1
    )

    fig.update_layout(
        paper_bgcolor="#080c14",
        plot_bgcolor="#0a1020",
        font=dict(family="IBM Plex Mono", color="#5a7a9a", size=11),
        showlegend=False,
        height=480,
        margin=dict(l=10, r=10, t=20, b=10),
        xaxis2=dict(
            showgrid=False,
            tickfont=dict(color="#3a5a7a", size=10),
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#0f1e30",
            tickfont=dict(color="#3a5a7a", size=10),
            title=dict(text="Volatility (%)", font=dict(color="#3a5a7a", size=10)),
        ),
        yaxis2=dict(
            showgrid=True,
            gridcolor="#0f1e30",
            tickfont=dict(color="#3a5a7a", size=10),
            title=dict(text="Δ Avg", font=dict(color="#3a5a7a", size=10)),
            zeroline=True,
            zerolinecolor="#1a3050",
        ),
        bargap=0.25,
        hoverlabel=dict(
            bgcolor="#0d1a2e",
            bordercolor="#1a3050",
            font=dict(family="IBM Plex Mono", color="#e8f4ff"),
        ),
    )

    return fig

def build_comparison_chart(df1, df2, ticker1, ticker2):
    """Build side-by-side comparison chart."""
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df1.index.strftime("%b %d"),
        y=df1["Volatility"],
        mode="lines+markers",
        name=ticker1,
        line=dict(color="#00d4ff", width=2.5),
        marker=dict(size=8, color="#00d4ff"),
        hovertemplate=f"<b>{ticker1}</b><br>%{{x}}<br>Volatility: %{{y:.3f}}%<extra></extra>",
    ))

    fig.add_trace(go.Scatter(
        x=df2.index.strftime("%b %d"),
        y=df2["Volatility"],
        mode="lines+markers",
        name=ticker2,
        line=dict(color="#fd79a8", width=2.5),
        marker=dict(size=8, color="#fd79a8"),
        hovertemplate=f"<b>{ticker2}</b><br>%{{x}}<br>Volatility: %{{y:.3f}}%<extra></extra>",
    ))

    # Risk bands
    fig.add_hrect(y0=0, y1=1.5, fillcolor="rgba(0,184,148,0.04)", line_width=0)
    fig.add_hrect(y0=1.5, y1=2.5, fillcolor="rgba(253,203,110,0.04)", line_width=0)
    fig.add_hrect(y0=2.5, y1=10, fillcolor="rgba(255,118,117,0.04)", line_width=0)

    fig.update_layout(
        paper_bgcolor="#080c14",
        plot_bgcolor="#0a1020",
        font=dict(family="IBM Plex Mono", color="#5a7a9a", size=11),
        legend=dict(
            bgcolor="#0d1a2e",
            bordercolor="#1a3050",
            borderwidth=1,
            font=dict(color="#8aaccc"),
        ),
        height=380,
        margin=dict(l=10, r=10, t=20, b=10),
        yaxis=dict(
            showgrid=True,
            gridcolor="#0f1e30",
            tickfont=dict(color="#3a5a7a", size=10),
            title=dict(text="Volatility (%)", font=dict(color="#3a5a7a", size=10)),
        ),
        xaxis=dict(
            showgrid=False,
            tickfont=dict(color="#3a5a7a", size=10),
        ),
        hoverlabel=dict(
            bgcolor="#0d1a2e",
            bordercolor="#1a3050",
            font=dict(family="IBM Plex Mono", color="#e8f4ff"),
        ),
    )

    return fig

# ------------------------------------------
# Sidebar
# ------------------------------------------
with st.sidebar:
    st.markdown("""
    <div style='padding: 16px 0 8px 0;'>
        <div style='font-family: IBM Plex Mono, monospace; font-size: 0.65rem;
                    color: #2a4a6a; letter-spacing: 3px; text-transform: uppercase;
                    margin-bottom: 4px;'>PLATFORM</div>
        <div style='font-family: IBM Plex Mono, monospace; font-size: 1.1rem;
                    font-weight: 600; color: #00d4ff; letter-spacing: 1px;'>
            GARCH VOLATILITY
        </div>
    </div>
    <hr style='border: none; border-top: 1px solid #1a2d45; margin: 12px 0 20px 0;'>
    """, unsafe_allow_html=True)

    page = st.selectbox(
        "NAVIGATE",
        ["📊 Dashboard", "🔧 Train Model", "🔮 Forecast", "⚖️ Compare Stocks"],
        label_visibility="visible"
    )

    st.markdown("<hr style='border: none; border-top: 1px solid #1a2d45; margin: 20px 0;'>", unsafe_allow_html=True)

    st.markdown(f"""
    <div style='font-family: IBM Plex Mono, monospace; font-size: 0.7rem; color: #2a4a6a;'>
        <div style='margin-bottom: 8px;'>API ENDPOINT</div>
        <div style='color: #3a6a8a; word-break: break-all;'>{API_URL}</div>
    </div>
    """, unsafe_allow_html=True)

    # Connection check
    try:
        r = requests.get(f"{API_URL}/hello", timeout=3)
        if r.status_code == 200:
            st.markdown("""
            <div style='margin-top: 14px; font-family: IBM Plex Mono, monospace;
                        font-size: 0.72rem; color: #00b894;'>
                ● BACKEND CONNECTED
            </div>
            """, unsafe_allow_html=True)
        else:
            raise Exception()
    except:
        st.markdown("""
        <div style='margin-top: 14px; font-family: IBM Plex Mono, monospace;
                    font-size: 0.72rem; color: #ff7675;'>
            ● BACKEND OFFLINE
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style='position: fixed; bottom: 24px; font-family: IBM Plex Mono, monospace;
                font-size: 0.65rem; color: #1a3050; letter-spacing: 1px;'>
        FastAPI · ARCH · Streamlit
    </div>
    """, unsafe_allow_html=True)

# ------------------------------------------
# Header
# ------------------------------------------
col_title, col_time = st.columns([3, 1])
with col_title:
    st.markdown("""
    <div class="main-title">GARCH Volatility Platform</div>
    <div class="main-subtitle">Real-time stock risk forecasting · GARCH(p,q) models</div>
    """, unsafe_allow_html=True)
with col_time:
    st.markdown(f"""
    <div style='text-align: right; padding-top: 14px;'>
        <div style='font-family: IBM Plex Mono, monospace; font-size: 0.68rem;
                    color: #2a4a6a; letter-spacing: 2px; text-transform: uppercase;'>
            {datetime.now().strftime("%d %b %Y")}
        </div>
        <div style='font-family: IBM Plex Mono, monospace; font-size: 1.1rem;
                    color: #3a6a8a; margin-top: 2px;'>
            {datetime.now().strftime("%H:%M")}
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr style='border: none; border-top: 1px solid #1a2d45; margin: 16px 0 28px 0;'>", unsafe_allow_html=True)


# ==============================================================
# PAGE: DASHBOARD
# ==============================================================
if page == "📊 Dashboard":
    st.markdown('<div class="section-header">// SYSTEM OVERVIEW</div>', unsafe_allow_html=True)

    # Quick stats row
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Model Type</div>
            <div class="metric-value" style="font-size:1.1rem;">GARCH(p,q)</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Data Source</div>
            <div class="metric-value" style="font-size:1.1rem;">Alpha Vantage</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Storage</div>
            <div class="metric-value" style="font-size:1.1rem;">SQLite</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Backend</div>
            <div class="metric-value" style="font-size:1.1rem;">FastAPI</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # How to use guide
    st.markdown('<div class="section-header">// HOW TO USE THIS PLATFORM</div>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("""
        <div class="metric-card">
            <div style="font-family: IBM Plex Mono, monospace; font-size: 0.7rem;
                        color: #00d4ff; letter-spacing: 2px; margin-bottom: 14px;">
                STEP 01 — TRAIN MODEL
            </div>
            <div style="font-size: 0.88rem; color: #8aaccc; line-height: 1.7;">
                Go to <b style="color:#e8f4ff;">Train Model</b> in the sidebar.<br>
                Enter a stock ticker (e.g. AAPL, TSLA, MSFT).<br>
                Choose whether to fetch the latest data from the API.<br>
                Set your GARCH parameters (p and q — start with 1,1).<br>
                Click <b style="color:#e8f4ff;">Train Model</b>. The model will be saved automatically.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_b:
        st.markdown("""
        <div class="metric-card">
            <div style="font-family: IBM Plex Mono, monospace; font-size: 0.7rem;
                        color: #00d4ff; letter-spacing: 2px; margin-bottom: 14px;">
                STEP 02 — FORECAST VOLATILITY
            </div>
            <div style="font-size: 0.88rem; color: #8aaccc; line-height: 1.7;">
                Go to <b style="color:#e8f4ff;">Forecast</b> in the sidebar.<br>
                Enter the same ticker you trained the model on.<br>
                Set the number of forecast days (1–30).<br>
                Click <b style="color:#e8f4ff;">Generate Forecast</b>.<br>
                View the volatility chart, risk level, and download the results.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="metric-card" style="margin-top: 4px;">
        <div style="font-family: IBM Plex Mono, monospace; font-size: 0.7rem;
                    color: #00d4ff; letter-spacing: 2px; margin-bottom: 14px;">
            STEP 03 — COMPARE STOCKS (OPTIONAL)
        </div>
        <div style="font-size: 0.88rem; color: #8aaccc; line-height: 1.7;">
            Use the <b style="color:#e8f4ff;">Compare Stocks</b> page to place two tickers side by side.<br>
            Both models must be trained first. You will see which stock carries more forecasted risk over the selected horizon.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">// UNDERSTANDING VOLATILITY</div>', unsafe_allow_html=True)

    col_x, col_y, col_z = st.columns(3)
    with col_x:
        st.markdown("""
        <div class="metric-card" style="border-left: 3px solid #00b894;">
            <div style="font-family: IBM Plex Mono, monospace; font-size: 0.7rem;
                        color: #00b894; letter-spacing: 2px; margin-bottom: 10px;">
                🟢 LOW RISK  &lt; 1.5%
            </div>
            <div style="font-size: 0.84rem; color: #8aaccc; line-height: 1.6;">
                The stock is expected to move less than 1.5% per day.
                Suitable for conservative portfolios.
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col_y:
        st.markdown("""
        <div class="metric-card" style="border-left: 3px solid #fdcb6e;">
            <div style="font-family: IBM Plex Mono, monospace; font-size: 0.7rem;
                        color: #fdcb6e; letter-spacing: 2px; margin-bottom: 10px;">
                🟡 MODERATE  1.5–2.5%
            </div>
            <div style="font-size: 0.84rem; color: #8aaccc; line-height: 1.6;">
                Normal market activity. Standard risk for most equity positions.
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col_z:
        st.markdown("""
        <div class="metric-card" style="border-left: 3px solid #ff7675;">
            <div style="font-family: IBM Plex Mono, monospace; font-size: 0.7rem;
                        color: #ff7675; letter-spacing: 2px; margin-bottom: 10px;">
                🔴 HIGH RISK  &gt; 2.5%
            </div>
            <div style="font-size: 0.84rem; color: #8aaccc; line-height: 1.6;">
                Elevated price swings expected. Exercise caution or hedge positions.
            </div>
        </div>
        """, unsafe_allow_html=True)


# ==============================================================
# PAGE: TRAIN MODEL
# ==============================================================
elif page == "🔧 Train Model":
    st.markdown('<div class="section-header">// MODEL TRAINING</div>', unsafe_allow_html=True)

    col_form, col_info = st.columns([1.6, 1])

    with col_form:
        with st.form("fit_form"):
            ticker = st.text_input("STOCK TICKER", "AAPL",
                                   placeholder="e.g. AAPL, TSLA, MSFT, AMZN").strip().upper()
            use_new_data = st.checkbox("Fetch latest data from Alpha Vantage API", value=True)
            n_observations = st.slider("Number of Observations (trading days)", 50, 2000, 500, 50)

            col_p, col_q = st.columns(2)
            with col_p:
                p = st.number_input("p  (ARCH order)", min_value=1, max_value=10, value=1,
                                    help="Lag order for past squared returns")
            with col_q:
                q = st.number_input("q  (GARCH order)", min_value=1, max_value=10, value=1,
                                    help="Lag order for past conditional variance")

            submitted = st.form_submit_button("🚀 TRAIN MODEL", use_container_width=True)

        if submitted:
            with st.spinner("Training GARCH model..."):
                payload = dict(
                    ticker=ticker,
                    use_new_data=use_new_data,
                    n_observations=n_observations,
                    p=int(p),
                    q=int(q),
                )
                try:
                    response = requests.post(f"{API_URL}/fit", json=payload, timeout=60)
                    data = response.json()
                    if data.get("success"):
                        st.markdown(f"""
                        <div class="success-panel">
                            ✓ Model trained successfully for
                            <span style="color:#e8f4ff; font-weight:600;">{ticker}</span><br><br>
                            {data['message']}
                        </div>
                        """, unsafe_allow_html=True)

                        # Extract and display AIC/BIC if present
                        msg = data.get("message", "")
                        if "AIC" in msg and "BIC" in msg:
                            try:
                                aic_val = msg.split("AIC ")[1].split(",")[0]
                                bic_val = msg.split("BIC ")[1].replace(".", "")
                                mc1, mc2, mc3 = st.columns(3)
                                with mc1:
                                    st.markdown(f"""
                                    <div class="metric-card">
                                        <div class="metric-label">Ticker</div>
                                        <div class="ticker-badge">{ticker}</div>
                                    </div>""", unsafe_allow_html=True)
                                with mc2:
                                    st.markdown(f"""
                                    <div class="metric-card">
                                        <div class="metric-label">AIC Score</div>
                                        <div class="metric-value" style="font-size:1.2rem;">
                                            {float(aic_val):.2f}
                                        </div>
                                        <div class="metric-delta" style="color:#8aaccc;">
                                            Lower is better
                                        </div>
                                    </div>""", unsafe_allow_html=True)
                                with mc3:
                                    st.markdown(f"""
                                    <div class="metric-card">
                                        <div class="metric-label">BIC Score</div>
                                        <div class="metric-value" style="font-size:1.2rem;">
                                            {float(bic_val):.2f}
                                        </div>
                                        <div class="metric-delta" style="color:#8aaccc;">
                                            Lower is better
                                        </div>
                                    </div>""", unsafe_allow_html=True)
                            except Exception:
                                pass
                    else:
                        st.markdown(f"""
                        <div class="error-panel">
                            ✗ Training failed: {data.get('message', 'Unknown error')}
                        </div>
                        """, unsafe_allow_html=True)
                except Exception as e:
                    st.markdown(f"""
                    <div class="error-panel">
                        ✗ Could not reach backend: {e}
                    </div>
                    """, unsafe_allow_html=True)

    with col_info:
        st.markdown("""
        <div class="metric-card">
            <div style="font-family: IBM Plex Mono, monospace; font-size: 0.7rem;
                        color: #00d4ff; letter-spacing: 2px; margin-bottom: 14px;">
                PARAMETER GUIDE
            </div>
            <div style="font-size: 0.84rem; color: #8aaccc; line-height: 1.8;">
                <b style="color:#e8f4ff;">Ticker</b><br>
                Stock symbol listed on a major exchange.
                Examples: AAPL, TSLA, MSFT, GOOGL, AMZN<br><br>
                <b style="color:#e8f4ff;">p (ARCH order)</b><br>
                How many past return shocks the model considers.
                Start with 1.<br><br>
                <b style="color:#e8f4ff;">q (GARCH order)</b><br>
                How many past variance estimates the model uses.
                Start with 1.<br><br>
                <b style="color:#e8f4ff;">Observations</b><br>
                Number of trading days of history to train on.
                500 ≈ 2 years of data.<br><br>
                <b style="color:#e8f4ff;">AIC / BIC</b><br>
                Model quality metrics. Lower values indicate a
                better fitting model.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="info-panel">
            💡 Always fetch fresh data on the first run for a ticker.
            Subsequent runs can use cached data to save API calls.
        </div>
        """, unsafe_allow_html=True)


# ==============================================================
# PAGE: FORECAST
# ==============================================================
elif page == "🔮 Forecast":
    st.markdown('<div class="section-header">// VOLATILITY FORECAST</div>', unsafe_allow_html=True)

    col_form, col_info = st.columns([1, 2.2])

    with col_form:
        with st.form("predict_form"):
            ticker = st.text_input("STOCK TICKER", "AAPL").strip().upper()
            n_days = st.slider("Forecast Horizon (days)", 1, 30, 5)
            submitted = st.form_submit_button("📡 GENERATE FORECAST", use_container_width=True)

    with col_info:
        st.markdown("""
        <div class="info-panel">
            The model must be trained before forecasting. If you see an error,
            go to <b>Train Model</b> first and train a model for this ticker.
        </div>
        """, unsafe_allow_html=True)

    if submitted:
        with st.spinner("Generating volatility forecast..."):
            try:
                response = requests.post(
                    f"{API_URL}/predict",
                    json={"ticker": ticker, "n_days": n_days},
                    timeout=30
                )
                data = response.json()

                if data.get("success"):
                    df = pd.DataFrame(
                        list(data["forecast"].items()),
                        columns=["Date", "Volatility"]
                    )
                    df["Date"] = pd.to_datetime(df["Date"])
                    df.set_index("Date", inplace=True)

                    avg_vol = df["Volatility"].mean()
                    max_vol = df["Volatility"].max()
                    min_vol = df["Volatility"].min()
                    risk_level, risk_label, risk_emoji = get_risk_label(avg_vol)

                    # Summary metrics
                    st.markdown("<br>", unsafe_allow_html=True)
                    m1, m2, m3, m4 = st.columns(4)
                    with m1:
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-label">Ticker</div>
                            <div class="ticker-badge">{ticker}</div>
                        </div>""", unsafe_allow_html=True)
                    with m2:
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-label">Avg Volatility</div>
                            <div class="metric-value">{avg_vol:.3f}%</div>
                        </div>""", unsafe_allow_html=True)
                    with m3:
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-label">Peak Volatility</div>
                            <div class="metric-value" style="color:#ff7675;">{max_vol:.3f}%</div>
                        </div>""", unsafe_allow_html=True)
                    with m4:
                        risk_colors = {"low": "#00b894", "medium": "#fdcb6e", "high": "#ff7675"}
                        rc = risk_colors[risk_level]
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-label">Risk Assessment</div>
                            <div style="font-family: IBM Plex Mono, monospace; font-size: 0.95rem;
                                        font-weight: 600; color: {rc}; margin-top: 6px;">
                                {risk_emoji} {risk_label}
                            </div>
                        </div>""", unsafe_allow_html=True)

                    # Chart
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown('<div class="section-header">// FORECAST CHART</div>',
                                unsafe_allow_html=True)
                    fig = build_forecast_chart(df, ticker)
                    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

                    # Table + download
                    col_tbl, col_dl = st.columns([2, 1])
                    with col_tbl:
                        st.markdown('<div class="section-header">// DAILY BREAKDOWN</div>',
                                    unsafe_allow_html=True)
                        display_df = df.copy()
                        display_df.index = display_df.index.strftime("%A, %d %b %Y")
                        display_df["Volatility"] = display_df["Volatility"].map("{:.4f}%".format)
                        display_df.columns = ["Forecast Volatility"]
                        st.dataframe(display_df, use_container_width=True)

                    with col_dl:
                        st.markdown('<div class="section-header">// EXPORT</div>',
                                    unsafe_allow_html=True)
                        csv = df.copy()
                        csv.index = csv.index.strftime("%Y-%m-%d")
                        csv_data = csv.to_csv()
                        st.download_button(
                            label="⬇ Download CSV",
                            data=csv_data,
                            file_name=f"{ticker}_volatility_forecast_{datetime.now().strftime('%Y%m%d')}.csv",
                            mime="text/csv",
                            use_container_width=True,
                        )
                        st.markdown("""
                        <div class="info-panel" style="margin-top: 12px; font-size:0.8rem;">
                            Export includes dates and daily
                            volatility forecast values in CSV format.
                        </div>
                        """, unsafe_allow_html=True)

                else:
                    st.markdown(f"""
                    <div class="error-panel">
                        ✗ {data.get('message', 'Prediction failed. Train the model first.')}
                    </div>
                    """, unsafe_allow_html=True)

            except Exception as e:
                st.markdown(f"""
                <div class="error-panel">
                    ✗ Could not reach backend: {e}
                </div>
                """, unsafe_allow_html=True)


# ==============================================================
# PAGE: COMPARE STOCKS
# ==============================================================
elif page == "⚖️ Compare Stocks":
    st.markdown('<div class="section-header">// STOCK COMPARISON</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="info-panel">
        Both tickers must have a trained model. Go to <b>Train Model</b> first if needed.
    </div>
    """, unsafe_allow_html=True)

    col_t1, col_t2, col_days = st.columns([1, 1, 1])
    with col_t1:
        ticker1 = st.text_input("TICKER 1", "AAPL").strip().upper()
    with col_t2:
        ticker2 = st.text_input("TICKER 2", "TSLA").strip().upper()
    with col_days:
        n_days_cmp = st.slider("Forecast Horizon (days)", 1, 30, 10, key="cmp_days")

    if st.button("⚖️ COMPARE", use_container_width=False):
        with st.spinner("Fetching forecasts..."):
            try:
                r1 = requests.post(f"{API_URL}/predict",
                                   json={"ticker": ticker1, "n_days": n_days_cmp}, timeout=30)
                r2 = requests.post(f"{API_URL}/predict",
                                   json={"ticker": ticker2, "n_days": n_days_cmp}, timeout=30)
                d1 = r1.json()
                d2 = r2.json()

                if d1.get("success") and d2.get("success"):
                    df1 = pd.DataFrame(list(d1["forecast"].items()), columns=["Date", "Volatility"])
                    df1["Date"] = pd.to_datetime(df1["Date"])
                    df1.set_index("Date", inplace=True)

                    df2 = pd.DataFrame(list(d2["forecast"].items()), columns=["Date", "Volatility"])
                    df2["Date"] = pd.to_datetime(df2["Date"])
                    df2.set_index("Date", inplace=True)

                    avg1 = df1["Volatility"].mean()
                    avg2 = df2["Volatility"].mean()
                    rl1, lb1, em1 = get_risk_label(avg1)
                    rl2, lb2, em2 = get_risk_label(avg2)

                    rc = {"low": "#00b894", "medium": "#fdcb6e", "high": "#ff7675"}

                    # Comparison metrics
                    st.markdown("<br>", unsafe_allow_html=True)
                    ca, cb, cc, cd = st.columns(4)
                    with ca:
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-label">{ticker1} Avg Vol</div>
                            <div class="metric-value">{avg1:.3f}%</div>
                        </div>""", unsafe_allow_html=True)
                    with cb:
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-label">{ticker1} Risk</div>
                            <div style="font-family: IBM Plex Mono, monospace;
                                        font-size: 0.95rem; font-weight: 600;
                                        color: {rc[rl1]}; margin-top: 8px;">
                                {em1} {lb1}
                            </div>
                        </div>""", unsafe_allow_html=True)
                    with cc:
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-label">{ticker2} Avg Vol</div>
                            <div class="metric-value">{avg2:.3f}%</div>
                        </div>""", unsafe_allow_html=True)
                    with cd:
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-label">{ticker2} Risk</div>
                            <div style="font-family: IBM Plex Mono, monospace;
                                        font-size: 0.95rem; font-weight: 600;
                                        color: {rc[rl2]}; margin-top: 8px;">
                                {em2} {lb2}
                            </div>
                        </div>""", unsafe_allow_html=True)

                    # Winner banner
                    if avg1 < avg2:
                        lower, higher = ticker1, ticker2
                        diff = avg2 - avg1
                    else:
                        lower, higher = ticker2, ticker1
                        diff = avg1 - avg2

                    st.markdown(f"""
                    <div class="success-panel" style="margin: 16px 0;">
                        <b style="color:#e8f4ff;">{lower}</b> is forecasting
                        <b style="color:#e8f4ff;">{diff:.3f}%</b> less daily volatility than
                        <b style="color:#e8f4ff;">{higher}</b> over the next {n_days_cmp} trading days.
                    </div>
                    """, unsafe_allow_html=True)

                    # Chart
                    st.markdown('<div class="section-header">// VOLATILITY COMPARISON CHART</div>',
                                unsafe_allow_html=True)
                    fig = build_comparison_chart(df1, df2, ticker1, ticker2)
                    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

                    # Side-by-side tables
                    st.markdown('<div class="section-header">// DAILY BREAKDOWN</div>',
                                unsafe_allow_html=True)
                    t1_col, t2_col = st.columns(2)
                    with t1_col:
                        st.markdown(f"**{ticker1}**")
                        d1_disp = df1.copy()
                        d1_disp.index = d1_disp.index.strftime("%d %b %Y")
                        d1_disp["Volatility"] = d1_disp["Volatility"].map("{:.4f}%".format)
                        st.dataframe(d1_disp, use_container_width=True)
                    with t2_col:
                        st.markdown(f"**{ticker2}**")
                        d2_disp = df2.copy()
                        d2_disp.index = d2_disp.index.strftime("%d %b %Y")
                        d2_disp["Volatility"] = d2_disp["Volatility"].map("{:.4f}%".format)
                        st.dataframe(d2_disp, use_container_width=True)

                else:
                    if not d1.get("success"):
                        st.markdown(f"""
                        <div class="error-panel">✗ {ticker1}: {d1.get('message')}</div>
                        """, unsafe_allow_html=True)
                    if not d2.get("success"):
                        st.markdown(f"""
                        <div class="error-panel">✗ {ticker2}: {d2.get('message')}</div>
                        """, unsafe_allow_html=True)

            except Exception as e:
                st.markdown(f"""
                <div class="error-panel">✗ Connection error: {e}</div>
                """, unsafe_allow_html=True)


# ------------------------------------------
# Footer
# ------------------------------------------
st.markdown("""
<div class="footer">
    GARCH VOLATILITY PLATFORM &nbsp;·&nbsp; ADEMBESA GODFREY &nbsp;·&nbsp; 2026
</div>
""", unsafe_allow_html=True)