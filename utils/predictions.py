# utils/predictions.py
import numpy as np
import pandas as pd
from config import MAX_CABINAS

def predecir(modelo_rf, hora, dia_semana):
    """Predice usando el modelo real o simulación"""
    if modelo_rf is not None:
        try:
            es_fin_semana = 1 if dia_semana in [5, 6] else 0
            X = pd.DataFrame([[hora, dia_semana, es_fin_semana]],
                           columns=['hora_inicio', 'dia_semana', 'es_fin_semana'])
            pred = modelo_rf.predict(X)[0]
            return int(round(max(0, min(MAX_CABINAS, pred))))
        except:
            pass  # caerá en simulación

    # Simulación realista (cuando no hay modelo)
    np.random.seed()
    if dia_semana in [5, 6]:  # fin de semana
        base = [8,11,15,19,22,24,25,24,22,19,16,13]
    else:
        base = [5,7,10,13,16,19,21,20,17,14,11,8]
    
    idx = hora - 10
    if 0 <= idx < len(base):
        valor = base[idx] + np.random.normal(0, 2.5)
    else:
        valor = 12
    return int(round(max(0, min(MAX_CABINAS, valor))))

def obtener_cluster(cabinas):
    if cabinas < 10:
        return 0
    elif cabinas < 18:
        return 1
    else:
        return 2