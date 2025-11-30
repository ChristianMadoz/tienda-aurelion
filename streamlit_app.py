import streamlit as st
import pandas as pd


st.title('🎈 Machine Learning Tienda Aurelion App')

st.info('Modelo de Machine Learning para tienda!')

# Use the "raw" GitHub URL instead of the "blob" URL
csv_url = 'https://raw.githubusercontent.com/ChristianMadoz/data/blob/main/df_aurelion.csv'
df = pd.read_csv(csv_url)

#df = pd.read_csv('https://github.com/ChristianMadoz/data/blob/main/df_aurelion.csv')
df
