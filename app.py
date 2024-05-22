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


business_name = data.info['longName']
st.write(business_name)

# Tabs
pricing_data, fundamental_data = st.tabs(["Business Details", "Fundamental Data"])

with pricing_data:
  st.subheader('Business Details')
  business_summary = data.info['longBusinessSummary']
  st.info(business_summary)

with fundamental_data:
  st.subheader('Fundamental Data')
  tickerDef


data.info
