import streamlit as st
from utils import build_the_model

def graphs_generator(x, y):
    equation, fig, metrics = build_the_model(x, y)
    st.pyplot(fig)
    st.markdown(
    f'''
    Metric results:
    * $R^2={round(metrics["r2"], 3)}$
    * $MSE={round(metrics["mse"], 3)}$
    ''')
    st.markdown(f'Equation: ${metrics["eq"]}$')