import yfinance as yf
import streamlit as st
import requests
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm

def build_pred_graph(ytrue, xtrue, ypred):
    fig, axs = plt.subplots(1,1,figsize=(7,5))
    sns.scatterplot(
        x=xtrue.reshape(1,-1)[0], 
        y=ytrue.reshape(1,-1)[0], 
        hue=ytrue.reshape(1,-1)[0],
        ax=axs
    )
    plt.plot(xtrue, ypred)
    plt.xlabel('Premium')
    plt.ylabel('Profitability')
    plt.legend([])
    return fig

@st.cache_resource
def download_ticker_returns(op, start_date, end_date):
    df = yf.download(
        op, start=start_date, end=end_date, progress=False, interval='1mo')
    roi = df['Adj Close'].pct_change().dropna().reset_index()
    return roi

def download_bond_data(start_date, end_date):
    fisc_api = f'https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v2/accounting/od/avg_interest_rates?page[size]=2166&&filter=record_date:gte:{start_date}'
    fiscdata = requests.get(fisc_api).json()
    yeild_ = pd.DataFrame(fiscdata['data'])
    yeild_ = yeild_[(yeild_['security_desc'] == 'Treasury Bonds') & (yeild_['security_type_desc'] == 'Marketable')][['record_date','avg_interest_rate_amt']]
    yeild_['record_date'] = pd.to_datetime(yeild_['record_date']) + pd.Timedelta(days=1)
    yeild_['avg_interest_rate_amt'] = pd.to_numeric(yeild_['avg_interest_rate_amt'])
    yeild_['avg_interest_rate_amt'] *= .01
    return yeild_

def build_the_model(x, y):
    x = x.to_numpy().reshape(-1,1)
    y = y.to_numpy().reshape(-1,1)
    reg_sklearn = LinearRegression()
    reg_sklearn.fit(x, y)
    yPredicted = reg_sklearn.predict(x)
    X = sm.add_constant(x)
    reg = sm.OLS(y, X).fit()
    b0, b1 = reg.params
    yHatText = f'y = {round(b0,5)} + {round(b1,5)}x'
    metrics = {
        'mse': mean_squared_error(y, yPredicted),
        'r2': r2_score(y, yPredicted),
        'eq': yHatText
    }
    yPredicted = yPredicted.reshape(1,-1)[0]
    x = x.reshape(1,-1)[0]
    y = y.reshape(1,-1)[0]
    figure = build_pred_graph(y, x, yPredicted)
    return reg_sklearn, figure, metrics
        

    