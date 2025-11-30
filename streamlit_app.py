import streamlit as st
import pandas as pd


st.title('🎈 Machine Learning Tienda Aurelion App')

st.info('Modelo de Machine Learning para tienda!')

# Use the "raw" GitHub URL instead of the "blob" URL
#csv_url = 'https://github.com/ChristianMadoz/data/blob/main/df_aurelion.csv?plain=1'
#df = pd.read_csv(csv_url)

df = pd.read_csv('https://raw.githubusercontent.com/ChristianMadoz/data/refs/heads/main/df_aurelion.csv')
df
