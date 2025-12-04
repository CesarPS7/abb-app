# utils/models.py
import pickle
import json
import streamlit as st

@st.cache_resource
def cargar_modelos():
    try:
        with open('modelo_random_forest.pkl', 'rb') as f:
            modelo_rf = pickle.load(f)
        with open('modelo_kmeans.pkl', 'rb') as f:
            modelo_kmeans = pickle.load(f)
        with open('scaler_kmeans.pkl', 'rb') as f:
            scaler_kmeans = pickle.load(f)
        with open('info_random_forest.json', 'r') as f:
            info_rf = json.load(f)
        
        #st.sidebar.success("✅ Modelos IA reales cargados")
        return modelo_kmeans, scaler_kmeans, modelo_rf, info_rf
    except Exception as e:
        st.sidebar.warning("⚠️ Usando simulación (falta algún modelo)")
        return None, None, None, None