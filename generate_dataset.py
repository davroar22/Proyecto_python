import pandas as pd
import random
from datetime import datetime, timedelta

stations = [
    "Portal Sur", "Perdomo", "Madelena", "Sevillana",
    "NQS", "CAD", "Universidad Nacional", "Bosa", "Ricaurte"
]

routes = ["G43", "B23", "C15", "H21"]
climates = ["Soleado", "Nublado", "Lluvia"]
user_types = ["Trabajador", "Estudiante", "Otro"]
days_map = {
    0: "Lunes", 1: "Martes", 2: "Miércoles", 3: "Jueves",
    4: "Viernes", 5: "Sábado", 6: "Domingo"
}

records = []
start_date = datetime(2026, 5, 1)

for trip_id in range(1, 1001):
    fecha = start_date + timedelta(days=random.randint(0, 29))
    hora_real = datetime(2026, 1, 1, random.randint(5, 22), random.randint(0, 59))
    origen = random.choice(stations)
    destino = random.choice([s for s in stations if s != origen])
    ruta = random.choice(routes)

    tiempo_estimado = random.randint(8, 35)
    transbordos = random.choice([0, 0, 0, 1, 1, 2])
    afluencia_origen = random.randint(80, 700)
    afluencia_destino = random.randint(80, 700)
    ocupacion = round(random.uniform(0.3, 1.0), 2)
    clima = random.choice(climates)
    incidente = random.choice([0, 0, 0, 1])
    usuario = random.choice(user_types)

    retraso = 0
    if clima == "Lluvia":
        retraso += random.randint(1, 5)
    if incidente == 1:
        retraso += random.randint(3, 10)
    retraso += int(ocupacion * 3)
    retraso += transbordos * random.randint(1, 4)

    tiempo_real = tiempo_estimado + retraso

    records.append({
        "trip_id": trip_id,
        "fecha": fecha.strftime("%Y-%m-%d"),
        "hora": hora_real.strftime("%H:%M"),
        "dia_semana": days_map[fecha.weekday()],
        "origen": origen,
        "destino": destino,
        "ruta_principal": ruta,
        "tiempo_estimado_min": tiempo_estimado,
        "tiempo_real_min": tiempo_real,
        "transbordos": transbordos,
        "afluencia_origen": afluencia_origen,
        "afluencia_destino": afluencia_destino,
        "ocupacion_promedio": ocupacion,
        "clima": clima,
        "incidente": incidente,
        "tipo_usuario": usuario
    })

df = pd.DataFrame(records)
df.to_csv("trip_records.csv", index=False)
print("Dataset generado: trip_records.csv")