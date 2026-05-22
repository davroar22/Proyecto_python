import streamlit as st
from transport_data import build_sample_network

st.set_page_config(
    page_title="Optimizador de Rutas de Transporte",
    page_icon="🚌",
    layout="centered"
)

graph = build_sample_network()
stations = sorted(list(graph.stations))

st.title("🚌 Optimizador de Rutas de Transporte")
st.write("Encuentra la mejor ruta entre dos estaciones.")
st.info("Ejemplo demostrativo inspirado en estaciones tipo TransMilenio. Los datos no son oficiales.")

with st.sidebar:
    st.header("Configuración")
    transfer_penalty = st.slider(
        "Penalización por transbordo (minutos)",
        min_value=0,
        max_value=15,
        value=4,
        step=1
    )

origin = st.selectbox("Selecciona estación de origen", stations, index=stations.index("Portal Sur"))
destination = st.selectbox("Selecciona estación de destino", stations, index=stations.index("Universidad Nacional"))

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
st.caption("Desarrollado en Python + Streamlit")