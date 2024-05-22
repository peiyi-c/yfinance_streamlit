import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px
import datetime

st.title("Stock Dashboard")

# Sidebar 
st.sidebar.header('Stocks')
ticker_name_list = pd.read_csv('./ticker_names.txt')
ticker = st.sidebar.selectbox('Stock ticker', ticker_name_list) 
start_date = st.sidebar.date_input("Start Date", datetime.date(2024,1,1))
end_date = st.sidebar.date_input("End Date", datetime.date.today())

# Retrieve Data
data = yf.Ticker(ticker) 
tickerDef = data.history(period='1d', start=start_date, end=end_date) 

# Ticker information
fig = px.line(tickerDef, x = tickerDef.index, y = tickerDef['Close'], title = data.info['longName'])
st.plotly_chart(fig)

