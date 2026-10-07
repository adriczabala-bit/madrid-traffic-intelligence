import streamlit as st

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
    grafico_multa_media,
    grafico_horas,
    grafico_anual
)

from map import crear_hotspots


# ==========================================================
# CONFIGURACIÓN
# ==========================================================

st.set_page_config(
    page_title="Madrid Traffic Intelligence",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================================
# ESTILO
# ==========================================================

st.markdown(
    """
    <style>

    .main {
        background-color: #0e1117;
    }

    .block-container {
        max-width: 1500px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    h1 {
        font-size: 42px !important;
        font-weight: 800 !important;
    }

    h2 {
        margin-top: 35px !important;
    }

    h3 {
        margin-top: 25px !important;
    }

    [data-testid="stMetric"] {
        background-color: #161b22;
        border: 1px solid #30363d;
        padding: 18px;
        border-radius: 12px;
    }

    [data-testid="stMetricValue"] {
        font-size: 26px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==========================================================
# CARGA DE DATOS
# ==========================================================

@st.cache_data
def cargar():

    df = cargar_datos()
    mapa = cargar_mapa()

    return df, mapa


df, mapa = cargar()


# ==========================================================
# CABECERA
# ==========================================================

st.title(
    "🚦 Madrid Traffic Intelligence"
)

st.markdown(
    """
    ### ¿Dónde, cuándo y qué tipo de infracciones se concentran en Madrid?

    Un análisis interactivo de las sanciones de tráfico para entender
    cómo se distribuyen a lo largo del tiempo, qué infracciones son
    más habituales y qué impacto económico tienen.
    """
)

st.caption(
    "4,1 M de sanciones analizadas a partir de "
    "19 archivos mensuales disponibles entre 2024 y 2026."
)


# ==========================================================
# FILTROS
# ==========================================================

st.sidebar.title("🎛️ Filtros")

st.sidebar.caption(
    "Ajusta los filtros para explorar los datos según el periodo "
    "o el tipo de sanción que te interese."
)


anios = sorted(
    df["ANIO"].dropna().unique()
)

anios_seleccionados = st.sidebar.multiselect(
    "Año",
    anios,
    default=anios
)


calificaciones = sorted(
    df["CALIFICACION"].dropna().unique()
)

calificaciones_seleccionadas = st.sidebar.multiselect(
    "Calificación",
    calificaciones,
    default=calificaciones
)


importe_min = float(
    df["IMP_BOL"].min()
)

importe_max = float(
    df["IMP_BOL"].max()
)


importe_seleccionado = st.sidebar.slider(
    "Importe de la multa (€)",
    min_value=importe_min,
    max_value=importe_max,
    value=(
        importe_min,
        importe_max
    ),
    step=10.0
)


df_filtrado = df[
    df["ANIO"].isin(
        anios_seleccionados
    )
    &
    df["CALIFICACION"].isin(
        calificaciones_seleccionadas
    )
    &
    df["IMP_BOL"].between(
        importe_seleccionado[0],
        importe_seleccionado[1]
    )
].copy()


# ==========================================================
# KPIs
# ==========================================================

kpis = calcular_kpis(
    df_filtrado
)


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "🚨 Sanciones",
        f"{kpis['total_multas']:,}"
    )


with col2:

    st.metric(
        "💰 Importe total de las sanciones",
        f"{kpis['importe_total']:,.0f} €"
    )


with col3:

    st.metric(
        "💶 Multa media",
        f"{kpis['importe_medio']:.2f} €"
    )


with col4:

    st.metric(
        "⚠️ Con pérdida de puntos",
        f"{kpis['porcentaje_puntos']:.2f}%"
    )


st.divider()


# ==========================================================
# EVOLUCIÓN TEMPORAL
# ==========================================================

st.header(
    "📈 Evolución de las sanciones"
)

st.markdown(
    """
    ¿Cómo ha cambiado el volumen de sanciones y cuánto ha variado
    el importe medio de las multas a lo largo del periodo analizado?
    """
)


mensual = evolucion_mensual(
    df_filtrado
)


col1, col2 = st.columns(2)


with col1:

    st.plotly_chart(
        grafico_evolucion(mensual),
        use_container_width=True
    )


with col2:

    st.plotly_chart(
        grafico_multa_media(mensual),
        use_container_width=True
    )


# ==========================================================
# RANKING DE INFRACCIONES
# ==========================================================

st.header(
    "🚨 Principales infracciones"
)

st.markdown(
    """
    Estas son las infracciones que aparecen con mayor frecuencia
    en los datos seleccionados, junto con su peso e impacto económico.
    """
)


resumen = resumen_infracciones(
    df_filtrado
)


st.dataframe(
    resumen,
    use_container_width=True,
    hide_index=True,
    column_config={

        "Infracción":
            st.column_config.TextColumn(
                "Tipo de infracción",
                width="large"
            ),

        "N.º sanciones":
            st.column_config.NumberColumn(
                "N.º sanciones",
                format="%d"
            ),

        "% del total":
            st.column_config.NumberColumn(
                "Peso sobre el total",
                format="%.1f %%"
            ),

        "Impacto económico":
            st.column_config.NumberColumn(
                "Impacto económico",
                format="%,.0f €"
            ),

        "Multa media":
            st.column_config.NumberColumn(
                "Multa media",
                format="%.2f €"
            )
    }
)


# ==========================================================
# PATRONES HORARIOS
# ==========================================================

st.header(
    "⏱️ ¿Cuándo se concentran las sanciones?"
)

st.markdown(
    """
    Distribución de las sanciones por hora para detectar
    las franjas del día con mayor actividad.
    """
)


horas = multas_por_hora(
    df_filtrado
)


st.plotly_chart(
    grafico_horas(horas),
    use_container_width=True
)


# ==========================================================
# COMPARATIVA ANUAL
# ==========================================================

st.header(
    "📊 Sanciones por año"
)

st.markdown(
    """
    Una visión rápida de cómo se reparte el volumen de sanciones
    entre los diferentes años disponibles.
    """
)


anual = comparativa_anual(
    df_filtrado
)


st.plotly_chart(
    grafico_anual(anual),
    use_container_width=True
)


# ==========================================================
# HOTSPOTS
# ==========================================================

st.header(
    "🔥 ¿Dónde se concentran las sanciones?"
)

st.markdown(
    """
    Mapa de las zonas con mayor concentración de sanciones.
    El tamaño de los puntos ayuda a identificar rápidamente
    los principales focos de actividad.
    """
)


st.plotly_chart(
    crear_hotspots(mapa),
    use_container_width=True
)


st.caption(
    "El mapa utiliza una agregación geográfica independiente "
    "de 420 celdas espaciales."
)


# ==========================================================
# PIE
# ==========================================================

st.divider()

st.caption(
    "Madrid Traffic Intelligence · "
    "Python · Pandas · Plotly · Streamlit · SQLite"
)