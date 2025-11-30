import streamlit as st
import pandas as pd


st.title('🎈 Machine Learning Tienda Aurelion App')

st.info('Modelo de Machine Learning para tienda!')

df = pd.read_csv('https://github.com/ChristianMadoz/data/blob/main/df_aurelion.csv')
df
