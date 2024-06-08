import streamlit as st
import pandas as pd
import numpy as np
from babel.numbers import format_currency

def buy_currency(currency):
    return round(currency + (currency * 0.00175), 2)

def sell_currency(currency):
    return round(currency - (currency * 0.00175), 2)

# read csv data
data = pd.read_csv('game_data_v01.csv')
date_list = data['date']
currency_list = data['usd_krw']
usd_index_list = data['usd_index']

print(date_list)

# ramdom int number in 500~4500
if 'account_krw' not in st.session_state:
    st.session_state.account_krw = 10000000

if 'account_usd' not in st.session_state:
    st.session_state.account_usd = 0

if 'start_index' not in st.session_state:
    st.session_state['start_index'] = np.random.randint(500, 4500)

if 'today_number' not in st.session_state:
    st.session_state['today_number'] = 1

today_number = st.session_state['today_number']
current_index = st.session_state['start_index'] + today_number

remaining_second = 60

# st.text(f'today_number: {today_number}')
# st.text(f'current_index: {current_index}')

today_currency = currency_list[current_index]
today_buy_currency = buy_currency(today_currency)
today_sell_currency = sell_currency(today_currency)
today_usd_index = usd_index_list[current_index]

st.title(f'Day {today_number}')
# st.text(f'오늘 날짜: {date_list[current_index]}')
st.text(f'남은 시간 : {remaining_second}초')

st.text(f"보유 원화: {format_currency(st.session_state.account_krw, 'KRW', locale='ko_KR')} 원")
st.text(f"보유 달러: {format_currency(st.session_state.account_usd, 'USD', locale='en_US')} 달러")

st.subheader('현재 환율')
col_1_1, col_1_2, col_1_3, col_1_4 = st.columns(4)
col_1_1.metric('기준환율', today_currency)
col_1_2.metric('살때', today_buy_currency)
col_1_3.metric('팔때', today_sell_currency)
col_1_4.metric('USD Index', today_usd_index)

if st.button("Next Day"):
    st.session_state['today_number'] = today_number + 1

st.divider()

col_2_1, col_2_2 = st.columns(2)

# 원화 -> 달러 환전
if 'buying_krw' not in st.session_state:
  st.session_state.buying_krw = 0

if 'buying_usd' not in st.session_state:
  st.session_state.buying_usd = 0

col_2_1.subheader('원화 -> 달러 환전')

buying_krw = col_2_1.number_input("원화", value=st.session_state.buying_krw, key='buying_krw_input', disabled=True)
buying_usd = col_2_1.number_input("달러", value=st.session_state.buying_usd, key='buying_usd_input')

if st.session_state.buying_usd != buying_usd:
    st.session_state.buying_usd = buying_usd
    st.session_state.buying_krw = round(buying_usd * today_buy_currency, 2)
    st.experimental_rerun()

if col_2_1.button("달러 사기"):
    st.session_state.account_krw -= st.session_state.buying_krw
    st.session_state.account_usd += st.session_state.buying_usd
    st.session_state.buying_krw = 0
    st.session_state.buying_usd = 0
    st.experimental_rerun()


# 달러 -> 원화 환전
if 'selling_krw' not in st.session_state:
  st.session_state.selling_krw = 0

if 'selling_usd' not in st.session_state:
  st.session_state.selling_usd = 0

col_2_2.subheader('달러 -> 원화 환전')

selling_usd = col_2_2.number_input("달러", value=st.session_state.selling_usd, key='selling_usd_input')
col_2_2.number_input("원화", value=st.session_state.selling_krw, disabled=True, key='selling_krw_input')

if st.session_state.selling_usd != selling_usd:
    st.session_state.selling_usd = selling_usd
    st.session_state.selling_krw = round(selling_usd * today_sell_currency, 2)
    st.experimental_rerun()

if col_2_2.button("달러 팔기"):
    st.session_state.account_krw += st.session_state.selling_krw
    st.session_state.account_usd -= st.session_state.selling_usd
    st.session_state.selling_krw = 0
    st.session_state.selling_usd = 0
    st.experimental_rerun()