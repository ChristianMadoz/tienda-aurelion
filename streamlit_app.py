import streamlit as st
import pandas as pd
import folium
import json
import requests
from streamlit_folium import st_folium

# st.set_page_config debe ir al principio de la aplicación y fuera de cualquier función o bloque.
st.set_page_config(layout="wide")

st.title('🎈 Machine Learning Tienda Aurelion App')
st.info('Modelo de Machine Learning para tienda!')

with st.expander('Data'):
    st.write('**Raw Data**')
    df = pd.read_csv('https://raw.githubusercontent.com/ChristianMadoz/data/refs/heads/main/dataset_ventas_unificado_completo.csv')
    st.dataframe(df)
    st.write('**X**')
    x = df.drop('nombre_producto', axis=1)
    st.dataframe(x)
    st.write('**Y**')
    y = df.nombre_producto
    st.dataframe(y)

with st.expander('Data Visualization'):
    st.bar_chart(data=df, x='ciudad', y='importe', use_container_width=True)

with st.expander('Map Visualization (Ventas por Departamento)'):
    if 'ciudad' not in df.columns or 'importe' not in df.columns:
        st.warning("Asegúrate de tener las columnas 'ciudad' e 'importe' en tu CSV para esta visualización.")
        # Usamos st.empty() para no mostrar nada si no hay datos
        st.empty() 
    else:
        # 1. Agrupar los datos de ventas por departamento
        ventas_por_depto = df.groupby('ciudad')['importe'].sum().reset_index()
        url_cordoba_geojson = 'https://raw.githubusercontent.com/mgaitan/departamentos_argentina/refs/heads/master/departamentos-cordoba.json''

        try:
            # 2. Descargar y cargar el GeoJSON
            response = requests.get(url_cordoba_geojson)
            if response.status_code != 200:
                st.error("Error al descargar el GeoJSON de Córdoba.")
                st.empty() 
            geo_json_data = response.json()

            # 3. FUSIONAR LOS DATOS DE VENTAS CON EL GEOJSON
            # Crear un diccionario de ventas para una búsqueda más rápida
            ventas_dict = ventas_por_depto.set_index('ciudad')['importe'].to_dict()

            # Recorrer el GeoJSON y añadir la propiedad del importe
            for feature in geo_json_data['features']:
                depto_nombre = feature['properties']['departamento']
                importe_vendido = ventas_dict.get(depto_nombre, 0)
                feature['properties']['importe_vendido'] = f"${importe_vendido:,.2f}"

            # 4. Crear el mapa base de Folium centrado en Córdoba
            m_choropleth = folium.Map(location=[-31.4167, -64.1833], zoom_start=7)

            # 5. Crear la capa coroplética (los colores)
            folium.Choropleth(
                geo_data=geo_json_data,
                name='Ventas Departamentos Córdoba',
                data=ventas_por_depto,
                columns=["ciudad", "importe"],
                key_on="feature.properties.departamento",
                fill_color='YlGn',
                fill_opacity=0.7,
                line_opacity=0.4,
                legend_name="Importe total de ventas ($)"
            ).add_to(m_choropleth)

            # 6. Añadir la capa GeoJson interactiva para el tooltip
            folium.GeoJson(
                geo_json_data,
                name='Interactividad',
                tooltip=folium.features.GeoJsonTooltip(
                    fields=['departamento', 'importe_vendido'],
                    aliases=['Departamento:', 'Ventas Totales:'],
                    localize=True
                ),
                highlight_function=lambda x: {'weight': 3, 'color': 'black', 'dashArray': '1,1'}
            ).add_to(m_choropleth)

            # 7. Añadir control de capas
            folium.LayerControl().add_to(m_choropleth)

            # 8. Renderizar el mapa y capturar la interacción
            map_data = st_folium(m_choropleth, width=750, height=500)

            # 9. Procesar la selección del usuario
            if map_data and "last_active_feature" in map_data:
                props = map_data["last_active_feature"]["properties"]
                st.success(f"Seleccionado: **{props['departamento']}** | Importe: **{props['importe_vendido']}**")

        except Exception as e:
            st.error(f"Error al cargar el mapa coroplético o los datos: {e}")
            st.warning("Verifica que los nombres de tus 'ciudad' (departamentos) coincidan exactamente con el GeoJSON.")
