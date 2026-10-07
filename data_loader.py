import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def cargar_datos():
    archivo = BASE_DIR / "multas_madrid_powerbi_comprimido.parquet"
    df = pd.read_parquet(archivo)

    for col in ["ANIO", "MES", "IMP_BOL", "PUNTOS"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df["FECHA"] = pd.to_datetime(df["FECHA"], errors="coerce")

    columnas_texto = [
        "CALIFICACION",
        "LUGAR",
        "DESCUENTO",
        "DENUNCIANTE",
        "HECHO-BOL"
    ]

    for col in columnas_texto:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    if "HORA" in df.columns:
        df["HORA_NUM"] = pd.to_numeric(
            df["HORA"].astype(str).str.extract(r"(\d{1,2})")[0],
            errors="coerce"
        )

    df["CON_PUNTOS"] = (df["PUNTOS"] > 0).astype(int)

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
