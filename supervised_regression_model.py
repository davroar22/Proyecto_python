import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

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

target = "tiempo_real_min"

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
    ("regressor", RandomForestRegressor(
        n_estimators=150,
        random_state=42
    ))
])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model.fit(X_train, y_train)

preds = model.predict(X_test)

mae = mean_absolute_error(y_test, preds)
rmse = mean_squared_error(y_test, preds) ** 0.5
r2 = r2_score(y_test, preds)

print(f"MAE: {mae:.2f}")
print(f"RMSE: {rmse:.2f}")
print(f"R2: {r2:.4f}")

joblib.dump(model, "supervised_regression_model.joblib")
print("Modelo guardado en supervised_regression_model.joblib")