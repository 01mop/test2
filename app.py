# financial_terminal.py
# ------------------------------------------------------------
# Tableau de bord financier type terminal avec Streamlit
# ------------------------------------------------------------
# Installation :
# pip install streamlit yfinance pandas numpy plotly ta
#
# Lancement :
# streamlit run financial_terminal.py
# ------------------------------------------------------------

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# ------------------------------------------------------------
# CONFIGURATION STREAMLIT
# ------------------------------------------------------------

st.set_page_config(
    page_title="Financial Terminal",
    page_icon="📈",
    layout="wide",
)

st.title("📈 Financial Terminal Dashboard")
st.markdown("Terminal financier interactif avec données de marché en temps réel")

# ------------------------------------------------------------
# SIDEBAR
# ------------------------------------------------------------

st.sidebar.header("⚙️ Paramètres")

default_tickers = ["AAPL", "MSFT", "GOOGL", "AMZN"]

tickers_input = st.sidebar.text_input(
    "Tickers (séparés par des virgules)",
    value=",".join(default_tickers)
)

tickers = [ticker.strip().upper() for ticker in tickers_input.split(",")]

period = st.sidebar.selectbox(
    "Période",
    ["1mo", "3mo", "6mo", "1y", "2y", "5y", "10y"],
    index=3
)

interval = st.sidebar.selectbox(
    "Intervalle",
    ["1d", "1wk", "1mo"],
    index=0
)

ma_short = st.sidebar.slider(
    "Moyenne mobile courte",
    min_value=5,
    max_value=50,
    value=20
)

ma_long = st.sidebar.slider(
    "Moyenne mobile longue",
    min_value=20,
    max_value=200,
    value=50
)

rsi_window = st.sidebar.slider(
    "Fenêtre RSI",
    min_value=5,
    max_value=30,
    value=14
)

bb_window = st.sidebar.slider(
    "Fenêtre Bandes de Bollinger",
    min_value=10,
    max_value=50,
    value=20
)

# ------------------------------------------------------------
# FONCTIONS TECHNIQUES
# ------------------------------------------------------------

@st.cache_data
def load_data(tickers, period, interval):
    data = yf.download(
        tickers=tickers,
        period=period,
        interval=interval,
        auto_adjust=True,
        progress=False
    )
    return data


def calculate_rsi(series, window=14):
    delta = series.diff()

    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)

    gain = pd.Series(gain, index=series.index)
    loss = pd.Series(loss, index=series.index)

    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi


def add_indicators(df):
    df = df.copy()

    df["MA_SHORT"] = df["Close"].rolling(ma_short).mean()
    df["MA_LONG"] = df["Close"].rolling(ma_long).mean()

    # RSI
    df["RSI"] = calculate_rsi(df["Close"], rsi_window)

    # Bollinger Bands
    rolling_mean = df["Close"].rolling(bb_window).mean()
    rolling_std = df["Close"].rolling(bb_window).std()

    df["BB_UPPER"] = rolling_mean + (rolling_std * 2)
    df["BB_LOWER"] = rolling_mean - (rolling_std * 2)

    return df


# ------------------------------------------------------------
# CHARGEMENT DES DONNÉES
# ------------------------------------------------------------

data = load_data(tickers, period, interval)

if len(tickers) == 1:
    close_prices = pd.DataFrame(data["Close"])
    close_prices.columns = tickers
else:
    close_prices = data["Close"]

# ------------------------------------------------------------
# PANNEAU PRINCIPAL
# ------------------------------------------------------------

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Analyse Technique",
    "💰 Fondamentaux",
    "🔥 Corrélations",
    "📋 Données"
])

# ------------------------------------------------------------
# TAB 1 - ANALYSE TECHNIQUE
# ------------------------------------------------------------

with tab1:

    selected_ticker = st.selectbox(
        "Sélectionnez un ticker",
        tickers
    )

    ticker_data = yf.download(
        selected_ticker,
        period=period,
        interval=interval,
        auto_adjust=True,
        progress=False
    )

    ticker_data = add_indicators(ticker_data)

    latest_price = ticker_data["Close"].iloc[-1]
    previous_price = ticker_data["Close"].iloc[-2]
    pct_change = ((latest_price - previous_price) / previous_price) * 100

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Dernier Prix",
        f"${latest_price:.2f}",
        f"{pct_change:.2f}%"
    )

    col2.metric(
        "RSI",
        f"{ticker_data['RSI'].iloc[-1]:.2f}"
    )

    col3.metric(
        "Volume",
        f"{ticker_data['Volume'].iloc[-1]:,.0f}"
    )

    # --------------------------------------------------------
    # GRAPHIQUE PRINCIPAL
    # --------------------------------------------------------

    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.08,
        row_heights=[0.7, 0.3]
    )

    # Candlestick
    fig.add_trace(
        go.Candlestick(
            x=ticker_data.index,
            open=ticker_data["Open"],
            high=ticker_data["High"],
            low=ticker_data["Low"],
            close=ticker_data["Close"],
            name="Prix"
        ),
        row=1,
        col=1
    )

    # Moyennes mobiles
    fig.add_trace(
        go.Scatter(
            x=ticker_data.index,
            y=ticker_data["MA_SHORT"],
            name=f"MA {ma_short}",
            line=dict(width=1.5)
        ),
        row=1,
        col=1
    )

    fig.add_trace(
        go.Scatter(
            x=ticker_data.index,
            y=ticker_data["MA_LONG"],
            name=f"MA {ma_long}",
            line=dict(width=1.5)
        ),
        row=1,
        col=1
    )

    # Bollinger Bands
    fig.add_trace(
        go.Scatter(
            x=ticker_data.index,
            y=ticker_data["BB_UPPER"],
            name="BB Upper",
            line=dict(dash="dot")
        ),
        row=1,
        col=1
    )

    fig.add_trace(
        go.Scatter(
            x=ticker_data.index,
            y=ticker_data["BB_LOWER"],
            name="BB Lower",
            line=dict(dash="dot"),
            fill="tonexty"
        ),
        row=1,
        col=1
    )

    # RSI
    fig.add_trace(
        go.Scatter(
            x=ticker_data.index,
            y=ticker_data["RSI"],
            name="RSI"
        ),
        row=2,
        col=1
    )

    fig.add_hline(
        y=70,
        line_dash="dash",
        line_color="red",
        row=2,
        col=1
    )

    fig.add_hline(
        y=30,
        line_dash="dash",
        line_color="green",
        row=2,
        col=1
    )

    fig.update_layout(
        title=f"{selected_ticker} - Analyse Technique",
        height=800,
        xaxis_rangeslider_visible=False,
        template="plotly_dark"
    )

    st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------------------------
# TAB 2 - FONDAMENTAUX
# ------------------------------------------------------------

with tab2:

    st.subheader("💰 Données Fondamentales")

    fundamentals = []

    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info

            fundamentals.append({
                "Ticker": ticker,
                "Nom": info.get("shortName"),
                "Secteur": info.get("sector"),
                "Industrie": info.get("industry"),
                "Market Cap": info.get("marketCap"),
                "P/E Ratio": info.get("trailingPE"),
                "Dividend Yield": info.get("dividendYield"),
                "Beta": info.get("beta"),
                "52W High": info.get("fiftyTwoWeekHigh"),
                "52W Low": info.get("fiftyTwoWeekLow"),
                "ROE": info.get("returnOnEquity"),
                "Marge Profit": info.get("profitMargins"),
            })

        except Exception as e:
            st.warning(f"Erreur pour {ticker}: {e}")

    fundamentals_df = pd.DataFrame(fundamentals)

    st.dataframe(
        fundamentals_df,
        use_container_width=True
    )

# ------------------------------------------------------------
# TAB 3 - CORRÉLATIONS
# ------------------------------------------------------------

with tab3:

    st.subheader("🔥 Carte Thermique des Corrélations")

    returns = close_prices.pct_change().dropna()

    corr_matrix = returns.corr()

    heatmap = px.imshow(
        corr_matrix,
        text_auto=True,
        aspect="auto",
        color_continuous_scale="RdBu_r",
        title="Corrélation des Rendements"
    )

    heatmap.update_layout(
        template="plotly_dark",
        height=700
    )

    st.plotly_chart(heatmap, use_container_width=True)

    st.subheader("📈 Rendements Cumulés")

    cumulative_returns = (1 + returns).cumprod()

    perf_fig = go.Figure()

    for col in cumulative_returns.columns:
        perf_fig.add_trace(
            go.Scatter(
                x=cumulative_returns.index,
                y=cumulative_returns[col],
                mode="lines",
                name=col
            )
        )

    perf_fig.update_layout(
        title="Performance Relative des Actifs",
        template="plotly_dark",
        height=600
    )

    st.plotly_chart(perf_fig, use_container_width=True)

# ------------------------------------------------------------
# TAB 4 - DONNÉES
# ------------------------------------------------------------

with tab4:

    st.subheader("📋 Données Historiques")

    st.dataframe(
        close_prices.tail(100),
        use_container_width=True
    )

    csv = close_prices.to_csv().encode("utf-8")

    st.download_button(
        label="📥 Télécharger CSV",
        data=csv,
        file_name="market_data.csv",
        mime="text/csv"
    )

# ------------------------------------------------------------
# FOOTER
# ------------------------------------------------------------

st.markdown("---")
st.caption(
    "Données fournies par Yahoo Finance via yfinance | "
    "Dashboard Streamlit type terminal financier"
)
