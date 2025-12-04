# 🎮 ABADDON LAN CENTER — Predictive Analytics App

Aplicación inteligente desarrollada en **Python + Streamlit** para analizar el comportamiento de un Lan Center y **predecir la demanda de cabinas** según día y hora.  
Usa modelos de **Machine Learning (Random Forest + KMeans)** entrenados con datos reales de un mes del negocio.

---

## 🚀 Características principales

### ✔ Predicción de demanda por hora

El modelo estima cuántas cabinas estarán ocupadas de acuerdo al **día de la semana**, **hora**, y patrones históricos.

### ✔ Identificación de horas pico

El sistema encuentra automáticamente los horarios donde tu local estará más lleno.

### ✔ Segmentación de clientes

Un modelo K-Means agrupa clientes según su comportamiento típico (opcional si agregas id_cliente).

### ✔ Dashboard interactivo

UI limpia creada con **Streamlit**, mostrando:

- Cabinas ocupadas
- Cabinas disponibles
- Distribuciones, gráficas y tendencias

---

## 🧠 Tecnologías utilizadas

- **Python 3.10+**
- **Streamlit**
- **Pandas**
- **Scikit-learn**
- **Matplotlib / Seaborn**
- **Pickle** (para serializar modelos)
- **JSON** (para configuración del Random Forest)
- **NumPy**

---

## 📁 Estructura del proyecto

ABADDON-APP/
│── assets/
│ └── logo_abb.png
│
│── utils/
│ ├── models.py
│ ├── predictions.py
│ └── plots.py
│
│── app.py
│── features_kmeans.pkl
│── modelo_kmeans.pkl
│── modelo_random_forest.pkl
│── scaler_kmeans.pkl
│── info_random_forest.json
│── requirements.txt
│── README.md

## 🔧 Instalación

Clona el proyecto:

```bash
git clone https://github.com/CesarPS7/abaddon-app.git
cd abaddon-app

Crea un entorno virtual (opcional, pero recomendado):

python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

Instala dependencias:

pip install -r requirements.txt

Ejecutar la aplicación localmente

streamlit run app.py

Luego abre en tu navegador:

http://localhost:8501
```
