import streamlit as st
import pandas as pd
import folium
import json
import requests # Importar requests aquí arriba
from streamlit_folium import st_folium

# st.set_page_config debe ir al principio de la aplicación
st.set_page_config(layout="wide")

st.title('🎈 Machine Learning Tienda Aurelion App')
st.info('Modelo de Machine Learning para tienda!')

with st.expander('Data'):
    st.write('**Raw Data**')
    df = pd.read_csv('https://raw.githubusercontent.com/ChristianMadoz/data/refs/heads/main/dataset_ventas_unificado_completo.csv')
    st.dataframe(df) # Usamos st.dataframe para mejor visualización
    st.write('**X**')
    x = df.drop('nombre_producto', axis = 1)
    st.dataframe(x)
    st.write('**Y**')
    y = df.nombre_producto
    st.dataframe(y)

with st.expander('Data Visualization'):
    # Asegúrate de usar la columna 'importe' para ventas si es lo que quieres graficar
    st.bar_chart(data=df, x='ciudad', y='importe', use_container_width=True)

with st.expander('Map Visualization (Mapa Base de Córdoba)'):
    # Usamos la URL de departamentos de Córdoba definida aquí
    url_cordoba_geojson = 'https://raw.githubusercontent.com/mgaitan/departamentos_argentina/refs/heads/master/departamentos-cordoba.json'
    
    # Creamos un mapa base centrado en Córdoba, sin datos por ahora
    m = folium.Map(location=[-31.4167, -64.1833], zoom_start=7) # Coordenadas de Córdoba capital
    
    # Simplemente añadimos el GeoJSON como una capa visual simple
    folium.GeoJson(url_cordoba_geojson, name="Límites Departamentos Córdoba").add_to(m)
    
    # Renderizamos el mapa base
    st_folium(m, width=700, height=500)

with st.expander('Map Visualization: Ventas por Departamento (Interactivo)'):
    
    if 'ciudad' not in df.columns or 'importe' not in df.columns:
        st.warning("Asegúrate de tener las columnas 'ciudad' e 'importe' en tu CSV.")
        st.stop()
        
    # Agrupamos los datos
    ventas_por_depto = df.groupby('ciudad')['importe'].sum().reset_index()
    url_cordoba_geojson = 'https://raw.githubusercontent.com/mgaitan/departamentos_argentina/refs/heads/master/departamentos-cordoba.json'
    
    try:
        response = requests.get(url_cordoba_geojson)
        if response.status_code != 200:
            st.error("Error al descargar el GeoJSON de Córdoba.")
            st.stop()
            
        geo_json_data = response.json()

        # --- FUSIONAR DATOS: AÑADIMOS EL IMPORTE AL OBJETO JSON ---
        # Recorremos cada departamento en el JSON y añadimos su importe de ventas
        for feature in geo_json_data['features']:
            depto_nombre = feature['properties']['departamento']
            # Buscamos el importe en nuestro DataFrame de ventas agrupadas
            importe = ventas_por_depto[ventas_por_depto['ciudad'] == depto_nombre]['importe']
            
            if not importe.empty:
                # Añadimos una nueva propiedad al JSON llamada 'importe_vendido'
                feature['properties']['importe_vendido'] = f"${importe.iloc[0]:,.2f}"
            else:
                feature['properties']['importe_vendido'] = "Sin ventas"

            # 3. Crear el mapa base de Folium centrado en Córdoba
            m_choropleth = folium.Map(location=[-31.4167, -64.1833], zoom_start=7)

            # 4. Crear el mapa coroplético (Choropleth Map)
            folium.Choropleth(
                geo_data=geo_json_data,
                name='Ventas Departamentos Córdoba', # Nombre de la capa (string)
                data=ventas_por_depto,
                columns=["ciudad", "importe"],
                key_on="feature.properties.departamento", # Clave en el GeoJSON
                fill_color='YlGn', # Esquema de color
                fill_opacity=0.7,
                line_opacity=0.2,
                legend_name="Importe total de ventas ($)"
            ).add_to(m_choropleth)
            
            folium.GeoJson(geo_json_data,
                name='Interactividad',
                tooltip=folium.features.GeoJsonTooltip(fields=['departamento'], aliases=['Departamento:']),
                highlight_function=lambda x: {'weight': 3, 'color': 'black', 'dashArray': '1,1'}).add_to(m_choropleth)
    
            # Añadir control de capas (opcional)
            folium.LayerControl().add_to(m_choropleth)
    
            # 6. Renderizar el mapa en Streamlit y CAPTURAR DATOS DE INTERACCIÓN
            map_data = st_folium(m_choropleth, width=750, height=500)
            
            # 7. Procesar la selección del usuario
            if map_data is not None and "last_active_feature" in map_data:
                # Capturar el nombre del departamento que fue clickeado/activo
                depto_seleccionado = map_data["last_active_feature"]["properties"]["departamento"]
                st.success(f"Departamento seleccionado: **{depto_seleccionado}**")              
            
        else:
            st.error(f"Error al descargar el GeoJSON. Código de estado: {response.status_code}")

    except Exception as e:
        st.error(f"Error al cargar el mapa coroplético o los datos: {e}")
        st.warning("Asegúrate de que los nombres de tus 'ciudad' (departamentos) coincidan exactamente con el GeoJSON (ej. 'Capital', 'Río Cuarto').")
