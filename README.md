# 🚦 Madrid Traffic Intelligence

Proyecto de análisis de sanciones de tráfico en Madrid desarrollado con Python, Pandas, Plotly y Streamlit.

La idea surgió de una pregunta bastante sencilla:

**¿Dónde, cuándo y qué tipo de infracciones se concentran en Madrid?**

A partir de más de **4,1 millones de sanciones**, construí una aplicación interactiva para explorar los datos y encontrar patrones que no son tan fáciles de ver trabajando directamente con los archivos originales.

## 🔎 ¿Qué he analizado?

La aplicación permite explorar:

* Cómo evolucionan las sanciones a lo largo del tiempo
* Qué infracciones aparecen con mayor frecuencia
* En qué horas se concentran más sanciones
* Cómo cambia el volumen de sanciones entre años
* Qué impacto económico tienen las diferentes infracciones
* Qué porcentaje de sanciones implica pérdida de puntos
* En qué zonas se concentra una mayor cantidad de sanciones

También incorporé filtros para poder analizar los datos por **año, calificación e importe de la multa**.

## 📊 Los datos

El dataset principal reúne **19 archivos mensuales disponibles entre enero de 2024 y marzo de 2026**, con un total de **4.105.718 registros**.

Antes de utilizarlos tuve que preparar y limpiar los datos para poder trabajar con ellos de forma consistente.

Para el análisis geográfico utilicé además una agregación independiente de **420 celdas espaciales**, que es la que alimenta el mapa de la aplicación.

## 🧠 ¿Qué hay detrás del proyecto?

Más allá de las visualizaciones, la parte que más me interesaba era convertir unos archivos de datos bastante grandes en algo que pudiera utilizarse para responder preguntas concretas.

Por eso separé el proyecto en diferentes partes:

* `data_loader.py` → carga y preparación de los datos
* `analysis.py` → cálculos, KPIs y análisis
* `charts.py` → visualizaciones
* `map.py` → análisis geográfico
* `app.py` → aplicación interactiva

Además, el dataset principal está almacenado en **Parquet** para reducir su tamaño y hacer más eficiente su lectura.

## 🛠️ Herramientas utilizadas

**Python · Pandas · Plotly · Streamlit · Parquet · GitHub**

## 🚀 Aplicación

He desplegado el proyecto en Streamlit para que pueda consultarse directamente desde el navegador.

👉 **[Abrir Madrid Traffic Intelligence](https://madrid-traffic-intelligence.streamlit.app/)**


```text
madrid-traffic-intelligence/
│
├── app.py
├── analysis.py
├── charts.py
├── data_loader.py
├── map.py
├── requirements.txt
│
├── multas_madrid_powerbi_comprimido.parquet
└── multas_madrid_final.xlsx
```

## 📌 Una aclaración sobre los datos

El importe total mostrado corresponde al **importe agregado de las sanciones registradas**, no a la recaudación efectiva.

El mapa utiliza una agregación geográfica independiente del dataset principal, por lo que sus cifras no deben compararse directamente con los 4,1 millones de registros.

---

Un proyecto en el que he intentado combinar **análisis de datos, visualización y una aplicación real**, en lugar de quedarme únicamente en el notebook.

**Madrid Traffic Intelligence · Python · Pandas · Plotly · Streamlit**
