import streamlit as st
import datetime
import numpy as np
from utils import download_ticker_returns, download_bond_data
from components.graphs_component import graphs_generator

def dataframe_shower(start_date, end_date, op_eval, volumes, chosen_tickers):
    if op_eval in chosen_tickers:
        if start_date < end_date:
            volumes = np.array(volumes) * .01
            roi = download_ticker_returns(' '.join(chosen_tickers), start_date, end_date)
            bond = download_bond_data(start_date, end_date)
            roi_and_yield = roi.merge(bond, left_on='Date', right_on='record_date') \
                [['Date', 'avg_interest_rate_amt'] + chosen_tickers]
            roi_and_yield['mu_m'] = np.sum(roi_and_yield[chosen_tickers] * volumes, axis=1)
            roi_and_yield['premium'] = roi_and_yield['mu_m'] - roi_and_yield['avg_interest_rate_amt']
            roi_and_yield.rename(columns=
                                {'avg_interest_rate_amt':'bond yield',
                                'Date': 'mo/y'
                                }, inplace=True)
            roi_and_yield['mo/y'] = roi_and_yield['mo/y'].dt.strftime('%m/%Y')
            dfcol, graphcol = st.columns(2)
            st.sidebar.success('Successfully loaded the data. See results on the right!')
            with dfcol:
                st.header('Last 10 ROIs and bond yields')
                st.dataframe(roi_and_yield.tail(10))
            with graphcol:
                st.header('CAPM model on ticker of interest')
                graphs_generator(roi_and_yield['premium'],
                                roi_and_yield[op_eval])
        else:
            st.sidebar.error('Error: End date must be before start date')
    else:
        st.sidebar.error('Error: Ticker of interest must be amongst selected ones')
