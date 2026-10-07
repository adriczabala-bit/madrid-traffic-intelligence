import pandas as pd
import re


def calcular_kpis(df):

    total_multas = len(df)

    importe_total = df["IMP_BOL"].sum()

    importe_medio = df["IMP_BOL"].mean()

    multas_puntos = df["CON_PUNTOS"].sum()

    porcentaje_puntos = (
        multas_puntos / total_multas * 100
        if total_multas > 0
        else 0
    )

    return {
        "total_multas": total_multas,
        "importe_total": importe_total,
        "importe_medio": importe_medio,
        "multas_puntos": multas_puntos,
        "porcentaje_puntos": porcentaje_puntos
    }


def evolucion_mensual(df):

    return (
        df.groupby("FECHA")
        .agg(
            multas=("IMP_BOL", "size"),
            importe=("IMP_BOL", "sum"),
            importe_medio=("IMP_BOL", "mean"),
            multas_puntos=("CON_PUNTOS", "sum")
        )
        .reset_index()
        .sort_values("FECHA")
    )


def nombre_infraccion(texto, max_chars=45):

    texto = str(texto)

    texto = re.sub(
        r"\s+",
        " ",
        texto
    ).strip()

    if len(texto) > max_chars:
        texto = (
            texto[:max_chars - 3].rstrip()
            + "..."
        )

    return texto


def top_infracciones(df, n=10):

    datos = (
        df["HECHO-BOL"]
        .value_counts()
        .head(n)
        .sort_values()
    )

    datos.index = [
        nombre_infraccion(x)
        for x in datos.index
    ]

    return datos


def impacto_infracciones(df, n=10):

    datos = (
        df.groupby("HECHO-BOL")
        .agg(
            multas=("IMP_BOL", "size"),
            importe_total=("IMP_BOL", "sum"),
            importe_medio=("IMP_BOL", "mean")
        )
        .sort_values(
            "importe_total",
            ascending=False
        )
        .head(n)
        .sort_values(
            "importe_total"
        )
    )

    datos.index = [
        nombre_infraccion(x)
        for x in datos.index
    ]

    return datos


def multas_por_hora(df):

    return (
        df.dropna(
            subset=["HORA_NUM"]
        )
        .groupby("HORA_NUM")
        .size()
        .reset_index(
            name="multas"
        )
        .sort_values(
            "HORA_NUM"
        )
    )


def comparativa_anual(df):

    return (
        df.groupby("ANIO")
        .agg(
            multas=("IMP_BOL", "size"),
            importe_total=("IMP_BOL", "sum"),
            importe_medio=("IMP_BOL", "mean"),
            multas_puntos=("CON_PUNTOS", "sum")
        )
        .reset_index()
    )


def multa_media_mensual(df):

    datos = (
        df.groupby("FECHA")
        .agg(
            multa_media=("IMP_BOL", "mean"),
            multas=("IMP_BOL", "size")
        )
        .reset_index()
        .sort_values("FECHA")
    )

    return datos


def resumen_infracciones(df, n=8):

    datos = (
        df.groupby("HECHO-BOL")
        .agg(
            multas=("IMP_BOL", "size"),
            importe_total=("IMP_BOL", "sum"),
            multa_media=("IMP_BOL", "mean")
        )
        .sort_values(
            "multas",
            ascending=False
        )
        .head(n)
        .reset_index()
    )

    total_multas = len(df)

    datos["peso"] = (
        datos["multas"]
        / total_multas
        * 100
        if total_multas > 0
        else 0
    )

    datos["Infracción"] = datos[
        "HECHO-BOL"
    ].apply(
        nombre_infraccion
    )

    resultado = datos[
        [
            "Infracción",
            "multas",
            "peso",
            "importe_total",
            "multa_media"
        ]
    ].copy()

    resultado.columns = [
        "Infracción",
        "N.º sanciones",
        "% del total",
        "Impacto económico",
        "Multa media"
    ]

    return resultado