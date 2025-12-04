# utils/plots.py
import matplotlib.pyplot as plt
import streamlit as st
from config import HORA_INICIO, HORA_FIN, MAX_CABINAS, CLUSTERS
from utils.predictions import obtener_cluster

def graficar_demanda_completa(dia_semana, hora_actual, cabinas_actual, dia_nombre, modelo_rf=None):
    fig = plt.figure(figsize=(19, 8))
    fig.patch.set_facecolor('#0e1117')
    
    # 12 horas fijas
    horas = [10,11,12,13,14,15,16,17,18,19,20,21]
    
    # Tus datos históricos reales
    if dia_semana in [5, 6]:
        demanda_hist = [8, 10, 15, 18, 16, 20, 22, 23, 21, 18, 15, 12]
    else:
        demanda_hist = [5, 6, 8, 12, 14, 18, 20, 19, 16, 14, 10, 7]

    gs = fig.add_gridspec(1, 2, width_ratios=[3, 1], wspace=0.35)  # ← Más separación entre gráficos
    
    # === GRÁFICO 1: Demanda durante el día ===
    ax1 = fig.add_subplot(gs[0])
    ax1.plot(horas, demanda_hist, 'o-', color='#00ffff', linewidth=5, markersize=10,
             markerfacecolor='#00ffff', markeredgecolor='black', markeredgewidth=2,
             label='Promedio histórico', zorder=5)
    
    # Punto de predicción MÁS ELEGANTE (menos gigante + borde pro)
    cluster_id = obtener_cluster(cabinas_actual)
    color_pred = CLUSTERS[cluster_id]["color"]
    ax1.scatter(hora_actual, cabinas_actual, color=color_pred, s=500,
                edgecolor='white', linewidth=6, zorder=10,
                label=f'Predicción {hora_actual}:00', marker='o')
    # Borde extra para que resalte más
    ax1.scatter(hora_actual, cabinas_actual, color='white', s=700, facecolors='none',
                edgecolor='white', linewidth=3, zorder=9, alpha=0.7)

    # Zonas de demanda
    ax1.axhspan(18, 25, alpha=0.3, color='#ff0000', zorder=1)
    ax1.axhspan(10, 18, alpha=0.2, color='#ffa500', zorder=1)
    ax1.axhspan(0, 10, alpha=0.15, color='#00ff00', zorder=1)
    ax1.axhline(25, color='#ff0066', linestyle='--', linewidth=4, label='Capacidad máxima')

    ax1.set_facecolor('#0e1117')
    ax1.grid(True, alpha=0.3, color='#333', linewidth=1)
    ax1.set_title("Demanda durante el día", color='#00ffff', fontsize=22, fontweight='bold', pad=30)
    ax1.set_xlabel("Hora", color='white', fontsize=14)
    ax1.set_ylabel("Cabinas ocupadas", color='white', fontsize=14)
    ax1.legend(facecolor='#1a1c23', labelcolor='white', fontsize=12, loc='upper left', framealpha=0.9)
    ax1.tick_params(colors='white', labelsize=12)
    ax1.set_ylim(0, 30)
    ax1.set_xticks(horas)
    ax1.set_yticks(range(0, 31, 5))

    # === GRÁFICO 2: Distribución de clusters (con día) ===
    ax2 = fig.add_subplot(gs[1])
    conteo = [0, 0, 0]
    for val in demanda_hist:
        conteo[obtener_cluster(val)] += 1

    bars = ax2.bar(["Baja", "Media", "Alta"], conteo,
                   color=['#00ff00', '#ffa500', '#ff0000'],
                   edgecolor='white', linewidth=3, alpha=0.9)

    # Resaltar cluster actual
    bars[cluster_id].set_edgecolor('#00ffff')
    bars[cluster_id].set_linewidth(7)

    ax2.set_facecolor('#0e1117')
    ax2.set_title(f"Distribución de clusters\n({dia_nombre})", color='#00ffff', fontsize=16, fontweight='bold', pad=20)
    ax2.tick_params(colors='white', labelsize=12)
    ax2.set_ylim(0, 12)

    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.3,
                f'{int(height)}h', ha='center', va='bottom', color='white',
                fontweight='bold', fontsize=16)

    plt.suptitle("", color='white')  # evita que el título se superponga
    return fig