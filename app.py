import streamlit as st
import pandas as pd

from data_loader import cargar_datos, cargar_mapa
from analysis import (
    calcular_kpis,
    evolucion_mensual,
    multas_por_hora,
    comparativa_anual,
    resumen_infracciones
)
from charts import (
    grafico_evolucion,
    grafico_horas,
    grafico_anual
)
from map import crear_hotspots


st.set_page_config(
    page_title="Madrid Traffic Intelligence",
    page_icon="🚦",
    layout="wide"
)


st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
        color: #f5f5f5;
    }

    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 4px;
    }

    .subtitle {
        font-size: 20px;
        color: #b8bec9;
        margin-bottom: 4px;
    }

    .caption {
        color: #8f98a8;
        margin-bottom: 28px;
    }

    div[data-testid="stMetric"] {
        background-color: #161b22;
        border: 1px solid #30363d;
        padding: 18px;
        border-radius: 12px;
    }

    div[data-testid="stMetricLabel"] {
        color: #9da7b5;
    }

    div[data-testid="stMetricValue"] {
        color: #ffffff;
    }

    h2 {
        margin-top: 35px;
    }

    .footer {
        text-align: center;
        color: #707885;
        margin-top: 50px;
        padding: 20px;
        border-top: 1px solid #30363d;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def cargar():
    df = cargar_datos()
    mapa = cargar_mapa()
    return df, mapa


# =========================================================
# CARGA DE DATOS
# =========================================================

df, mapa = cargar()


# =========================================================
# FILTROS
# =========================================================

st.sidebar.title("🎛️ Filtros")

anios = sorted(df["ANIO"].dropna().unique())

anios_seleccionados = st.sidebar.multiselect(
    "Año",
    options=anios,
    default=anios
)

calificaciones = sorted(
    df["CALIFICACION"].dropna().astype(str).unique()
)

calificaciones_seleccionadas = st.sidebar.multiselect(
    "Calificación",
    options=calificaciones,
    default=calificaciones
)

importes = sorted(df["IMP_BOL"].dropna().unique())

importes_seleccionados = st.sidebar.multiselect(
    "Importe de la multa (€)",
    options=importes,
    default=importes
)


# =========================================================
# APLICAR FILTROS
# =========================================================

df_filtrado = df[
    df["ANIO"].isin(anios_seleccionados)
    & df["CALIFICACION"].isin(calificaciones_seleccionadas)
    & df["IMP_BOL"].isin(importes_seleccionados)
].copy()


# =========================================================
# CABECERA
# =========================================================

st.markdown(
    '<div class="main-title">🚦 Madrid Traffic Intelligence</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">¿Dónde, cuándo y qué tipo de infracciones se concentran en Madrid?</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="caption">4,1 M de sanciones analizadas a partir de 19 archivos mensuales disponibles entre 2024 y 2026.</div>',
    unsafe_allow_html=True
)


# =========================================================
# CONTROL DE DATOS
# =========================================================

if df_filtrado.empty:
    st.warning("No hay sanciones que coincidan con los filtros seleccionados.")
    st.stop()


# =========================================================
# KPIs
# =========================================================

kpis = calcular_kpis(df_filtrado)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Sanciones",
        f"{kpis['total_multas']:,.0f}"
    )

with col2:
    st.metric(
        "Importe total de las sanciones",
        f"{kpis['importe_total']:,.0f} €"
    )

with col3:
    st.metric(
        "Multa media",
        f"{kpis['importe_medio']:,.2f} €"
    )

with col4:
    st.metric(
        "Con pérdida de puntos",
        f"{kpis['porcentaje_puntos']:.2f}%"
    )


# =========================================================
# EVOLUCIÓN
# =========================================================

st.header("Evolución de las sanciones")

datos_evolucion = evolucion_mensual(df_filtrado)

st.plotly_chart(
    grafico_evolucion(datos_evolucion),
    use_container_width=True
)


# =========================================================
# PRINCIPALES INFRACCIONES
# =========================================================

st.header("Principales infracciones")

tabla_infracciones = resumen_infracciones(
    df_filtrado,
    n=8
)

st.dataframe(
    tabla_infracciones.style.format({
        "N.º sanciones": "{:,.0f}",
        "% del total": "{:.2f}%",
        "Impacto económico": "{:,.0f} €",
        "Multa media": "{:,.2f} €"
    }),
    use_container_width=True,
    hide_index=True
)


# =========================================================
# HORAS
# =========================================================

st.header("¿Cuándo se concentran las sanciones?")

datos_horas = multas_por_hora(df_filtrado)

st.plotly_chart(
    grafico_horas(datos_horas),
    use_container_width=True
)


# =========================================================
# COMPARATIVA ANUAL
# =========================================================

st.header("Sanciones por año")

datos_anuales = comparativa_anual(df_filtrado)

st.plotly_chart(
    grafico_anual(datos_anuales),
    use_container_width=True
)


# =========================================================
# MAPA
# =========================================================

st.header("¿Dónde se concentran las sanciones?")

st.caption(
    "Mapa basado en una agregación geográfica independiente de 420 celdas espaciales."
)

st.plotly_chart(
    crear_hotspots(mapa),
    use_container_width=True
)


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        Madrid Traffic Intelligence · Python · Pandas · Plotly · Streamlit · SQLite
    </div>
    """,
    unsafe_allow_html=True
)
