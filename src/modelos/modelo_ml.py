import os
import joblib
import numpy as np
import pandas as pd
from sklearn import model_selection
from sklearn.model_selection import train_test_split, KFold
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC, SVR
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ADMISION = os.path.join(BASE_DIR, "data", "processed", "conare_admision_limpio.csv")
MATRICULA = os.path.join(BASE_DIR, "data", "processed", "conare_matricula_limpio.csv")
# Clasificacion: Rango de nota de admision
df = pd.read_csv(ADMISION)
features = [
    "ANO_CONCURSO", "SEXO", "NACIONALIDAD", "RANGO_EDAD",
    "PROVINCIA_RESIDENCIA", "CANTON_RESIDENCIA", "SEDE", "RECINTO",
    "TIPO_COLEGIO", "TIPO_HORARIO_COLEGIO", "TIPO_MODALIDAD_COLEGIO",
    "PROVINCIA_COLEGIO", "CANTON_COLEGIO", "TIPO_PROCESO_ADMISION", "CARRERA"
]
target = "RANGO_NOTA_ADMISION"
# Benchmark con una muestra
df_b = df.sample(n=min(15000, len(df)), random_state=42)
X = df_b[features]
y = df_b[target]
# Division del train y test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
pre = ColumnTransformer([("cat", Pipeline([("imp", SimpleImputer(strategy="most_frequent")),("oh", OneHotEncoder(handle_unknown="ignore"))]), features)])
models = [
    ("LR", LogisticRegression(max_iter=1000)),
    ("LDA", LinearDiscriminantAnalysis()),
    ("KNN", KNeighborsClassifier()),
    ("CART", DecisionTreeClassifier(random_state=42)),
    ("NB", GaussianNB()),
    ("SVM", SVC())
]
# Para este CSV, LR obtuvo el mayor F1 weighted.
lr = Pipeline([
    ("pre", pre),
    ("model", LogisticRegression(C=1, max_iter=1000))])
lr.fit(X_train, y_train)
pred = lr.predict(X_test)
print("CLASIFICACION")
print("Accuracy:", accuracy_score(y_test, pred))
print("Precision:", precision_score(y_test, pred, average="weighted", zero_division=0))
print("Recall:", recall_score(y_test, pred, average="weighted", zero_division=0))
print("F1:", f1_score(y_test, pred, average="weighted", zero_division=0))
# Modelo final con todos los registros.
modelo_clasificacion = Pipeline([
    ("pre", pre),
    ("model", LogisticRegression(C=1, max_iter=1000))])
modelo_clasificacion.fit(df[features], df[target])
joblib.dump(modelo_clasificacion,"ml_clasificacion_nota.joblib")
# Regresion: Cantidad de matriculados por año/universidad/carrera
mat = pd.read_csv(MATRICULA)
keys = ["AÑO", "UNIVERSIDAD", "CARRERA"]
target_r = "MATRICULADOS"
agg = mat.groupby(keys, as_index=False).size().rename(columns={"size": target_r})
extra_cols = [
    "REGION_PLANIFICACION_SEDE", "GAM_SEDE", "GRADO_ACADEMICO",
    "NIVEL_ACADEMICO", "NIVEL_CINE", "AREA_CONOCIMIENTO",
    "DISCIPLINA", "AREA_UNESCO", "DISCIPLINA_UNESCO", "STEM_MICITT"
]
extra = mat[keys + extra_cols]
extra = extra.groupby(keys)[extra_cols].agg(lambda s: s.mode().iloc[0] if len(s.mode()) else "SIN INFO").reset_index()
reg = agg.merge(extra, on=keys, how="left")
features_r = [
    "AÑO", "UNIVERSIDAD", "CARRERA", "REGION_PLANIFICACION_SEDE",
    "GAM_SEDE", "GRADO_ACADEMICO", "NIVEL_ACADEMICO", "NIVEL_CINE",
    "AREA_CONOCIMIENTO", "DISCIPLINA", "AREA_UNESCO",
    "DISCIPLINA_UNESCO", "STEM_MICITT"
]
cat_r = [c for c in features_r if c != "AÑO"]
pre_r = ColumnTransformer([
    ("num", SimpleImputer(strategy="median"), ["AÑO"]),
    ("cat", Pipeline([
        ("imp", SimpleImputer(strategy="most_frequent")),
        ("oh", OneHotEncoder(handle_unknown="ignore"))
    ]), cat_r)
])
Xr = reg[features_r]
yr = reg[target_r]
Xr_train, Xr_test, yr_train, yr_test = train_test_split(Xr, yr, test_size=0.2, random_state=42)
modelo_regresion_test = Pipeline([
    ("pre", pre_r),
    ("model", DecisionTreeRegressor(random_state=42))])
modelo_regresion_test.fit(Xr_train, yr_train)
pred_r = modelo_regresion_test.predict(Xr_test)
print("\nREGRESION")
print("MAE:", mean_absolute_error(yr_test, pred_r))
print("RMSE:", mean_squared_error(yr_test, pred_r) ** 0.5)
print("R2:", r2_score(yr_test, pred_r))
# Modelo final.
modelo_regresion = Pipeline([("pre", pre_r),("model", DecisionTreeRegressor(random_state=42))])
modelo_regresion.fit(reg[features_r], reg[target_r])
joblib.dump(modelo_regresion, "ml_regresion_matriculados.joblib")
reg.to_csv(os.path.join(BASE_DIR, "data", "processed", "matricula_agregada_modelo.csv"),index=False,encoding="utf-8-sig")
print("\nModelos guardados correctamente.")