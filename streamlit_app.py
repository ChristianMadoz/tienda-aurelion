import streamlit as st
import pandas as pd


st.title('🎈 Machine Learning Tienda Aurelion App')

st.info('Modelo de Machine Learning para tienda!')

with st.expander('Data'):
  st.write('**Raw Data**')
  # Use the "raw" GitHub URL instead of the "blob" URL
  df = pd.read_csv('https://raw.githubusercontent.com/ChristianMadoz/data/refs/heads/main/dataset_ventas_unificado_completo.csv')
  df
  st.write('**X**')
  x = df.drop('nombre_producto', axis = 1)
  x
  st.write('**Y**')
  y = df.nombre_producto
  y

with st.expander('Data Visualization'):
  st.scatter_chart(data=df, x = 'productos', y = 'fecha', color = 'ciudad')
