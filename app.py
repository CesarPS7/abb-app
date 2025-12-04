# app.py
import streamlit as st
from PIL import Image
import os
from config import *
from utils.models import cargar_modelos
from utils.predictions import predecir, obtener_cluster
from utils.plots import graficar_demanda_completa

# ==================================== CONFIGURACIÓN DE PÁGINA ====================================
st.set_page_config(
    page_title=f"{NOMBRE_LOCAL} - Predicción IA",
    page_icon="gamepad",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo gamer oscuro mejorado con transiciones suaves y sombras
st.markdown("""
<style>
    .reportview-container { background: #0e1117; color: #fafafa; }
    .sidebar .sidebar-content { background: #1a1c23; box-shadow: 0 4px 8px rgba(0,0,0,0.5); }
    h1, h2, h3, h4 { color: #00ffff; font-family: 'Orbitron', sans-serif; text-shadow: 0 0 5px #00ffff; }
    .stButton>button { background: linear-gradient(45deg, #ff0066, #ff00cc); border: none; border-radius: 20px; color: white; padding: 10px 20px; font-weight: bold; transition: all 0.3s ease; }
    .stButton>button:hover { transform: scale(1.05); box-shadow: 0 0 10px #ff0066; }
    .metric { background: rgba(30, 30, 50, 0.8); border-radius: 10px; padding: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.3); }
    .metric-value { font-size: 2.5rem !important; color: #00ffff; text-shadow: 0 0 3px #00ffff; }
    .stExpander { background: #1a1c23; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.3); }
</style>
""", unsafe_allow_html=True)

# Estrellas solo la primera vez
if not st.session_state.get('first_load', False):
    st.snow()
    st.session_state.first_load = True

# ==================================== CARGA DE MODELOS ====================================
modelo_kmeans, scaler_kmeans, modelo_rf, info_rf = cargar_modelos()

# ==================================== SIDEBAR ====================================
# Logo
logo_path = "assets/logo_abb.png"
if os.path.exists(logo_path):
    logo = Image.open(logo_path)
    st.sidebar.image(logo, use_container_width=True)
else:
    st.sidebar.error("logo_abb.png no encontrado en /assets")

st.sidebar.markdown(f"# {NOMBRE_LOCAL}")
st.sidebar.markdown("**Sistema Predictivo con Inteligencia Artificial**")

# --- SELECCIÓN DE FECHA Y HORA ---
st.sidebar.markdown("---")
st.sidebar.markdown("## Selecciona fecha y hora para predicción")

dia_nombre = st.sidebar.selectbox("Día de la semana", list(DIAS_MAP.keys()))
dia_semana = DIAS_MAP[dia_nombre]

hora = st.sidebar.slider("Hora del día", HORA_INICIO, HORA_FIN, 17, step=1)

if st.sidebar.button("Predecir Demanda", type="primary", use_container_width=True):
    st.session_state.prediccion_realizada = True
    st.session_state.hora = hora
    st.session_state.dia_semana = dia_semana
    st.session_state.dia_nombre = dia_nombre

# --- ESTADO DE MODELOS IA ---
st.sidebar.markdown("---")
st.sidebar.markdown("## Estado de Modelos IA")

if modelo_rf is not None:
    st.sidebar.success("✅ Modelos IA reales cargados")

    # Random Forest
    n_trees = info_rf.get('n_estimators', 300)
    r2 = info_rf.get('r2', 0.85) * 100
    mae = info_rf.get('mae', 2.5)

    # K-Means usando info_rf 
    k_clusters = info_rf.get('mejor_k', 3)
    features_kmeans = ", ".join(info_rf.get('features_kmeans', [
        'venta_total', 'venta_promedio', 'duracion_promedio', 'cantidad_ventas'
    ]))

    st.sidebar.markdown(f"""
    **🌲 Random Forest**
    - 🎯 Árboles: **{n_trees}**
    - 📊 Precisión (R²)≈ **{r2:.1f}%**
    - 📈 Error (MAE)≈ **{mae:.1f}** cabinas

    **🔍 K-Means Clustering**
    - 🎯 Clusters: **{k_clusters}**
    - 📊 Características: `{features_kmeans}`
    """)

else:
    st.sidebar.warning("⚠️ Usando simulación (modelos no encontrados)")
    st.sidebar.info("Sube tus archivos .pkl y .json en la carpeta principal")

# ==================================== CONTENIDO PRINCIPAL ====================================
col1, col2 = st.columns([1, 4])
with col1:
    if os.path.exists(logo_path):
        st.image(logo, use_container_width=True)
with col2:
    st.markdown(f"# {NOMBRE_LOCAL}")
    st.markdown("### Sistema de Predicción de Demanda con Inteligencia Artificial")

# ==================================== PREDICCIÓN ====================================
if st.session_state.get('prediccion_realizada', False):
    hora = st.session_state.hora
    dia_semana = st.session_state.dia_semana
    dia_nombre = st.session_state.dia_nombre
    
    with st.spinner("Consultando los modelos de IA..."):
        cabinas_pred = predecir(modelo_rf, hora, dia_semana)
        cluster_id = obtener_cluster(cabinas_pred)
        cluster = CLUSTERS[cluster_id]
    
    ocupacion = (cabinas_pred / MAX_CABINAS) * 100
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Cabinas Ocupadas", f"≈ {cabinas_pred:.2f}")
    with col2:
        st.metric("Disponibles", f"≈ {MAX_CABINAS - cabinas_pred:.2f}")
    with col3:
        st.metric("Ocupación", f"≈ {ocupacion:.1f}%")
    with col4:
        st.metric("Ingreso estimado/hora", f" ≈ S/.{cabinas_pred * 5:,}")

    st.markdown(f"## {cluster['emoji']} {cluster['nombre']} a las {hora}:00")
    st.markdown(f"**{dia_nombre}** • {cluster['rango']}")

    fig = graficar_demanda_completa(dia_semana, hora, cabinas_pred, dia_nombre, modelo_rf)
    st.pyplot(fig, use_container_width=True)

    with st.expander("Análisis detallado y recomendaciones"):
        if cluster_id == 0:
            recs = ["Mantenimiento profundo", "Promociones agresivas", "Personal mínimo"]
        elif cluster_id == 1:
            recs = ["Operación normal", "Precios estándar", "Stock completo"]
        else:
            recs = ["¡Estamos a full!", "Stock con reservas necesarias", "Todo el personal"]
        
        st.write(f"### Recomendaciones para {cluster['emoji']} {cluster['nombre']}")
        for r in recs:
            st.write(f"• {r}")

else:
    st.info("""
    Antes de iniciar, selecciona un **día de la semana** y una **hora específica** desde el panel lateral.  
    Esto le permitirá al sistema analizar patrones históricos del lan center y estimar cuántas cabinas estarían ocupadas en ese momento.

    Una vez elijas ambos valores, presiona **Predecir Demanda** para generar:

    • La cantidad estimada de cabinas ocupadas  
    • Las cabinas disponibles  
    • El porcentaje de ocupación  
    • El ingreso aproximado por hora  
    • El tipo de escenario (baja, media o alta demanda) y recomendaciones operativas  
    ⬅️  Usa el panel de la izquierda para comenzar.
    """)
        

    # Sin balloons

# ==================================== FOOTER ====================================
st.markdown("---")
st.markdown(
    """
    <p style="text-align: center; color: #666; margin: 20px 0;">
    Nota: Estos modelos fueron entrenados con datos de 1 mes del lan center. Para obtener patrones más exactos y predicciones específicas para días particulares, se recomienda entrenar con datos históricos de varios meses que incluyan variaciones estacionales.
    </br>Prototipo de IA - Abaddon Lan Center | Modelos: Random Forest + K-Means | Despliegue: Streamlit Cloud - 2025
    </p>
    """,
    unsafe_allow_html=True
)