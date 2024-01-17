# main.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Función para cargar los datos
@st.experimental_memo
def load_data():
    data_path = "Data/Skyserver_SQL2_27_2018 6_51_39 PM.csv"
    return pd.read_csv(data_path)

# Configuración inicial de Streamlit
def setup_streamlit():
    st.set_page_config(page_title="Explorador de Datos Astronómicos", page_icon=":telescope:", layout="wide")

# Creación de la barra lateral para opciones de filtrado
def create_sidebar(data):
    with st.sidebar:
        st.title("Opciones de Filtrado")
        class_option = st.selectbox("Selecciona la Clase de Objeto:", ["Todos", "GALAXY", "STAR", "QSO"])
        return data if class_option == "Todos" else data[data["class"] == class_option]

# Función para mostrar el mapa celeste
def show_celestial_map(data):
    fig = px.scatter(data, x="ra", y="dec", color="class", title="Distribución de Objetos en el Cielo")
    st.plotly_chart(fig, use_container_width=True)

# Función para mostrar análisis de datos
def show_data_analysis(data):
    bandas = ["u", "g", "r", "i", "z"]
    for banda in bandas + ["redshift"]:
        st.subheader(f"Histograma para {banda.upper()}")
        fig, ax = plt.subplots()
        sns.histplot(data=data, x=banda, kde=True, ax=ax)
        st.pyplot(fig)

# Función principal que organiza la aplicación Streamlit
def main():
    setup_streamlit()
    data = load_data()
    filtered_data = create_sidebar(data)

    st.title("Explorador de Datos Astronómicos")
    st.markdown("Esta aplicación interactiva permite explorar un conjunto de datos astronómicos, incluyendo la clasificación de galaxias, estrellas y quásares.")

    tab1, tab2 = st.tabs(["Mapa Celeste", "Análisis de Datos"])

    with tab1:
        st.subheader("Mapa Celeste")
        show_celestial_map(filtered_data)

    with tab2:
        st.subheader("Análisis de Datos")
        show_data_analysis(filtered_data)

if __name__ == "__main__":
    main()
