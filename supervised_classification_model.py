import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

df = pd.read_csv("trip_records_supervised.csv")

features = [
    "dia_semana",
    "origen",
    "destino",
    "ruta_principal",
    "tiempo_estimado_min",
    "transbordos",
    "afluencia_origen",
    "afluencia_destino",
    "ocupacion_promedio",
    "clima",
    "incidente",
    "tipo_usuario",
]

target = "retraso_alto"

X = df[features]
y = df[target]

numeric_features = [
    "tiempo_estimado_min",
    "transbordos",
    "afluencia_origen",
    "afluencia_destino",
    "ocupacion_promedio",
    "incidente",
]

categorical_features = [
    "dia_semana",
    "origen",
    "destino",
    "ruta_principal",
    "clima",
    "tipo_usuario",
]

preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), numeric_features),
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
    ]
)

model = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("classifier", RandomForestClassifier(
        n_estimators=150,
        random_state=42
    ))
])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

model.fit(X_train, y_train)

preds = model.predict(X_test)

acc = accuracy_score(y_test, preds)
print(f"Accuracy: {acc:.4f}")
print("\nClassification report:")
print(classification_report(y_test, preds))
print("\nConfusion matrix:")
print(confusion_matrix(y_test, preds))

joblib.dump(model, "supervised_classification_model.joblib")
print("Modelo guardado en supervised_classification_model.joblib")