import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="Financial Dashboard",
    layout="wide"
    )

st.title("Financial Dashboard")

tickers = st.sidebar.multiselect(
    "Select assets",
    ["AAPL", "MSFT", "NVDA", "GOOGL", "BTC-USD", "SPY"],
    default=["AAPL", "MSFT", "NVDA"]
)

period = st.sidebar.selectbox(
    "Select periods",
    ["6mo", "1y", "2y", "3y"]
    )

data = yf.download(tickers, period=period)
df = data["Close"]

if not tickers:
  st.warning('Please choose ticker.')
  st.stop()

tick = st.sidebar.selectbox(
    "Select ticks",
    tickers
    )

series = df[tick]

tab1, tab2, tab3, tab4 = st.tabs(["Ticker", "Normalization", "Volatility","Sharpe Ratio"])

with tab1:

    fig = go.Figure()

    fig.add_trace(go.Scatter(
    x=series.index,
    y=series,
    mode='lines',
    name=tick,
    line=dict(color='firebrick', width=2)
    ))

    fig.update_layout(
    title=tick,
    xaxis_title='Date',
    yaxis_title='Price (USD)'
    )

    fig.add_trace(go.Scatter(
    x=series.index,
    y=series.rolling(20).mean(),
    mode='lines',
    name='MA20',
    line=dict(dash='dash')
    ))

    fig.add_trace(go.Scatter(
    x=series.index,
    y=series.rolling(50).mean(),

    mode='lines',
    name='MA50',
    line=dict(dash='dash')
    ))

    st.plotly_chart(fig)

normalized = df / df.iloc[0] * 100 

with tab2:
    
    fig = go.Figure()

    for col in normalized:
        fig.add_trace(go.Scatter(
        x=normalized.index,
        y=normalized[col],

        mode='lines',
        name=col,
        line=dict(width=2)
    ))

    fig.update_layout(
        title="Normalized",
        xaxis_title='Date',
        yaxis_title='Growth (base 100)'
    )

    st.plotly_chart(fig)

returns = df.pct_change()
volatility = returns.rolling(30).std() * 100

with tab3:

    fig = go.Figure()

    for col in volatility:
        fig.add_trace(go.Scatter(
        x=volatility.index,
        y=volatility[col],

        mode='lines',
        name=col,
        line=dict(width=2)
    ))

    fig.update_layout(
        title="Volatility",
        xaxis_title='Date',
        yaxis_title='Volatility (%)'
    )

    st.plotly_chart(fig)

mean_returns = returns.mean()
std_returns = returns.std()
sharpe_ratio = (mean_returns/std_returns)*(252**0.5)

with tab4:
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=sharpe_ratio.index,
        y=sharpe_ratio.values,

        name=tick
    ))

    fig.update_layout(
        title="Sharpe Ratio",
        xaxis_title='Tick',
        yaxis_title='Sharpe Ratio'
    )

    st.caption("Sharpe > 1 — good, > 2 — very good, negative — return doesn't justify the risk")

    st.plotly_chart(fig)