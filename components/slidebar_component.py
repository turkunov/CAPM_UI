import streamlit as st
import datetime

def on_volumechange(last_key):
    volume = st.session_state[last_key]

    # uncomment if debug is necessary
    # print(f'{last_key} is changed with {volume}. Current state: {st.session_state}')

    remaining_tickers = [t for t in st.session_state['choices'] if t != last_key]
    n_of_tickers = len(st.session_state['choices']) - 1
    for t in remaining_tickers:
        st.session_state[f'last_{t}'] = st.session_state[t]
        st.session_state[t] = round((100 - volume) / n_of_tickers, 3)

    st.session_state[f'last_{last_key}'] = volume

def slidebar_tweaker():
    TICKER_CHOICES = ['TSLA', 'AAPL', 'GOOGL', 'MSFT', 'META']
    for all_t in TICKER_CHOICES:
        st.session_state[f'last_{all_t}'] = 0

    today = datetime.date.today()
    start_date = st.sidebar.date_input('Start date')
    end_date = st.sidebar.date_input('End date', today)
    option_eval = st.sidebar.text_input('Ticker of interest', value='TSLA')
    option_eval = option_eval.upper()
    options = st.sidebar.multiselect(
    'Select tickers',
    TICKER_CHOICES,
    ['TSLA', 'MSFT'],
    key='choices')
    slider_components = []
    for option in st.session_state['choices']:
        slider_components.append(st.sidebar.slider(
            f'% of {option} in the portfolio', 1, 100, 
            0, key=option, on_change=on_volumechange,
            args=[option]
        ))
    return option_eval, start_date, end_date, \
    [st.session_state[t] for t in st.session_state['choices']], st.session_state['choices']