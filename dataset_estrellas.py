import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Configuración inicial de la página
st.set_page_config(page_title="Explorador de Datos Astronómicos", page_icon=":telescope:", layout="wide")

# Cargando el dataset
@st.experimental_memo
def load_data():
    data_path = "Data/Skyserver_SQL2_27_2018 6_51_39 PM.csv"
    data = pd.read_csv(data_path)
    return data

data = load_data()

# Sidebar para filtros y opciones
with st.sidebar:
    st.title("Opciones de Filtrado")
    class_option = st.selectbox("Selecciona la Clase de Objeto:", ["Todos", "GALAXY", "STAR", "QSO"])
    filtered_data = data if class_option == "Todos" else data[data["class"] == class_option]

# Cabecera y Descripción
st.title("Explorador de Datos Astronómicos")
st.markdown("""
Esta aplicación interactiva permite explorar un conjunto de datos astronómicos,
incluyendo la clasificación de galaxias, estrellas y quásares.
""")

# Usando pestañas para organizar diferentes secciones
tab1, tab2, tab3 = st.tabs(["Mapa Celeste", "Análisis de Datos", "Detalles de Observación"])

with tab1:
    st.subheader("Mapa Celeste")
    fig = px.scatter(filtered_data, x="ra", y="dec", color="class", title="Distribución de Objetos en el Cielo")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Análisis de Datos")
    bandas = ["u", "g", "r", "i", "z"]
    for banda in bandas + ["redshift"]:
        st.subheader(f"Histograma para {banda.upper()}")
        fig, ax = plt.subplots()
        sns.histplot(data=filtered_data, x=banda, kde=True, ax=ax)
        st.pyplot(fig)
    st.subheader("Clasificación de Objetos")
    class_count = filtered_data['class'].value_counts()
    st.bar_chart(class_count)

with tab3:
    st.subheader("Detalles de Observación")
    observation_details = ["run", "camcol", "field"]
    for detail in observation_details:
        fig = px.histogram(filtered_data, x=detail, color="class", title=f"Distribución por {detail.capitalize()}")
        st.plotly_chart(fig, use_container_width=True)

# Usando columnas para organizar el contenido adicional
col1, col2 = st.columns(2)
with col1:
    st.subheader("Proporción de Clasificaciones de Objetos")
    fig, ax = plt.subplots()
    ax.pie(class_count, labels=class_count.index, autopct='%1.1f%%')
    st.pyplot(fig)

with col2:
    st.subheader("Datos Brutos")
    if st.checkbox("Mostrar datos brutos"):
        st.write(filtered_data)

# Nota: Este código es un esqueleto y puede necesitar ajustes según la estructura exacta del dataset y los requerimientos específicos.
