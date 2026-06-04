import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import IsolationForest

df = pd.read_csv("trip_records.csv")

numeric_features = [
    "tiempo_estimado_min",
    "tiempo_real_min",
    "transbordos",
    "afluencia_origen",
    "afluencia_destino",
    "ocupacion_promedio",
    "incidente"
]

categorical_features = [
    "clima",
    "tipo_usuario",
    "ruta_principal",
    "dia_semana"
]

X = df[numeric_features + categorical_features]

preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), numeric_features),
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
    ]
)

pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("anomaly", IsolationForest(contamination=0.05, random_state=42))
])

pipeline.fit(X)

preds = pipeline.named_steps["anomaly"].predict(
    pipeline.named_steps["preprocessor"].transform(X)
)

df["anomalia"] = preds  # -1 anómalo, 1 normal

print(df["anomalia"].value_counts())

anomalias = df[df["anomalia"] == -1]
print("\nViajes anómalos detectados:")
print(anomalias.head())

df.to_csv("trip_records_anomalies.csv", index=False)
print("\nArchivo generado: trip_records_anomalies.csv")