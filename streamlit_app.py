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
  st.bar_chart(data=df, x = 'ciudad', y = 'id_venta',y_label = 'Monto Ventas')
  #st.bar_chart(datos=df, x=Ninguno, y=Ninguno, etiqueta_x=Ninguno, etiqueta_y=Ninguno, color=Ninguno, horizontal=Falso, orden=Verdadero, pila=Ninguno, ancho="estirar", alto="contenido", ancho_del_contenedor_de_uso=Ninguno)


with st.expander('Map Visualization'):
  st.map(data=df, lat = 34, lon = 63, width ="stretch", height=500)

#st.map(datos=Ninguno, *, latitud=Ninguno, longitud=Ninguno, color=Ninguno, tamaño=Ninguno, zoom=Ninguno, ancho="estirar", alto=500, ancho_del_contenedor_de_uso=Ninguno)
