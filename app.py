import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta

# ============= PAGE SETUP =============
st.set_page_config(page_title="Stock Dashboard", page_icon="🧊", layout="centered")

# ============ CSS STYLES ==============
st.markdown('<style>h3{font-size:1.65rem;opacity:0.3;}div.block-container{padding:1rem auto;} div.element-container{margin: 0rem; padding: 0rem;}div[role="tablist"]{justify-content: space-between;}button[role="tab"]{padding: 1rem; border-radius: 10px;}button[role="tab"][aria-selected="true"]{background: #E0FBE2;}button[role="tab"] p, summary{color:#333333; font-weight:600;} summary:hover span{color:#ACE1AF; font-weight:bold;} div[role="presentation"]{background:none;} div[role="alert"]{padding:1.2rem 2.2rem;background:#F6F5F250;color:#333333;line-height: 1.7;} a{color:rgb(49, 51, 63) !important; text-decoration:none;} a:hover{color:#ACE1AF !important; text-decoration:none;} div[data-baseweb="select"]>div{border-color: #D2E9E9 !important; box-shadow: rgba(0, 0, 0, 0.04) 0px 3px 5px;}div[data-testid="stTable"]{padding: 7px 0 0 0;}table{font-family:"Source Sans Pro", sans-serif;text-align:left;border-radius: 10px;}.no-data{padding: 1.75rem 0;text-align: left; color: rgb(49, 51, 63); font-weight: bold;} .tab-num{font-size: 2.25rem; color: rgb(49, 51, 63);}</style>', unsafe_allow_html = True)

# Title #   
st.header('Stock Dashboard')  

# initiate 
today = datetime.now().date()
ticker = ''
company = ''

col1, col2 = st.columns((2))
with col1:
  ticker_name_list = pd.read_csv('./ticker_names.txt')
  ticker = st.selectbox('Select a Stock', ticker_name_list) 

# ============ Company Data ============
company = yf.Ticker(ticker) 

# ============ Company Info ============
infos = company.info

# Current Price #
col2.metric("Current Price", f"${infos.get('currentPrice', '')}")

# Company name # 
st.title(infos.get('longName', ''))

# Subheader - Performance # 
st.subheader('Performance')

# Tabs #
one_day, one_week, one_month, one_year, max = st.tabs(['5 Days',' 1 Week',' 1 Month',' 1 Year', 'Max'])

def get_past_date(value, units):
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
 ticker = company.history(period='1d', start=get_past_date(5, 'days'), end=today) 
 if ticker.empty:
    st.markdown("<p class='no-data'>No Data available</p>", unsafe_allow_html=True)
 else: 
   fig = px.line(ticker, x = ticker.index, y = ticker['Close'], title = '5 Days')
   update_axis_names(fig, 'Hour', 'Close Price')
   st.plotly_chart(fig, use_container_width = True)

with one_week:
 ticker = company.history(interval='1d', start=get_past_date(1, 'weeks'), end=today) 
 if ticker.empty:
    st.markdown("<p class='no-data'>No Data available</p>", unsafe_allow_html=True)
 else: 
  fig = px.line(ticker, x = ticker.index, y = ticker['Close'], title = '1 Week')
  update_axis_names(fig, 'Date', 'Close Price')
  st.plotly_chart(fig, use_container_width = True)

with one_month:
 ticker = company.history(interval='1d', start=get_past_date(1, 'months'), end=today) 
 if ticker.empty:
  st.markdown("<p class='no-data'>No Data available</p>", unsafe_allow_html=True)
 else: 
  fig = px.line(ticker, x = ticker.index, y = ticker['Close'], title = '1 Month')
  update_axis_names(fig, 'Date', 'Close Price')
  st.plotly_chart(fig, use_container_width = True)

with one_year:
 ticker = company.history(interval='1mo', start=get_past_date(1, 'years'), end=today) 
 if ticker.empty:
  st.markdown("<p class='no-data'>No Data available</p>", unsafe_allow_html=True)
 else: 
  fig = px.line(ticker, x = ticker.index, y = ticker['Close'], title = '1 Year')
  update_axis_names(fig, 'Month', 'Close Price')
  st.plotly_chart(fig, use_container_width = True)

with max:
 ticker = company.history(period='max', interval='3mo') 
 if ticker.empty:
  st.markdown("<p class='no-data'>No Data available</p>", unsafe_allow_html=True)
 else:
  fig = px.line(ticker, x = ticker.index, y = ticker['Close'], title = 'Max')
  update_axis_names(fig, 'Year', 'Close Price')
  st.plotly_chart(fig, use_container_width = True)

st.divider()

# Tabs #
custom_period, day_high, day_low, fiftyTwo_high, fiftyTwo_low = st.tabs(['Custom Period','Day High',' Day Low','52 Week High','52 Week Low'])
with custom_period:
  col1, col2, col3 = st.columns((3))
  with col1:
    min_date = ticker.index.min().date() if not ticker.empty else date(date.today().year, 1, 1)
    start_date = pd.to_datetime(st.date_input("Start Date", date(date.today().year, 1, 1), min_value=min_date))
  with col2:
    end_date = pd.to_datetime(st.date_input("End Date", date.today()))
  with col3:
    interval = st.selectbox("Interval", ['1 Day', '5 Days', '1 Week', '1 Month', '3 Months'])
    
  def switch_inter(value):
    if value == '1 Day':
      return '1d'
    elif value == '5 Days':
      return '5d'
    elif value == '1 Week':
      return '1wk'
    elif value == '1 Month':
      return '1mo'
    elif value == '3 Months':
      return '3mo'
    else:
      return '1d'

  ticker = company.history(period='max', interval=switch_inter(interval), start=start_date, end=end_date)

  if ticker.empty:
    st.markdown("<p class='no-data'>No Data available</p>", unsafe_allow_html=True)
  else:
    fig = px.line(ticker, x = ticker.index, y = ticker['Close'], title = company.info['longName'])
    update_axis_names(fig, 'Day', 'Close Price')
    st.plotly_chart(fig, use_container_width = True)

with day_high:
  if 'dayHigh'in infos:
    dayHigh = round(float(infos['dayHigh']), 3)
    st.markdown(f"<p class='tab-num' style='width:40%; text-align:right;'>$ {dayHigh}</p>", unsafe_allow_html=True)
  else:
   st.markdown("<p class='no-data'>No Data available</p>", unsafe_allow_html=True)

with day_low:
  if 'dayLow'in infos:
   dayLow = round(float(infos['dayLow']), 3)
   st.markdown(f"<p class='tab-num' style='width:60%; text-align:right;'>$ {dayLow}</p>", unsafe_allow_html=True)
  else:
    st.markdown("<p class='no-data'>No Data available</p>", unsafe_allow_html=True)

with fiftyTwo_high:
  if 'fiftyTwoWeekHigh'in infos:
    fiftyTwoWeekHigh = round(float(infos['fiftyTwoWeekHigh']), 3)
    st.markdown(f"<p class='tab-num' style='width:80%; text-align:right;'>$ {fiftyTwoWeekHigh}</p>", unsafe_allow_html=True)
  else:
    st.markdown("<p class='no-data'>No Data available</p>", unsafe_allow_html=True)

with fiftyTwo_low:
  if 'fiftyTwoWeekLow'in infos:
    fiftyTwoWeekLow = round(float(infos['fiftyTwoWeekLow']), 3)
    st.markdown(f"<p class='tab-num' style='text-align: right;'>$ {fiftyTwoWeekLow}</p>", unsafe_allow_html=True)
  else:
    st.markdown("<p class='no-data'>No Data available</p>", unsafe_allow_html=True)

st.divider()

# Subheader - Company Information # 
st.subheader("Company Information")

if infos.get('longName') is not None:
  st.markdown(f"**Company Name:** { infos.get('longName', '')}")
if infos.get('sector') is not None:
  st.markdown(f"**Sector:** {infos.get('sector', '')}")
if infos.get('website') is not None:
  st.markdown(f"**Website:** {infos.get('website', '')}")
if infos.get('irWebsite') is not None:
  st.markdown(f"**IR Website:** {infos.get('irWebsite', '')}")
if infos.get('address1') is not None:
  st.markdown("<p style='margin-bottom:0;font-weight:600;'>Address:</p>", unsafe_allow_html=True)
st.markdown(f"<span>{infos.get('address1', '')}<br/> {infos.get('city', '')}<br/> {infos.get('state', '')}  {infos.get('zip', '')}  {infos.get('country', '')}</span>", unsafe_allow_html=True)
if infos.get('longBusinessSummary') is not None:
  st.markdown("<p style='margin-bottom:3px;font-weight:600;'>Description:</p>", unsafe_allow_html=True)
  with st.expander("Read more"):
    st.info(infos.get('longBusinessSummary', ''))

# Display company logo
if 'logo_url' in company.info:
    st.image(company.info['logo_url'])
  
# Divider #
st.divider()

# ============== Company Fin ==============
#financials = company.financials
cashflow = company.cashflow
# =========================================

# Subheader - Key Metrics # 
st.subheader("Key Metrics")

if ticker.empty:
  st.markdown("<p class='no-data'>No Data available</p>", unsafe_allow_html=True)
else:
  col4, col5 = st.columns((2))
  with col4:
    if infos.get('marketCap') is not None:
      st.metric(label="Market Cap", value=f"$ {infos.get('marketCap', ''):,}")
    if infos.get('fiftyDayAverage') is not None:
      st.metric(label="50 Day Average", value=f"$ {infos.get('fiftyDayAverage', ''):,}")
    if infos.get('profitMargins') is not None:
      profitMargins = round((infos.get('profitMargins', '') * 100), 2)
      st.metric(label="Profit Margins", value=f"{profitMargins} %")
    if infos.get('grossMargins') is not None:
      grossMargins = round((infos.get('grossMargins', '') * 100), 2)
      st.metric(label="Gross Margins", value=f"{grossMargins} %")

  with col5: 
    if infos.get('totalRevenue') is not None:
     st.metric(label="Total Revenue", value=f"${ infos.get('totalRevenue', ''):,}")
    if infos.get('ebitda') is not None:
      st.metric(label="EBITDA", value=f"${ infos.get('ebitda', ''):,}")
    if infos.get('netIncomeToCommon') is not None:
     st.metric(label="Net Income", value=f"$ {infos.get('netIncomeToCommon', ''):,}")
    if infos.get('freeCashflow') is not None:
     st.metric(label="Free Cash Flow", value=f"$ {infos.get('freeCashflow', ''):,}")
    if infos.get('lastDividendValue') is not None and infos.get('lastDividendDate') is not None:
     lastDividendDate = datetime.utcfromtimestamp(infos.get('lastDividendDate')).date()
     lastDividendValue = round((infos.get('lastDividendValue', '')), 2)
     st.metric(label=f"Last Dividend {lastDividendDate}", value=f"$ {lastDividendValue}")
  

#st.write(infos)