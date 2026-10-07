import plotly.express as px


def crear_hotspots(mapa):

    datos = mapa.copy()

    fig = px.scatter_map(
        datos,
        lat="latitud_grid",
        lon="longitud_grid",
        size="multas",
        color="multas",
        size_max=42,
        zoom=9.5,
        center={
            "lat": 40.4168,
            "lon": -3.7038
        },
        map_style="open-street-map",
        color_continuous_scale="Turbo",
        hover_data={
            "latitud_grid": ":.4f",
            "longitud_grid": ":.4f",
            "multas": ":,.0f",
            "importe_total": ":,.0f",
            "importe_medio": ":.2f",
            "multas_con_puntos": ":,.0f"
        },
        labels={
            "latitud_grid": "Latitud",
            "longitud_grid": "Longitud",
            "multas": "Sanciones",
            "importe_total": "Impacto económico (€)",
            "importe_medio": "Multa media (€)",
            "multas_con_puntos": "Con pérdida de puntos"
        }
    )

    fig.update_traces(
        marker=dict(
            opacity=0.75
        )
    )

    fig.update_layout(
        height=680,
        margin=dict(
            l=0,
            r=0,
            t=10,
            b=0
        ),
        coloraxis_colorbar=dict(
            title="N.º sanciones"
        )
    )

    return fig