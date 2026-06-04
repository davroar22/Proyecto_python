import pandas as pd
import matplotlib.pyplot as plt

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

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

X_transformed = preprocessor.fit_transform(X)

scores = []
ks = range(2, 8)

for k in ks:
    model = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = model.fit_predict(X_transformed)
    score = silhouette_score(X_transformed, labels)
    scores.append(score)
    print(f"k={k}, silhouette={score:.4f}")

plt.plot(list(ks), scores, marker="o")
plt.title("Selección de número de clusters")
plt.xlabel("Número de clusters (k)")
plt.ylabel("Silhouette score")
plt.grid(True)
plt.show()