import streamlit as st

st.set_page_config(
    page_title="CAPM UI | docs",
    page_icon="📕",
)

st.markdown('''
Parameters:
* `Start date`: historical date **from** which the data is going to be pulled
* `End date`: historical date **till** which the data is going to be pulled 
* `Ticker of interst`: which ticker is going to be passed into the CAPM model
* `Select tickers`: select stocks for the portfolio
* `% of ... in the portfolio`: select % of shares each stock takes up in the portfolio
''')
st.markdown('''
Click "**Send**" button after you've finished
choosing parameters.     
''')