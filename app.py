import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Dashboard de ventas",
    page_icon="📊",
    layout="wide"
)

# Datos de ejemplo
datos = {
    "Fecha": [
        "2026-01-05", "2026-01-12", "2026-02-03",
        "2026-02-15", "2026-03-02", "2026-03-18",
        "2026-04-07", "2026-04-20", "2026-05-09",
        "2026-05-22", "2026-06-04", "2026-06-19"
    ],
    "Producto": [
        "Laptop", "Mouse", "Teclado", "Monitor",
        "Laptop", "Audifonos", "Mouse", "Monitor",
        "Teclado", "Laptop", "Audifonos", "Mouse"
    ],
    "Categoria": [
        "Computadoras", "Accesorios", "Accesorios",
        "Pantallas", "Computadoras", "Accesorios",
        "Accesorios", "Pantallas", "Accesorios",
        "Computadoras", "Accesorios", "Accesorios"
    ],
    "Precio": [
        12000, 250, 600, 3500, 12000, 450,
        250, 3500, 600, 12000, 450, 250
    ],
    "Cantidad": [2, 5, 3, 1, 1, 4, 8, 2, 5, 1, 3, 6],
    "Pago": [
        "Tarjeta", "Efectivo", "Tarjeta", "Transferencia",
        "Efectivo", "Tarjeta", "Efectivo", "Transferencia",
        "Tarjeta", "Transferencia", "Efectivo", "Tarjeta"
    ]
}

df = pd.DataFrame(datos)
df["Fecha"] = pd.to_datetime(df["Fecha"])
df["Total"] = df["Precio"] * df["Cantidad"]
df["Mes"] = df["Fecha"].dt.strftime("%Y-%m")

# Titulo
st.title("Dashboard de ventas")
st.write("Consulta y analiza los registros de ventas.")

# Barra lateral
st.sidebar.header("Controles")

categorias = st.sidebar.multiselect(
    "Categoria",
    options=sorted(df["Categoria"].unique()),
    default=sorted(df["Categoria"].unique())
)

meses = st.sidebar.multiselect(
    "Mes",
    options=sorted(df["Mes"].unique()),
    default=sorted(df["Mes"].unique())
)

pagos = st.sidebar.multiselect(
    "Metodo de pago",
    options=sorted(df["Pago"].unique()),
    default=sorted(df["Pago"].unique())
)

# Busqueda por texto
busqueda = st.text_input("Buscar producto")

# Aplicar filtros
filtrado = df[
    df["Categoria"].isin(categorias)
    & df["Mes"].isin(meses)
    & df["Pago"].isin(pagos)
]

if busqueda:
    filtrado = filtrado[
        filtrado["Producto"].str.contains(
            busqueda, case=False, na=False
        )
    ]

# Indicadores
col1, col2, col3 = st.columns(3)

col1.metric("Ventas totales", f"${filtrado['Total'].sum():,.2f}")
col2.metric("Unidades vendidas", int(filtrado["Cantidad"].sum()))
col3.metric("Registros", len(filtrado))

st.divider()

# Mostrar u ocultar la tabla
mostrar_datos = st.checkbox("Mostrar base de datos")

if mostrar_datos:
    st.subheader("Registros de ventas")
    st.dataframe(filtrado, use_container_width=True)

# Grafica 1
st.subheader("Ventas por categoria")
ventas_categoria = filtrado.groupby("Categoria")["Total"].sum()
st.bar_chart(ventas_categoria)

# Grafica 2
st.subheader("Ventas por mes")
ventas_mes = filtrado.groupby("Mes")["Total"].sum().sort_index()
st.line_chart(ventas_mes)

# Grafica 3
st.subheader("Ventas por metodo de pago")
ventas_pago = filtrado.groupby("Pago")["Total"].sum()
st.bar_chart(ventas_pago)

# Acerca de
st.divider()
st.subheader("Acerca de")

st.write("Autora: Angélica Martínez Hernández")
st.write("Carrera: Licenciatura en Ingeniería de Software")
st.write("Matrícula: zS26004664")

st.write("Ciudad natal: Coscomatepec,Ver.")
st.map(
  pd.DataFrame({
    "lat": [19.072775],
    "lon": [-97.04685]
  }),
  latitude="lat",
  longitude="lon",
  zoom=12
)


