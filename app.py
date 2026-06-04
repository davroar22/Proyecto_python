import streamlit as st
import pandas as pd
from transport_data import build_network_from_csv

st.set_page_config(
    page_title="Optimizador de Rutas de Transporte",
    page_icon="🚌",
    layout="centered",
)

graph = build_network_from_csv("network_edges.csv")
stations = sorted(list(graph.stations))

st.title("🚌 Optimizador de Rutas de Transporte")
st.write("Encuentra la mejor ruta entre dos estaciones.")
st.info("Red cargada desde archivo CSV.")

with st.sidebar:
    st.header("Configuración")
    transfer_penalty = st.slider(
        "Penalización por transbordo (minutos)",
        min_value=0,
        max_value=15,
        value=4,
        step=1,
    )

origin = st.selectbox("Selecciona estación de origen", stations)
destination = st.selectbox("Selecciona estación de destino", stations)

if st.button("Calcular mejor ruta", type="primary"):
    if origin == destination:
        st.warning("El origen y el destino no pueden ser la misma estación.")
    else:
        result = graph.shortest_path(origin, destination, transfer_penalty=transfer_penalty)

        if result is None:
            st.error("No se encontró una ruta disponible entre esas estaciones.")
        else:
            st.success("Ruta encontrada")

            st.subheader("Resumen")
            col1, col2, col3 = st.columns(3)
            col1.metric("Costo total", f"{result['total_cost']} min")
            col2.metric("Transbordos", result["transfers"])
            col3.metric("Rutas usadas", len(result["routes_used"]))

            st.subheader("Recorrido")
            st.write(" → ".join(result["path"]))

            st.subheader("Buses/Rutas utilizadas")
            for i, route in enumerate(result["routes_used"], start=1):
                st.write(f"{i}. {route}")

            st.subheader("Detalle")
            st.json(result)

st.markdown("---")

st.subheader("Aprendizaje no supervisado")
st.write(
    "En esta sección se analizan patrones ocultos de movilidad, agrupación de viajes y detección de comportamientos similares sin variable objetivo."
)

if pd.io.common.file_exists("trip_records.csv"):
    df_unsup = pd.read_csv("trip_records.csv")
    st.write("Muestra de datos para aprendizaje no supervisado:")
    st.dataframe(df_unsup.head(10))
else:
    st.warning("No se encontró trip_records.csv")

st.markdown("---")

st.header("Aprendizaje supervisado")
st.write(
    "En esta sección se utilizan datos etiquetados para predecir variables como tiempo real de viaje o retraso alto."
)

if pd.io.common.file_exists("trip_records_supervised.csv"):
    df_sup = pd.read_csv("trip_records_supervised.csv")
    st.write("Muestra de datos para aprendizaje supervisado:")
    st.dataframe(df_sup.head(10))
else:
    st.warning("No se encontró trip_records_supervised.csv")

st.markdown("---")
st.caption("Desarrollado en Python + Streamlit")