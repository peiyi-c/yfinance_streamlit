import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta

# page setup
st.set_page_config(page_title="Stock Dashboard", page_icon="🧊", layout="centered")

# custom styles
st.markdown('<style>h3{font-size:1.65rem;opacity:0.3;}div.block-container{padding:1rem auto;} div.element-container{margin: 0rem; padding: 0rem;}div[role="tablist"]{justify-content: space-between;}button[role="tab"]{padding: 1rem; border-radius: 10px;}button[role="tab"][aria-selected="true"]{background: #E0FBE2;}button[role="tab"] p, summary{color:#333333; font-weight:600;} summary:hover span{color:#ACE1AF; font-weight:bold;} div[role="presentation"]{background:none;} div[role="alert"]{background:#F6F5F250;color:#5AB2FF;} a{color:rgb(49, 51, 63) !important; text-decoration:none;} a:hover{color:#ACE1AF !important; text-decoration:none;} div[data-baseweb="select"]>div{border-color: #D2E9E9 !important; box-shadow: rgba(0, 0, 0, 0.04) 0px 3px 5px;}div[data-testid="stTable"]{padding: 7px 0 0 0;}table{font-family:"Source Sans Pro", sans-serif;text-align:left;border-radius: 10px;}thead{display:none;}.no-data{padding: 1.75rem 0;text-align: left; color: rgb(49, 51, 63); font-weight: bold;} .tab-num{font-size: 2.25rem; color: rgb(49, 51, 63);}</style>', unsafe_allow_html = True)

# Title #   
st.subheader('Stock Dashboard')  

col1, col2 = st.columns((2))
# Selectbox: Ticker #
def get_trend(company):
  if date.today().weekday() == 0 or date.today().weekday() == 5 or date.today().weekday() == 6:
    return ''
  elif round(company.info['currentPrice'] - company.basic_info['lastPrice'], 3) > 0:
    return round(company.info['currentPrice'] - company.basic_info['lastPrice'], 3)
  else:
    return ''

with col1:
  ticker_name_list = pd.read_csv('./ticker_names.txt')
  ticker = st.selectbox('Select a Stock', ticker_name_list) 
  # Retrieve Data
  company = yf.Ticker(ticker) 
# Current Price #
#col2.metric("Current Price", f'${company.info['currentPrice']}', f"${(company.info['currentPrice'] - company.basic_info['lastPrice']):.3f}")
if company.info['currentPrice']:
  col2.metric("Current Price", f'${company.info['currentPrice']}', get_trend(company))

# Company name # 
st.title(company.info['longName'])

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
 if ticker.empty:
    st.markdown("<p class='no-data'>No Data available</p>", unsafe_allow_html=True)
 else: 
   fig = px.line(ticker, x = ticker.index, y = ticker['Close'], title = '1 Day')
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

# Tab #
custom_period  = st.tabs(['Custom Period'])
col1, col2, col3 = st.columns((3))
with col1:
  start_date = pd.to_datetime(st.date_input("Start Date", date(date.today().year, 1, 1), min_value=ticker.index.min()))
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
 
# Divider #
st.divider()

# Basic Infos #
basic_info = company.basic_info
# Tabs #
day_high, day_low, year_high, year_low= st.tabs(['Day High',' Day Low',' Year High','Year Low'])
with day_high:
  st.markdown(f"<p class='tab-num'>$ {round(basic_info['dayHigh'], 3)}</p>", unsafe_allow_html=True)
with day_low:
  st.markdown(f"<p class='tab-num'>$ {round(basic_info['dayLow'], 3)}</p>", unsafe_allow_html=True)
with year_high:
  st.markdown(f"<p class='tab-num'>$ {round(basic_info['yearHigh'], 3)}</p>", unsafe_allow_html=True)
with year_low:
  st.markdown(f"<p class='tab-num'>$ {round(basic_info['yearLow'], 3)}</p>", unsafe_allow_html=True)

# Divider #
st.divider()

# Display company basic information
st.subheader("Company Information")
infos = company.info
st.markdown(f"**Company Name:** {company.info['longName']}")
st.markdown(f"**Sector:** {infos.get('sector', '')}")
st.markdown(f"**Website:** {infos.get('website', '')}")
st.markdown("<p style='margin-bottom:0;font-weight:600;'>Address:</p>", unsafe_allow_html=True)
st.markdown(f"<span>{infos.get('address1', 'N/A')}<br/> {infos.get('city', '')}<br/> {infos.get('state', '')}  {infos.get('zip', '')}  {infos.get('country', '')}</span>", unsafe_allow_html=True)
if infos['longBusinessSummary']:
  st.markdown("<p style='margin-bottom:3px;font-weight:600;'>Description:</p>", unsafe_allow_html=True)
  with st.expander("Read more"):
    st.info(infos.get('longBusinessSummary', ''))

# Display company logo
if 'logo_url' in company.info:
    st.image(company.info['logo_url'])
  
# Divider #
st.divider()

# Key Metrics # 
st.subheader("Key Metrics")
col4, col5 = st.columns((2))
with col4:
   st.metric(label="Market Cap", value=f"$ {infos.get('marketCap', 'N/A'):,}")
   st.metric(label="52 Week High", value=f"$ {infos.get('fiftyTwoWeekHigh', 'N/A'):,}")
   st.metric(label="52 Week Low", value=f"$ {infos.get('fiftyTwoWeekLow', 'N/A'):,}")
with col5: 
  st.metric(label="Revenue", value=f"${ infos.get('totalRevenue', 'N/A'):,}")
  st.metric(label="EBITDA", value=f"${ infos.get('ebitda', 'N/A'):,}")
  st.metric(label="Net Income", value=f"$ {infos.get('netIncomeToCommon', 'N/A'):,}")

# Dividends # 
if not company.actions.empty:
  st.markdown("<p style='margin: 0;font-size:14px; color:rgb(49, 51, 6);'>Dividend</p>", unsafe_allow_html=True)
  #format table..
  actions = company.actions.iloc[:, :-1]
  actions.index = actions.index.date
  actions['Dividends'] = actions['Dividends'].apply(lambda x: f"$ {x:.2f}")
  st.table(actions)

#basic_info

#st.write('financials')
#company.financials

#st.write(infos)