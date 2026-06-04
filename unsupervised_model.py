import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score

# 1. Cargar datos
df = pd.read_csv("trip_records.csv")

# 2. Seleccionar variables para clustering
features = [
    "tiempo_estimado_min",
    "tiempo_real_min",
    "transbordos",
    "afluencia_origen",
    "afluencia_destino",
    "ocupacion_promedio",
    "clima",
    "incidente",
    "tipo_usuario",
    "ruta_principal",
    "dia_semana"
]

X = df[features]

# 3. Separar columnas numéricas y categóricas
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

# 4. Preprocesamiento
preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), numeric_features),
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
    ]
)

# 5. Probar un número de clusters
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)

pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("cluster", kmeans)
])

# 6. Entrenar
pipeline.fit(X)

# 7. Obtener etiquetas
labels = pipeline.named_steps["cluster"].labels_
df["cluster"] = labels

# 8. Evaluación rápida
X_transformed = pipeline.named_steps["preprocessor"].transform(X)
score = silhouette_score(X_transformed, labels)
print(f"Silhouette Score: {score:.4f}")

# 9. Reducir dimensionalidad para visualizar
pca = PCA(n_components=2, random_state=42)
X_pca = pca.fit_transform(X_transformed.toarray() if hasattr(X_transformed, "toarray") else X_transformed)

df["pca_1"] = X_pca[:, 0]
df["pca_2"] = X_pca[:, 1]

# 10. Visualización
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x="pca_1", y="pca_2", hue="cluster", palette="Set2")
plt.title("Clustering de viajes de transporte")
plt.xlabel("PCA 1")
plt.ylabel("PCA 2")
plt.tight_layout()
plt.show()

# 11. Resumen por cluster
summary = df.groupby("cluster")[numeric_features].mean()
print("\nResumen numérico por cluster:")
print(summary)

print("\nConteo por cluster:")
print(df["cluster"].value_counts())

# 12. Guardar resultados
df.to_csv("trip_records_clustered.csv", index=False)
print("\nArchivo generado: trip_records_clustered.csv")