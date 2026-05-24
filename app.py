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