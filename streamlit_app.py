import streamlit as st
import pandas as pd
import folium
import json # Necesario para cargar el GeoJSON
from streamlit_folium import st_folium
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
  #st.map(df, lat, lon, width ="stretch", height=500)
  #st.map(datos=Ninguno, *, latitud=Ninguno, longitud=Ninguno, color=Ninguno, tamaño=Ninguno, zoom=Ninguno, ancho="estirar", alto=500, ancho_del_contenedor_de_uso=Ninguno)

  m = folium.Map(location=[-33.43144133557529, -63.28125000000001], zoom_start=4)
  folium.Marker(location=[-33.43144133557529, -63.28125000000001]).add_to(m)
  
  st.set_page_config(layout="wide") # Opcional: mejora la visualización del mapa ancho
  
  # Renderiza el mapa y captura el resultado de la interacción del usuario
  map_data = st_folium(m, width=700, height=500)

with st.expander('Map Visualization: Ventas por Provincia'):
    # 1. Agrupar los datos por provincia y sumar el importe total de ventas
    # Asumimos que la columna 'ciudad' existe en tu CSV. Si no, cámbiala por la columna correcta.
    ventas_por_provincia = df.groupby('ciudad')['importe'].sum().reset_index()

    # 2. Cargar el archivo GeoJSON de Argentina (Provincias)
    # URL pública del GeoJSON desde datos.gob.ar
    geo_data = "https://raw.githubusercontent.com/mgaitan/departamentos_argentina/refs/heads/master/departamentos-cordoba.json"
    
    # Intentamos cargar el GeoJSON
    try:
        # Cargar el archivo JSON para que Folium lo use
        # En una app real, es mejor descargarlo y guardarlo localmente si el enlace cambia
        import requests
        geo_data = requests.get(geo_data).json()

        # 3. Crear el mapa base de Folium centrado en Argentina
        m = folium.Map(location=[-34.6037, -58.3816], zoom_start=7)

        # 4. Crear el mapa coroplético (Choropleth Map)
        folium.Choropleth(
            geo_data=geo_data,
            name="choropleth",
            data=df,
            columns=["ciudad","importe"],
            key_on="feature.properties.departamento", 
            fill_color ='YlGn',
            fill_opacity=0.7,
            line_opacity=0.2,
            #threshold_scale=[0, 200000, 400000, 600000, 800000, 1000000],
            legend_name="Importe total (%)",
            folium.GeoJson(geo_data, highlight_function=lambda feature: {"fillColor": ("green" if "e" in feature["properties"]["name"].lower() else "#ffff00"),},).add_to(m)

        #folium.GeoJson(geo_data, highlight_function=lambda feature: {"fillColor": ("green" if "e" in feature["properties"]["name"].lower() else "#ffff00"),},).add_to(m)
        # Añadir control de capas (opcional)
        folium.LayerControl().add_to(m)

        # 5. Renderizar el mapa en Streamlit
        st_folium(m, width=750, height=500)
      
        # Solo intenta escribir los datos si map_data no es None
        if map_data is not None:
          pass # Usamos 'pass' si realmente no queremos mostrar nada
        else:
          st.error(f"Error al descargar el GeoJSON. Código de estado: {response.status_code}")
          st.write("Contenido de la respuesta:", response.text)

    except Exception as e:
        st.error(f"Error al cargar el mapa coroplético o los datos: {e}")
        st.warning("Asegúrate de que la columna 'provincia' exista en tu CSV y que los nombres de provincia coincidan con el GeoJSON.")    
  
#st.write("Datos del último clic en el mapa:")
# map_data contendrá un diccionario con información como 'last_clicked'
#st.write(map_data)
