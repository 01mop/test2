"""
╔══════════════════════════════════════════════════════════════╗
║          QUANTUM TERMINAL — Financial Dashboard v1.0         ║
║          Streamlit · yfinance · Pandas · Plotly              ║
╚══════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="QUANTUM TERMINAL",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  GLOBAL CSS — Dark terminal aesthetic
# ─────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Space+Mono:ital,wght@0,400;0,700;1,400&family=IBM+Plex+Sans:wght@300;400;600&family=Orbitron:wght@700;900&display=swap');

  /* ── Base ── */
  html, body, [class*="css"] {
      background-color: #090d12 !important;
      color: #c8d8e8 !important;
      font-family: 'IBM Plex Sans', sans-serif;
  }
  .stApp { background-color: #090d12; }

  /* ── Sidebar ── */
  section[data-testid="stSidebar"] {
      background: linear-gradient(180deg, #0c1520 0%, #0a1118 100%) !important;
      border-right: 1px solid #1a2f45;
  }
  section[data-testid="stSidebar"] * { color: #8aafc8 !important; }
  section[data-testid="stSidebar"] .stSelectbox label,
  section[data-testid="stSidebar"] .stMultiSelect label,
  section[data-testid="stSidebar"] .stSlider label { color: #4da8da !important; font-family: 'Space Mono', monospace; font-size: 11px; letter-spacing: 1px; text-transform: uppercase; }

  /* ── Selectbox / Input ── */
  .stSelectbox > div > div,
  .stMultiSelect > div > div {
      background-color: #0f1e2e !important;
      border: 1px solid #1e3a55 !important;
      border-radius: 2px !important;
      color: #4da8da !important;
  }

  /* ── Metric cards ── */
  [data-testid="metric-container"] {
      background: linear-gradient(135deg, #0d1f30 0%, #0a1520 100%);
      border: 1px solid #1a3a55;
      border-left: 3px solid #00d4ff;
      border-radius: 2px;
      padding: 12px 16px;
  }
  [data-testid="metric-container"] label { color: #4da8da !important; font-family: 'Space Mono', monospace; font-size: 10px; letter-spacing: 1.5px; }
  [data-testid="metric-container"] [data-testid="stMetricValue"] { color: #e8f4fd !important; font-family: 'Space Mono', monospace; font-size: 18px; }
  [data-testid="metric-container"] [data-testid="stMetricDelta"] { font-family: 'Space Mono', monospace; font-size: 12px; }

  /* ── Tabs ── */
  .stTabs [data-baseweb="tab-list"] { background: #0c1520; border-bottom: 1px solid #1a3a55; gap: 0; }
  .stTabs [data-baseweb="tab"] { color: #4a7a99; font-family: 'Space Mono', monospace; font-size: 11px; letter-spacing: 1px; padding: 10px 20px; border-bottom: 2px solid transparent; }
  .stTabs [aria-selected="true"] { color: #00d4ff !important; border-bottom: 2px solid #00d4ff !important; background: transparent !important; }

  /* ── DataFrames ── */
  .stDataFrame { border: 1px solid #1a3a55; border-radius: 2px; }
  .stDataFrame th { background-color: #0d1f30 !important; color: #4da8da !important; font-family: 'Space Mono', monospace; font-size: 11px; }
  .stDataFrame td { background-color: #090d12 !important; color: #c8d8e8 !important; font-family: 'Space Mono', monospace; font-size: 12px; }

  /* ── Divider ── */
  hr { border-color: #1a3a55 !important; }

  /* ── Scrollbar ── */
  ::-webkit-scrollbar { width: 4px; }
  ::-webkit-scrollbar-track { background: #090d12; }
  ::-webkit-scrollbar-thumb { background: #1e3a55; border-radius: 2px; }

  /* ── Title banner ── */
  .terminal-header {
      font-family: 'Orbitron', sans-serif;
      font-size: 28px;
      font-weight: 900;
      letter-spacing: 6px;
      color: #00d4ff;
      text-shadow: 0 0 20px rgba(0, 212, 255, 0.4), 0 0 40px rgba(0, 212, 255, 0.1);
      margin: 0;
  }
  .terminal-sub {
      font-family: 'Space Mono', monospace;
      font-size: 10px;
      letter-spacing: 3px;
      color: #2a5a7a;
      margin-top: 2px;
  }
  .section-label {
      font-family: 'Space Mono', monospace;
      font-size: 10px;
      letter-spacing: 2px;
      color: #2a6a8a;
      text-transform: uppercase;
      border-bottom: 1px solid #1a3a55;
      padding-bottom: 4px;
      margin-bottom: 12px;
  }
  .price-badge {
      display: inline-block;
      background: #0d2a3f;
      border: 1px solid #00d4ff;
      color: #00d4ff;
      font-family: 'Space Mono', monospace;
      padding: 2px 10px;
      font-size: 13px;
      border-radius: 2px;
      margin: 2px;
  }
  .up-badge { border-color: #00ff88; color: #00ff88; }
  .dn-badge { border-color: #ff4466; color: #ff4466; }
  .status-dot {
      display: inline-block;
      width: 7px; height: 7px;
      border-radius: 50%;
      background: #00ff88;
      box-shadow: 0 0 8px #00ff88;
      animation: pulse 2s infinite;
      margin-right: 6px;
  }
  @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.4; } }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────
PLOTLY_LAYOUT = dict(
    paper_bgcolor="#090d12",
    plot_bgcolor="#090d12",
    font=dict(family="Space Mono, monospace", color="#8aafc8", size=11),
    xaxis=dict(gridcolor="#0f2035", zerolinecolor="#0f2035", showgrid=True),
    yaxis=dict(gridcolor="#0f2035", zerolinecolor="#0f2035", showgrid=True),
    margin=dict(l=50, r=20, t=40, b=40),
    legend=dict(bgcolor="#0a1520", bordercolor="#1a3a55", borderwidth=1),
)

def color_seq():
    return ["#00d4ff", "#00ff88", "#ffaa00", "#ff4466", "#aa88ff", "#ff88aa", "#44ffdd", "#ffdd44"]

@st.cache_data(ttl=300)
def fetch_data(ticker: str, period: str, interval: str) -> pd.DataFrame:
    try:
        df = yf.download(ticker, period=period, interval=interval, progress=False, auto_adjust=True)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        df.dropna(inplace=True)
        return df
    except Exception:
        return pd.DataFrame()

@st.cache_data(ttl=600)
def fetch_info(ticker: str) -> dict:
    try:
        return yf.Ticker(ticker).info or {}
    except Exception:
        return {}

def compute_indicators(df: pd.DataFrame, sma1: int, sma2: int, ema: int, bb_window: int, rsi_window: int) -> pd.DataFrame:
    close = df["Close"].squeeze()
    df = df.copy()
    df[f"SMA{sma1}"] = close.rolling(sma1).mean()
    df[f"SMA{sma2}"] = close.rolling(sma2).mean()
    df[f"EMA{ema}"]  = close.ewm(span=ema, adjust=False).mean()
    df["BB_mid"]  = close.rolling(bb_window).mean()
    bb_std        = close.rolling(bb_window).std()
    df["BB_up"]   = df["BB_mid"] + 2 * bb_std
    df["BB_dn"]   = df["BB_mid"] - 2 * bb_std
    # RSI
    delta  = close.diff()
    gain   = delta.clip(lower=0).rolling(rsi_window).mean()
    loss   = (-delta.clip(upper=0)).rolling(rsi_window).mean()
    rs     = gain / loss.replace(0, np.nan)
    df["RSI"] = 100 - 100 / (1 + rs)
    # MACD
    ema12  = close.ewm(span=12, adjust=False).mean()
    ema26  = close.ewm(span=26, adjust=False).mean()
    df["MACD"]        = ema12 - ema26
    df["MACD_signal"] = df["MACD"].ewm(span=9, adjust=False).mean()
    df["MACD_hist"]   = df["MACD"] - df["MACD_signal"]
    return df

def fmt_large(val):
    if val is None or (isinstance(val, float) and np.isnan(val)):
        return "N/A"
    if abs(val) >= 1e12: return f"${val/1e12:.2f}T"
    if abs(val) >= 1e9:  return f"${val/1e9:.2f}B"
    if abs(val) >= 1e6:  return f"${val/1e6:.2f}M"
    return f"${val:,.0f}"

def safe(info, key, fmt=None, default="N/A"):
    v = info.get(key)
    if v is None or (isinstance(v, float) and np.isnan(v)): return default
    if fmt: return fmt(v)
    return v

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 16px 0 8px;'>
      <div style='font-family:Orbitron,sans-serif; font-size:16px; font-weight:900;
                  letter-spacing:4px; color:#00d4ff;
                  text-shadow: 0 0 15px rgba(0,212,255,0.5);'>
        ⬡ QUANTUM
      </div>
      <div style='font-family:Space Mono,monospace; font-size:9px;
                  letter-spacing:2px; color:#2a5a7a; margin-top:2px;'>
        TERMINAL v1.0
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    st.markdown("<div class='section-label'>▸ Universe</div>", unsafe_allow_html=True)

    DEFAULT_TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA", "BRK-B"]
    selected_tickers = st.multiselect(
        "Tickers", DEFAULT_TICKERS + ["JPM","GS","BTC-USD","ETH-USD","GLD","SPY","QQQ"],
        default=["AAPL", "MSFT", "NVDA", "TSLA"],
        max_selections=8,
    )
    primary_ticker = st.selectbox("Primary Ticker (Chart)", selected_tickers if selected_tickers else ["AAPL"])

    st.divider()
    st.markdown("<div class='section-label'>▸ Time Window</div>", unsafe_allow_html=True)

    period_map = {
        "1 Week": ("7d", "60m"), "1 Month": ("1mo", "1d"),
        "3 Months": ("3mo", "1d"), "6 Months": ("6mo", "1d"),
        "1 Year": ("1y", "1d"), "2 Years": ("2y", "1wk"),
        "5 Years": ("5y", "1wk"),
    }
    period_label = st.selectbox("Period", list(period_map.keys()), index=3)
    period, interval = period_map[period_label]

    chart_type = st.selectbox("Chart Type", ["Candlestick", "OHLC", "Line"])

    st.divider()
    st.markdown("<div class='section-label'>▸ Indicators</div>", unsafe_allow_html=True)

    show_sma  = st.checkbox("SMA", value=True)
    show_ema  = st.checkbox("EMA", value=False)
    show_bb   = st.checkbox("Bollinger Bands", value=True)
    show_vol  = st.checkbox("Volume", value=True)
    show_rsi  = st.checkbox("RSI", value=True)
    show_macd = st.checkbox("MACD", value=True)

    with st.expander("▸ Indicator Windows"):
        sma1       = st.slider("SMA Fast",   5, 50,  20)
        sma2       = st.slider("SMA Slow",  20, 200, 50)
        ema_w      = st.slider("EMA",        5, 100, 21)
        bb_window  = st.slider("BB Window", 10, 50,  20)
        rsi_window = st.slider("RSI Window", 5, 30,  14)

    st.divider()
    st.markdown(f"""
    <div style='font-family:Space Mono,monospace; font-size:9px; color:#1e3a55; text-align:center;'>
      <span class='status-dot'></span>LIVE · {datetime.now().strftime('%H:%M:%S')}
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  HEADER
# ─────────────────────────────────────────────
col_h1, col_h2, col_h3 = st.columns([3, 1, 1])
with col_h1:
    st.markdown(f"""
    <p class='terminal-header'>QUANTUM TERMINAL</p>
    <p class='terminal-sub'>
      <span class='status-dot'></span>
      MARKET DATA · {datetime.now().strftime('%A %d %B %Y · %H:%M UTC')}
    </p>
    """, unsafe_allow_html=True)

if not selected_tickers:
    st.warning("▸ Sélectionnez au moins un ticker dans la barre latérale.")
    st.stop()

# ─────────────────────────────────────────────
#  LIVE PRICE STRIP
# ─────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<div class='section-label'>▸ Live Quotes</div>", unsafe_allow_html=True)

price_cols = st.columns(len(selected_tickers))
for i, tkr in enumerate(selected_tickers):
    info = fetch_info(tkr)
    price    = info.get("currentPrice") or info.get("regularMarketPrice") or info.get("previousClose")
    prev     = info.get("previousClose")
    chg_pct  = ((price - prev) / prev * 100) if price and prev else None
    name     = info.get("shortName", tkr)[:18]
    with price_cols[i]:
        if price:
            delta_str = f"{chg_pct:+.2f}%" if chg_pct is not None else ""
            delta_color = "normal" if chg_pct is None else ("normal" if chg_pct >= 0 else "inverse")
            st.metric(label=f"**{tkr}**", value=f"${price:,.2f}", delta=delta_str, delta_color=delta_color)
        else:
            st.metric(label=f"**{tkr}**", value="N/A")

st.divider()

# ─────────────────────────────────────────────
#  TABS
# ─────────────────────────────────────────────
tab_chart, tab_fund, tab_corr, tab_screener = st.tabs([
    "📈  CHART & INDICATORS",
    "🏢  FUNDAMENTALS",
    "🔥  CORRELATION",
    "📋  SCREENER",
])

# ══════════════════════════════════════════════
#  TAB 1 — CHART
# ══════════════════════════════════════════════
with tab_chart:
    df_raw = fetch_data(primary_ticker, period, interval)
    if df_raw.empty:
        st.error(f"Aucune donnée pour {primary_ticker}.")
    else:
        df = compute_indicators(df_raw, sma1, sma2, ema_w, bb_window, rsi_window)

        # ── subplot structure ────────────────────
        rows = 1
        row_heights = [0.55]
        if show_vol:  rows += 1; row_heights.append(0.12)
        if show_rsi:  rows += 1; row_heights.append(0.14)
        if show_macd: rows += 1; row_heights.append(0.19)

        fig = make_subplots(
            rows=rows, cols=1, shared_xaxes=True,
            vertical_spacing=0.03,
            row_heights=row_heights,
        )
        cur_row = 1

        # ── price candles / line ──────────────────
        close = df["Close"].squeeze()
        open_ = df["Open"].squeeze()
        high  = df["High"].squeeze()
        low   = df["Low"].squeeze()
        vol   = df["Volume"].squeeze()
        idx   = df.index

        if chart_type == "Candlestick":
            fig.add_trace(go.Candlestick(
                x=idx, open=open_, high=high, low=low, close=close,
                increasing_line_color="#00ff88", decreasing_line_color="#ff4466",
                increasing_fillcolor="#00ff88", decreasing_fillcolor="#ff4466",
                name=primary_ticker, line_width=1,
            ), row=cur_row, col=1)
        elif chart_type == "OHLC":
            fig.add_trace(go.Ohlc(
                x=idx, open=open_, high=high, low=low, close=close,
                increasing_line_color="#00ff88", decreasing_line_color="#ff4466",
                name=primary_ticker,
            ), row=cur_row, col=1)
        else:
            fig.add_trace(go.Scatter(
                x=idx, y=close, mode="lines",
                line=dict(color="#00d4ff", width=1.5),
                name=primary_ticker,
                fill="tozeroy", fillcolor="rgba(0,212,255,0.04)",
            ), row=cur_row, col=1)

        # ── overlays ──────────────────────────────
        c = color_seq()
        if show_sma:
            fig.add_trace(go.Scatter(x=idx, y=df[f"SMA{sma1}"], mode="lines", line=dict(color=c[1], width=1), name=f"SMA{sma1}"), row=cur_row, col=1)
            fig.add_trace(go.Scatter(x=idx, y=df[f"SMA{sma2}"], mode="lines", line=dict(color=c[2], width=1, dash="dash"), name=f"SMA{sma2}"), row=cur_row, col=1)
        if show_ema:
            fig.add_trace(go.Scatter(x=idx, y=df[f"EMA{ema_w}"], mode="lines", line=dict(color=c[4], width=1), name=f"EMA{ema_w}"), row=cur_row, col=1)
        if show_bb:
            fig.add_trace(go.Scatter(x=idx, y=df["BB_up"], mode="lines", line=dict(color="#ffaa00", width=0.8, dash="dot"), name="BB Upper"), row=cur_row, col=1)
            fig.add_trace(go.Scatter(x=idx, y=df["BB_dn"], mode="lines", line=dict(color="#ffaa00", width=0.8, dash="dot"), fill="tonexty", fillcolor="rgba(255,170,0,0.04)", name="BB Lower"), row=cur_row, col=1)
            fig.add_trace(go.Scatter(x=idx, y=df["BB_mid"], mode="lines", line=dict(color="#ffaa00", width=0.5), name="BB Mid"), row=cur_row, col=1)

        # ── volume ────────────────────────────────
        if show_vol:
            cur_row += 1
            vol_colors = ["#00ff88" if c_ >= o_ else "#ff4466" for c_, o_ in zip(close, open_)]
            fig.add_trace(go.Bar(x=idx, y=vol, marker_color=vol_colors, name="Volume", opacity=0.7), row=cur_row, col=1)
            fig.update_yaxes(title_text="VOL", row=cur_row, col=1)

        # ── RSI ───────────────────────────────────
        if show_rsi:
            cur_row += 1
            fig.add_trace(go.Scatter(x=idx, y=df["RSI"], mode="lines", line=dict(color="#aa88ff", width=1.2), name="RSI"), row=cur_row, col=1)
            fig.add_hline(y=70, line_dash="dot", line_color="#ff4466", line_width=0.7, row=cur_row, col=1)
            fig.add_hline(y=30, line_dash="dot", line_color="#00ff88", line_width=0.7, row=cur_row, col=1)
            fig.add_hrect(y0=30, y1=70, fillcolor="rgba(170,136,255,0.04)", line_width=0, row=cur_row, col=1)
            fig.update_yaxes(title_text="RSI", range=[0,100], row=cur_row, col=1)

        # ── MACD ──────────────────────────────────
        if show_macd:
            cur_row += 1
            hist_col = ["#00ff88" if v >= 0 else "#ff4466" for v in df["MACD_hist"].fillna(0)]
            fig.add_trace(go.Bar(x=idx, y=df["MACD_hist"], marker_color=hist_col, name="MACD Hist", opacity=0.8), row=cur_row, col=1)
            fig.add_trace(go.Scatter(x=idx, y=df["MACD"], mode="lines", line=dict(color="#00d4ff", width=1), name="MACD"), row=cur_row, col=1)
            fig.add_trace(go.Scatter(x=idx, y=df["MACD_signal"], mode="lines", line=dict(color="#ffaa00", width=1), name="Signal"), row=cur_row, col=1)
            fig.update_yaxes(title_text="MACD", row=cur_row, col=1)

        fig.update_layout(
            **PLOTLY_LAYOUT,
            height=max(600, 200 * rows),
            title=dict(text=f"◈ {primary_ticker} — {period_label}", font=dict(family="Orbitron", color="#00d4ff", size=14)),
            xaxis_rangeslider_visible=False,
            showlegend=True,
            hovermode="x unified",
        )
        fig.update_xaxes(showspikes=True, spikecolor="#1e3a55", spikethickness=1)
        fig.update_yaxes(showspikes=True, spikecolor="#1e3a55", spikethickness=1)
        st.plotly_chart(fig, use_container_width=True)

        # ── Stats strip ───────────────────────────
        st.markdown("<div class='section-label'>▸ Period Statistics</div>", unsafe_allow_html=True)
        oc1, oc2, oc3, oc4, oc5, oc6 = st.columns(6)
        latest = float(close.iloc[-1])
        first  = float(close.iloc[0])
        ret    = (latest - first) / first * 100
        hi     = float(high.max())
        lo     = float(low.min())
        vol_m  = float(vol.mean()) / 1e6
        atr    = float((high - low).rolling(14).mean().iloc[-1])
        oc1.metric("Open (Period)", f"${first:,.2f}")
        oc2.metric("Last Price",    f"${latest:,.2f}")
        oc3.metric("Period Return", f"{ret:+.2f}%")
        oc4.metric("52W High / Low", f"${hi:,.2f} / ${lo:,.2f}")
        oc5.metric("Avg Volume",    f"{vol_m:.1f}M")
        oc6.metric("ATR(14)",       f"${atr:,.2f}")

# ══════════════════════════════════════════════
#  TAB 2 — FUNDAMENTALS
# ══════════════════════════════════════════════
with tab_fund:
    fund_ticker = st.selectbox("Select Ticker", selected_tickers, key="fund_tkr")
    info = fetch_info(fund_ticker)

    if not info:
        st.warning("Données fondamentales indisponibles.")
    else:
        fc1, fc2, fc3 = st.columns([1, 1, 1])

        with fc1:
            st.markdown("<div class='section-label'>▸ Company</div>", unsafe_allow_html=True)
            st.markdown(f"""
            <div style='font-family:Space Mono,monospace; font-size:12px; line-height:2;'>
              <b style='color:#00d4ff;'>{info.get('longName','N/A')}</b><br>
              <span style='color:#4a7a99;'>Sector:</span> {info.get('sector','N/A')}<br>
              <span style='color:#4a7a99;'>Industry:</span> {info.get('industry','N/A')}<br>
              <span style='color:#4a7a99;'>Country:</span> {info.get('country','N/A')}<br>
              <span style='color:#4a7a99;'>Exchange:</span> {info.get('exchange','N/A')}<br>
              <span style='color:#4a7a99;'>Currency:</span> {info.get('currency','N/A')}<br>
              <span style='color:#4a7a99;'>Employees:</span> {info.get('fullTimeEmployees', 'N/A'):,} if isinstance(info.get('fullTimeEmployees'), int) else info.get('fullTimeEmployees','N/A')
            </div>
            """.replace("if isinstance(info.get('fullTimeEmployees'), int) else info.get('fullTimeEmployees','N/A')", ""), unsafe_allow_html=True)

            emp = info.get("fullTimeEmployees")
            st.markdown(f"<span style='color:#4a7a99; font-family:Space Mono,monospace; font-size:12px;'>Employees:</span> <span style='font-family:Space Mono,monospace; font-size:12px;'>{emp:,}</span>" if isinstance(emp, (int, float)) else "", unsafe_allow_html=True)

            website = info.get("website", "")
            if website:
                st.markdown(f"<a href='{website}' style='color:#00d4ff; font-size:11px; font-family:Space Mono,monospace;'>↗ {website}</a>", unsafe_allow_html=True)

        with fc2:
            st.markdown("<div class='section-label'>▸ Valuation</div>", unsafe_allow_html=True)
            valuation_data = {
                "Market Cap":       fmt_large(info.get("marketCap")),
                "Enterprise Value": fmt_large(info.get("enterpriseValue")),
                "P/E (TTM)":        f"{info.get('trailingPE', 'N/A'):.2f}" if isinstance(info.get("trailingPE"), float) else "N/A",
                "Fwd P/E":          f"{info.get('forwardPE', 'N/A'):.2f}" if isinstance(info.get("forwardPE"), float) else "N/A",
                "P/B":              f"{info.get('priceToBook', 'N/A'):.2f}" if isinstance(info.get("priceToBook"), float) else "N/A",
                "P/S (TTM)":        f"{info.get('priceToSalesTrailing12Months', 'N/A'):.2f}" if isinstance(info.get("priceToSalesTrailing12Months"), float) else "N/A",
                "EV/EBITDA":        f"{info.get('enterpriseToEbitda', 'N/A'):.2f}" if isinstance(info.get("enterpriseToEbitda"), float) else "N/A",
                "EV/Revenue":       f"{info.get('enterpriseToRevenue', 'N/A'):.2f}" if isinstance(info.get("enterpriseToRevenue"), float) else "N/A",
            }
            for k, v in valuation_data.items():
                cols = st.columns([2, 1])
                cols[0].markdown(f"<span style='color:#4a7a99; font-family:Space Mono,monospace; font-size:11px;'>{k}</span>", unsafe_allow_html=True)
                cols[1].markdown(f"<span style='color:#e8f4fd; font-family:Space Mono,monospace; font-size:11px;'>{v}</span>", unsafe_allow_html=True)

        with fc3:
            st.markdown("<div class='section-label'>▸ Financials</div>", unsafe_allow_html=True)
            fin_data = {
                "Revenue (TTM)":   fmt_large(info.get("totalRevenue")),
                "Gross Profit":    fmt_large(info.get("grossProfits")),
                "EBITDA":          fmt_large(info.get("ebitda")),
                "Net Income":      fmt_large(info.get("netIncomeToCommon")),
                "Total Cash":      fmt_large(info.get("totalCash")),
                "Total Debt":      fmt_large(info.get("totalDebt")),
                "Free Cash Flow":  fmt_large(info.get("freeCashflow")),
                "Op Cash Flow":    fmt_large(info.get("operatingCashflow")),
            }
            for k, v in fin_data.items():
                cols = st.columns([2, 1])
                cols[0].markdown(f"<span style='color:#4a7a99; font-family:Space Mono,monospace; font-size:11px;'>{k}</span>", unsafe_allow_html=True)
                cols[1].markdown(f"<span style='color:#e8f4fd; font-family:Space Mono,monospace; font-size:11px;'>{v}</span>", unsafe_allow_html=True)

        st.divider()

        # ── Growth & Margins ──────────────────────
        st.markdown("<div class='section-label'>▸ Margins & Growth</div>", unsafe_allow_html=True)
        mg1, mg2, mg3, mg4, mg5, mg6 = st.columns(6)
        def pct(v): return f"{v*100:.1f}%" if isinstance(v, float) else "N/A"
        mg1.metric("Gross Margin",    pct(info.get("grossMargins")))
        mg2.metric("Op Margin",       pct(info.get("operatingMargins")))
        mg3.metric("Profit Margin",   pct(info.get("profitMargins")))
        mg4.metric("Revenue Growth",  pct(info.get("revenueGrowth")))
        mg5.metric("Earnings Growth", pct(info.get("earningsGrowth")))
        mg6.metric("ROE",             pct(info.get("returnOnEquity")))

        # ── Dividend & Short ──────────────────────
        st.markdown("<div class='section-label'>▸ Dividend & Short Interest</div>", unsafe_allow_html=True)
        dv1, dv2, dv3, dv4, dv5 = st.columns(5)
        div_yield = info.get("dividendYield")
        div_rate  = info.get("dividendRate")
        short_pct = info.get("shortPercentOfFloat")
        beta      = info.get("beta")
        dv1.metric("Dividend Yield",  pct(div_yield) if div_yield else "N/A")
        dv2.metric("Dividend Rate",   f"${div_rate:.2f}" if isinstance(div_rate, float) else "N/A")
        dv3.metric("Short % Float",   pct(short_pct) if short_pct else "N/A")
        dv4.metric("Beta",            f"{beta:.2f}" if isinstance(beta, float) else "N/A")
        dv5.metric("52W High / Low",  f"{fmt_large(info.get('fiftyTwoWeekHigh'))} / {fmt_large(info.get('fiftyTwoWeekLow'))}".replace("$",""))

        # ── Business Summary ──────────────────────
        summary = info.get("longBusinessSummary", "")
        if summary:
            with st.expander("▸ Business Summary"):
                st.markdown(f"<p style='font-family:IBM Plex Sans,sans-serif; font-size:13px; color:#8aafc8; line-height:1.7;'>{summary}</p>", unsafe_allow_html=True)

# ══════════════════════════════════════════════
#  TAB 3 — CORRELATION HEATMAP
# ══════════════════════════════════════════════
with tab_corr:
    st.markdown("<div class='section-label'>▸ Correlation Matrix — Daily Returns</div>", unsafe_allow_html=True)

    if len(selected_tickers) < 2:
        st.info("Sélectionnez ≥ 2 tickers pour calculer la corrélation.")
    else:
        with st.spinner("Fetching correlation data…"):
            closes = {}
            for t in selected_tickers:
                d = fetch_data(t, period, "1d")
                if not d.empty:
                    closes[t] = d["Close"].squeeze()

            if len(closes) >= 2:
                price_df = pd.DataFrame(closes).dropna()
                ret_df   = price_df.pct_change().dropna()
                corr     = ret_df.corr()

                # Heatmap
                fig_corr = go.Figure(go.Heatmap(
                    z=corr.values,
                    x=corr.columns.tolist(),
                    y=corr.columns.tolist(),
                    colorscale=[
                        [0.0,  "#ff4466"],
                        [0.25, "#aa2244"],
                        [0.5,  "#0d1f30"],
                        [0.75, "#004488"],
                        [1.0,  "#00d4ff"],
                    ],
                    zmid=0,
                    text=[[f"{v:.3f}" for v in row] for row in corr.values],
                    texttemplate="%{text}",
                    textfont=dict(family="Space Mono", size=12, color="#e8f4fd"),
                    hovertemplate="<b>%{y}</b> vs <b>%{x}</b><br>Corr: %{z:.4f}<extra></extra>",
                    colorbar=dict(
                        tickfont=dict(family="Space Mono", color="#8aafc8"),
                        title=dict(text="ρ", font=dict(color="#4da8da")),
                        bordercolor="#1a3a55",
                    ),
                ))
                fig_corr.update_layout(
                    **PLOTLY_LAYOUT,
                    height=500,
                    title=dict(text=f"◈ Return Correlation — {period_label}", font=dict(family="Orbitron", color="#00d4ff", size=13)),
                )
                st.plotly_chart(fig_corr, use_container_width=True)

                # ── Normalized performance ─────────────
                st.markdown("<div class='section-label'>▸ Normalized Performance (Base 100)</div>", unsafe_allow_html=True)
                norm = (price_df / price_df.iloc[0]) * 100
                fig_norm = go.Figure()
                for i, col in enumerate(norm.columns):
                    fig_norm.add_trace(go.Scatter(
                        x=norm.index, y=norm[col], mode="lines",
                        name=col,
                        line=dict(color=color_seq()[i % len(color_seq())], width=1.5),
                    ))
                fig_norm.update_layout(
                    **PLOTLY_LAYOUT,
                    height=380,
                    title=dict(text="◈ Normalized Prices", font=dict(family="Orbitron", color="#00d4ff", size=13)),
                    hovermode="x unified",
                )
                st.plotly_chart(fig_norm, use_container_width=True)

                # ── Return distribution ────────────────
                st.markdown("<div class='section-label'>▸ Return Distribution</div>", unsafe_allow_html=True)
                fig_box = go.Figure()
                for i, col in enumerate(ret_df.columns):
                    fig_box.add_trace(go.Violin(
                        y=ret_df[col] * 100,
                        name=col,
                        box_visible=True,
                        meanline_visible=True,
                        line_color=color_seq()[i % len(color_seq())],
                        fillcolor=color_seq()[i % len(color_seq())].replace("ff", "44") if len(color_seq()[i % len(color_seq())]) == 7 else color_seq()[i % len(color_seq())],
                        opacity=0.6,
                    ))
                fig_box.update_layout(
                    **PLOTLY_LAYOUT,
                    height=380,
                    title=dict(text="◈ Daily Return Distribution (%)", font=dict(family="Orbitron", color="#00d4ff", size=13)),
                    yaxis_title="Daily Return (%)",
                    violinmode="overlay",
                )
                st.plotly_chart(fig_box, use_container_width=True)

# ══════════════════════════════════════════════
#  TAB 4 — SCREENER
# ══════════════════════════════════════════════
with tab_screener:
    st.markdown("<div class='section-label'>▸ Multi-Asset Snapshot</div>", unsafe_allow_html=True)

    rows_list = []
    prog = st.progress(0, text="Loading data…")
    for idx_t, t in enumerate(selected_tickers):
        info = fetch_info(t)
        df_t = fetch_data(t, "6mo", "1d")
        close_t = df_t["Close"].squeeze() if not df_t.empty else pd.Series(dtype=float)

        price   = info.get("currentPrice") or info.get("regularMarketPrice") or (float(close_t.iloc[-1]) if len(close_t) else None)
        prev    = info.get("previousClose")
        chg_pct = (price - prev) / prev * 100 if price and prev else None
        vol_20  = float(close_t.rolling(20).std().iloc[-1]) if len(close_t) >= 20 else None
        sma50_v = float(close_t.rolling(50).mean().iloc[-1]) if len(close_t) >= 50 else None
        sma200  = float(close_t.rolling(200).mean().iloc[-1]) if len(close_t) >= 200 else None
        above50 = "↑" if (price and sma50_v and price > sma50_v) else ("↓" if sma50_v else "—")

        # RSI quick
        rsi_v = None
        if len(close_t) > 14:
            delta_ = close_t.diff()
            gain_  = delta_.clip(lower=0).rolling(14).mean()
            loss_  = (-delta_.clip(upper=0)).rolling(14).mean()
            rs_    = gain_ / loss_.replace(0, np.nan)
            rsi_series = 100 - 100 / (1 + rs_)
            rsi_v = float(rsi_series.iloc[-1]) if not np.isnan(rsi_series.iloc[-1]) else None

        rows_list.append({
            "Ticker":      t,
            "Name":        (info.get("shortName","")[:20] if info.get("shortName") else t),
            "Price":       f"${price:,.2f}" if price else "N/A",
            "Chg %":       f"{chg_pct:+.2f}%" if chg_pct is not None else "N/A",
            "Mkt Cap":     fmt_large(info.get("marketCap")),
            "P/E":         f"{info.get('trailingPE',0):.1f}" if isinstance(info.get("trailingPE"), float) else "N/A",
            "EPS":         f"${info.get('trailingEps',0):.2f}" if isinstance(info.get("trailingEps"), float) else "N/A",
            "Beta":        f"{info.get('beta',0):.2f}" if isinstance(info.get("beta"), float) else "N/A",
            "Vol(20d σ)":  f"{vol_20:.2f}%" if vol_20 else "N/A",
            "RSI(14)":     f"{rsi_v:.1f}" if rsi_v else "N/A",
            "vs SMA50":    above50,
            "Sector":      info.get("sector","N/A"),
        })
        prog.progress((idx_t + 1) / len(selected_tickers), text=f"Loaded {t}…")

    prog.empty()

    screen_df = pd.DataFrame(rows_list)
    st.dataframe(screen_df.set_index("Ticker"), use_container_width=True, height=350)

    # ── RSI Gauge chart ───────────────────────
    st.markdown("<div class='section-label'>▸ RSI Gauge (14)</div>", unsafe_allow_html=True)
    rsi_vals = []
    rsi_tkrs = []
    for r in rows_list:
        try:
            v = float(r["RSI(14)"])
            rsi_vals.append(v)
            rsi_tkrs.append(r["Ticker"])
        except Exception:
            pass

    if rsi_vals:
        rsi_colors = ["#ff4466" if v > 70 else "#00ff88" if v < 30 else "#00d4ff" for v in rsi_vals]
        fig_rsi = go.Figure(go.Bar(
            x=rsi_tkrs, y=rsi_vals,
            marker_color=rsi_colors,
            text=[f"{v:.1f}" for v in rsi_vals],
            textposition="outside",
            textfont=dict(family="Space Mono", color="#e8f4fd", size=11),
        ))
        fig_rsi.add_hline(y=70, line_dash="dot", line_color="#ff4466", line_width=1, annotation_text="OB 70", annotation_font_color="#ff4466")
        fig_rsi.add_hline(y=30, line_dash="dot", line_color="#00ff88", line_width=1, annotation_text="OS 30", annotation_font_color="#00ff88")
        fig_rsi.add_hrect(y0=30, y1=70, fillcolor="rgba(0,212,255,0.03)", line_width=0)
        fig_rsi.update_layout(
            **PLOTLY_LAYOUT,
            height=300,
            yaxis=dict(range=[0, 100], title="RSI"),
            title=dict(text="◈ RSI(14) Overview", font=dict(family="Orbitron", color="#00d4ff", size=13)),
            showlegend=False,
        )
        st.plotly_chart(fig_rsi, use_container_width=True)

# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.divider()
st.markdown("""
<div style='text-align:center; font-family:Space Mono,monospace; font-size:9px; color:#1e3a55; padding: 8px 0;'>
  QUANTUM TERMINAL · Data via Yahoo Finance · For informational purposes only · Not financial advice
</div>
""", unsafe_allow_html=True)
