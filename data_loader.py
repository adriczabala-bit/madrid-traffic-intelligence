import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def cargar_datos():
    archivo = BASE_DIR / "multas_madrid_powerbi_comprimido.parquet"

    columnas = [
        "FECHA",
        "ANIO",
        "MES",
        "HORA",
        "CALIFICACION",
        "IMP_BOL",
        "PUNTOS",
        "HECHO-BOL"
    ]

    df = pd.read_parquet(
        archivo,
        columns=columnas
    )

    df["FECHA"] = pd.to_datetime(
        df["FECHA"],
        errors="coerce"
    )

    df["ANIO"] = pd.to_numeric(
        df["ANIO"],
        errors="coerce"
    ).astype("int16")

    df["MES"] = pd.to_numeric(
        df["MES"],
        errors="coerce"
    ).astype("int8")

    df["IMP_BOL"] = pd.to_numeric(
        df["IMP_BOL"],
        errors="coerce"
    ).astype("int16")

    df["PUNTOS"] = pd.to_numeric(
        df["PUNTOS"],
        errors="coerce"
    ).fillna(0).astype("int8")

    df["CALIFICACION"] = (
        df["CALIFICACION"]
        .astype("category")
    )

    df["HECHO-BOL"] = (
        df["HECHO-BOL"]
        .astype("category")
    )

    if "HORA" in df.columns:
        df["HORA_NUM"] = pd.to_numeric(
            df["HORA"]
            .astype(str)
            .str.extract(r"(\d{1,2})")[0],
            errors="coerce"
        ).astype("Int8")

    df["CON_PUNTOS"] = (
        df["PUNTOS"] > 0
    ).astype("int8")

    return df


def cargar_mapa():
    archivo = BASE_DIR / "multas_madrid_final.xlsx"

    mapa = pd.read_excel(archivo)

    columnas_numericas = [
        "latitud_grid",
        "longitud_grid",
        "multas",
        "importe_total",
        "importe_medio",
        "multas_con_puntos"
    ]

    for col in columnas_numericas:
        if col in mapa.columns:
            mapa[col] = pd.to_numeric(
                mapa[col],
                errors="coerce"
            )

    return mapa
