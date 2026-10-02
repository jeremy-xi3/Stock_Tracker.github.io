import pandas as pd
import streamlit as st
import yfinance as yf

st.title("Python Stock Tracker")

time_period = st.selectbox("Period", ["5d", "1mo", "3mo", "6mo", "1y", "5y", "ytd", "max"])

if "tickers" not in st.session_state:
    st.session_state.tickers = []

with st.form("add_ticker", clear_on_submit=True):
    ticker_symbol = st.text_input("Enter Stock Ticker: ")
    submit = st.form_submit_button("Add ticker")

if submit:
    if(ticker_symbol != ""):
        stock_data = yf.Ticker(ticker_symbol)
        hist_data = stock_data.history(period=time_period)

    if hist_data.empty:
        st.error(f"No data found for '{ticker_symbol.upper()}'. Try another symbol.")

    else:
        st.session_state.tickers.append(ticker_symbol)


# for output in st.session_state.tickers:
#     stock_data = yf.Ticker(output)
#     hist_data = stock_data.history(period=time_period)

#     #outputs charts for data
#     st.subheader(f"Price Chart for {output.upper()}")
#     st.line_chart(hist_data["Close"])
#     st.subheader("Recent Data")
#     st.write(hist_data.tail())
if st.session_state.tickers:
    data = yf.download(st.session_state.tickers, period=time_period)["Close"]
    st.line_chart(data)
    for stock in list(st.session_state.tickers):
        if st.button(f"Remove {stock}", key=f"remove_{stock}"):
            st.session_state.tickers.remove(stock)
            st.rerun()
