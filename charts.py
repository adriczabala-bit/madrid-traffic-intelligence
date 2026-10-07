import plotly.express as px


# ==========================================================
# ESTILO GENERAL
# ==========================================================

def aplicar_estilo(fig, altura=450):

    fig.update_layout(
        template="plotly_dark",
        height=altura,
        margin=dict(
            l=20,
            r=20,
            t=65,
            b=45
        ),
        font=dict(
            family="Arial"
        ),
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    return fig


# ==========================================================
# EVOLUCIÓN DE SANCIONES
# ==========================================================

def grafico_evolucion(mensual):

    fig = px.line(
        mensual,
        x="FECHA",
        y="multas",
        markers=True,
        title="Evolución del número de sanciones"
    )

    fig.update_traces(
        line=dict(width=3),
        marker=dict(size=7)
    )

    fig.update_layout(
        xaxis_title="",
        yaxis_title="N.º de sanciones",
        hoverlabel=dict(
            bgcolor="#161b22"
        )
    )

    fig.update_yaxes(
        separatethousands=True
    )

    return aplicar_estilo(fig)


# ==========================================================
# MULTA MEDIA
# ==========================================================

def grafico_multa_media(mensual):

    fig = px.line(
        mensual,
        x="FECHA",
        y="importe_medio",
        markers=True,
        title="Evolución de la multa media"
    )

    fig.update_traces(
        line=dict(width=3),
        marker=dict(size=7)
    )

    fig.update_layout(
        xaxis_title="",
        yaxis_title="Importe medio (€)",
        hoverlabel=dict(
            bgcolor="#161b22"
        )
    )

    fig.update_yaxes(
        tickprefix="€ ",
        separatethousands=True
    )

    return aplicar_estilo(fig)


# ==========================================================
# PRINCIPALES INFRACCIONES
# ==========================================================

def grafico_infracciones(data):

    fig = px.bar(
        data,
        x=data.values,
        y=data.index,
        orientation="h",
        title="Infracciones más frecuentes",
        labels={
            "x": "Número de sanciones",
            "y": ""
        }
    )

    fig.update_traces(
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Sanciones: %{x:,.0f}"
            "<extra></extra>"
        )
    )

    fig.update_layout(
        xaxis_title="N.º de sanciones",
        yaxis_title="",
        showlegend=False
    )

    return aplicar_estilo(
        fig,
        520
    )


# ==========================================================
# IMPACTO ECONÓMICO POR INFRACCIÓN
# ==========================================================

def grafico_impacto(data):

    fig = px.bar(
        data,
        x="importe_total",
        y=data.index,
        orientation="h",
        title="Infracciones con mayor impacto económico",
        labels={
            "x": "Impacto económico (€)",
            "y": ""
        }
    )

    fig.update_traces(
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Impacto: €%{x:,.0f}"
            "<extra></extra>"
        )
    )

    fig.update_layout(
        xaxis_title="Impacto económico (€)",
        yaxis_title="",
        showlegend=False
    )

    fig.update_xaxes(
        tickprefix="€ ",
        separatethousands=True
    )

    return aplicar_estilo(
        fig,
        520
    )


# ==========================================================
# PATRONES HORARIOS
# ==========================================================

def grafico_horas(data):

    fig = px.line(
        data,
        x="HORA_NUM",
        y="multas",
        markers=True,
        title="Concentración de sanciones por hora"
    )

    fig.update_traces(
        line=dict(width=3),
        marker=dict(size=7)
    )

    fig.update_layout(
        xaxis_title="Hora del día",
        yaxis_title="N.º de sanciones",
        xaxis=dict(
            dtick=1
        )
    )

    return aplicar_estilo(fig)


# ==========================================================
# COMPARATIVA ANUAL
# ==========================================================

def grafico_anual(data):

    fig = px.bar(
        data,
        x="ANIO",
        y="multas",
        text="multas",
        title="Volumen de sanciones por año"
    )

    fig.update_traces(
        texttemplate="%{text:,.0f}",
        textposition="outside"
    )

    fig.update_layout(
        xaxis_title="Año",
        yaxis_title="N.º de sanciones",
        showlegend=False
    )

    fig.update_yaxes(
        separatethousands=True
    )

    return aplicar_estilo(
        fig,
        430
    )