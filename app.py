import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta

# page setup
st.set_page_config(page_title="Stock Dashboard", page_icon="🧊", layout="centered")

# styles
st.markdown('<style>div.block-container{padding-top:1rem; padding-bottom:1rem;} div.element-container{margin: 0rem; padding: 0rem;}</style>', unsafe_allow_html = True)

# Title #
st.title('Stock Dashboard')

col1, col2, col3 = st.columns((3))
# Selectbox: Ticker #
with col1:
  ticker_name_list = pd.read_csv('./ticker_names.txt')
  ticker = st.selectbox('Select a Stock', ticker_name_list) 
  # Retrieve Data
  company = yf.Ticker(ticker) 
# Company name #
col2.metric('Company Name', company.info['longName'])
# Current Price #
col3.metric(f"Current Price", f'${company.info['currentPrice']}', f"${(company.info['currentPrice'] - company.info['open']):.3f}")


   

# 1. Subheader # 
st.subheader('Performance')

# Tabs #
one_day, one_week, one_month, one_year, max = st.tabs(['1 Day',' 1 Week',' 1 Month',' 1 Year', 'Max'])
today = datetime.now().date()

def get_past_date(value, units='days'):
    if units == 'days':
        past_date = today - timedelta(days=value)
    elif units == 'weeks':
        past_date = today - timedelta(weeks=value)
    elif units == 'months':
        past_date = today - relativedelta(months=value)
    elif units == 'years':
        past_date = today - relativedelta(years=value)
    else:
        past_date = today - timedelta(days=value)
    return past_date


def update_axis_names(fig, x_axis_name, y_axis_name):
    fig.update_layout(xaxis_title=x_axis_name, yaxis_title=y_axis_name)
    return fig

with one_day:
 ticker = company.history(period='1d', interval='90m', start=get_past_date(1), end=today) 
 fig = px.line(ticker, x = ticker.index, y = ticker['Close'], title = '1 Day')
 update_axis_names(fig, 'Hour', 'Close Price')
 st.plotly_chart(fig, use_container_width = True)

with one_week:
 ticker = company.history(period='1d', interval='1d', start=get_past_date(1, 'weeks'), end=today) 
 fig = px.line(ticker, x = ticker.index, y = ticker['Close'], title = '1 Week')
 update_axis_names(fig, 'Day', 'Close Price')
 st.plotly_chart(fig, use_container_width = True)

with one_month:
 ticker = company.history(period='1d', interval='1d', start=get_past_date(1, 'months'), end=today) 
 fig = px.line(ticker, x = ticker.index, y = ticker['Close'], title = '1 Month')
 update_axis_names(fig, 'Day', 'Close Price')
 st.plotly_chart(fig, use_container_width = True)

with one_year:
 ticker = company.history(period='1d', interval='1mo', start=get_past_date(1, 'years'), end=today) 
 fig = px.line(ticker, x = ticker.index, y = ticker['Close'], title = '1 Year')
 update_axis_names(fig, 'Month', 'Close Price')
 st.plotly_chart(fig, use_container_width = True)

with max:
 ticker = company.history(period='max', interval='3mo') 
 fig = px.line(ticker, x = ticker.index, y = ticker['Close'], title = 'Max')
 update_axis_names(fig, 'Year', 'Close Price')
 st.plotly_chart(fig, use_container_width = True)

# Expander #
with st.expander('Custom Date'):
  ticker = company.history(period='max') 
  col1, col2, col3 = st.columns((3))
  with col1:
    start_date = pd.to_datetime(st.date_input("Start Date", date(date.today().year, 1, 1), min_value=ticker.index.min()))
  with col2:
    end_date = pd.to_datetime(st.date_input("End Date", date.today()))
  with col3:
    interval = st.selectbox("Interval", ['day', 'month'])
   
  def switch_inter(value):
    if value == 'day':
        return '1d'
    elif value == 'month':
        return '1mo'
    else:
        return '1d'

  ticker = company.history(period='max', interval=switch_inter(interval), start=start_date, end=end_date)
  fig = px.line(ticker, x = ticker.index, y = ticker['Close'], title = company.info['longName'])
  update_axis_names(fig, 'Day', 'Close Price')

  st.plotly_chart(fig, use_container_width = True)
 

# Divider #
st.divider()

infos = company.info

# Display company basic information
st.subheader("Company Information")
st.markdown(f"**Industry:** {infos.get('industry', 'N/A')}")
st.markdown(f"**Sector:** {infos.get('sector', 'N/A')}")
st.markdown(f"**Website:** {infos.get('website', 'N/A')}")
st.markdown(f"**Description:**")
with st.expander("Read more"):
  st.info(infos.get('longBusinessSummary', 'N/A'))

# Display company logo
if 'logo_url' in company.info:
    st.image(company.info['logo_url'])

# Key Metrics # 
st.subheader("Key Metrics")
col4, col5 = st.columns((2))
with col4:
   st.metric(label="Market Cap", value=f"${infos.get('marketCap', 'N/A'):,}")
   st.metric(label="Net Income", value=f"${infos.get('netIncomeToCommon', 'N/A'):,}")
   st.metric(label="52 Week High", value=f"${infos.get('fiftyTwoWeekHigh', 'N/A'):,}")
with col5: 
  st.metric(label="Revenue", value=f"${infos.get('totalRevenue', 'N/A'):,}")
  st.metric(label="EBITDA", value=f"${infos.get('ebitda', 'N/A'):,}")
  st.metric(label="52 Week Low", value=f"${infos.get('fiftyTwoWeekLow', 'N/A'):,}")

st.write(infos)



st.write('actions')
company.actions
st.write('basic_info')
company.basic_info
st.write('financials')
company.financials

