import streamlit as st
from components.slidebar_component import slidebar_tweaker
from components.df_component import dataframe_shower

st.set_page_config(
    page_title="CAPM UI | home",
    page_icon="📈",
)

st.title('CAPM UI 📈')
st.markdown('''
This app lets you automatically create a single factor
CAPM model based on interactive portfolio of predefined stocks: `TSLA`,
`MSFT`, `AAPL`, `GOOGL` and `META`. You can read more on what is CAPM model, 
            why and how it can be used in [my research](https://github.com/turkunov/CAPM_UI/blob/main/paper.ipynb).
''')
st.sidebar.info('''
Tweak parameters below before passing them to the model. For parameters explanation, please,
refer to docs page.
''')

def main():
    op_eval, start, end, volumes, chosen_tickers = slidebar_tweaker()
    if st.sidebar.button('Send'):
        dataframe_shower(start, end, op_eval, volumes, chosen_tickers)

if __name__ == '__main__':
    main()