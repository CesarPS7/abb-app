# config.py
NOMBRE_LOCAL = "Abaddon Lan Center"

# Horarios y capacidad
HORA_INICIO = 10
HORA_FIN = 20
MAX_CABINAS = 25

# Mapeo de días
DIAS_MAP = {
    "Lunes": 0, "Martes": 1, "Miércoles": 2,
    "Jueves": 3, "Viernes": 4, "Sábado": 5, "Domingo": 6
}

# Clusters bonitos
CLUSTERS = {
    0: {"nombre": "Baja Demanda", "color": "#00ff00", "rango": "0-9 cabinas", "emoji": "🟢"},
    1: {"nombre": "Media Demanda", "color": "#ffa500", "rango": "10-17 cabinas", "emoji": "🟡"},
    2: {"nombre": "Alta Demanda", "color": "#ff0000", "rango": "18-25 cabinas", "emoji": "🔴"}
}