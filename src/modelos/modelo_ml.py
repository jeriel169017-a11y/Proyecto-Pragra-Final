import os
import joblib
import numpy as np
import pandas as pd
from sklearn import model_selection
from sklearn.model_selection import train_test_split, KFold, GridSearchCV
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
# CLASIFICACION: Rango de nota de admision
df = pd.read_csv(ADMISION)
features = [
    "ANO_CONCURSO", "SEXO", "NACIONALIDAD", "RANGO_EDAD",
    "PROVINCIA_RESIDENCIA", "CANTON_RESIDENCIA", "SEDE", "RECINTO",
    "TIPO_COLEGIO", "TIPO_HORARIO_COLEGIO", "TIPO_MODALIDAD_COLEGIO",
    "PROVINCIA_COLEGIO", "CANTON_COLEGIO", "TIPO_PROCESO_ADMISION", "CARRERA"]
target = "RANGO_NOTA_ADMISION"
# Benchmark con una muestra
df_b = df.sample(n=min(15000, len(df)), random_state=42)
X = df_b[features]
y = df_b[target]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
pre = ColumnTransformer([
    ("cat", Pipeline([
        ("imp", SimpleImputer(strategy="most_frequent")),
        ("oh", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
    ]), features)
])
models = [
    ("LR", LogisticRegression(max_iter=1000)),
    ("LDA", LinearDiscriminantAnalysis()),
    ("KNN", KNeighborsClassifier()),
    ("CART", DecisionTreeClassifier(random_state=42)),
    ("NB", GaussianNB()),
    ("SVM", SVC())]
# Comparacion de modelos con validacion cruzada
print("COMPARACION DE MODELOS (clasificacion)")
X_bench = X_train.sample(n=min(3000, len(X_train)), random_state=42)
y_bench = y_train.loc[X_bench.index]
for name, model in models:
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    pipe = Pipeline([("pre", pre), ("model", model)])
    cv_results = model_selection.cross_val_score(pipe, X_bench, y_bench, cv=kf, scoring="f1_weighted", n_jobs=-1)
    print("%s: %f (%f)" % (name, cv_results.mean(), cv_results.std()), flush=True)
# LR gano la comparacion, Afinamos sus hiperparametros
print("\nGRIDSEARCHCV - LogisticRegression")
param_grid = {
    "model__C": [0.001, 0.01, 0.1, 1, 10, 100],
    "model__solver": ["lbfgs"],}
lr_pipe = Pipeline([("pre", pre), ("model", LogisticRegression(max_iter=1000))])
lr_cv = GridSearchCV(lr_pipe, param_grid, cv=5, scoring="f1_weighted", n_jobs=-1)
lr_cv.fit(X_train, y_train)
print("Mejores hiperparametros:", lr_cv.best_params_)
print("Mejor F1 weighted promedio (cv=5):", lr_cv.best_score_)
lr = lr_cv.best_estimator_
pred = lr.predict(X_test)
print("\nCLASIFICACION")
print("Accuracy:", accuracy_score(y_test, pred))
print("Precision:", precision_score(y_test, pred, average="weighted", zero_division=0))
print("Recall:", recall_score(y_test, pred, average="weighted", zero_division=0))
print("F1:", f1_score(y_test, pred, average="weighted", zero_division=0))
# Modelo final con todos los registros, usando los mejores hiperparametros.
best_lr_params = {k.replace("model__", ""): v for k, v in lr_cv.best_params_.items()}
modelo_clasificacion = Pipeline([
    ("pre", pre),
    ("model", LogisticRegression(max_iter=1000, **best_lr_params))])
modelo_clasificacion.fit(df[features], df[target])
joblib.dump(modelo_clasificacion, "ml_clasificacion_nota.joblib")
# REGRESION: Cantidad de matriculados por año/universidad/carrera
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
    "DISCIPLINA_UNESCO", "STEM_MICITT"]
cat_r = [c for c in features_r if c != "AÑO"]
pre_r = ColumnTransformer([
    ("num", SimpleImputer(strategy="median"), ["AÑO"]),
    ("cat", Pipeline([
        ("imp", SimpleImputer(strategy="most_frequent")),
        ("oh", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
    ]), cat_r)
])
Xr = reg[features_r]
yr = reg[target_r]
Xr_train, Xr_test, yr_train, yr_test = train_test_split(Xr, yr, test_size=0.2, random_state=42)
models_r = [
    ("LINEAR", LinearRegression()),
    ("KNN", KNeighborsRegressor()),
    ("CART", DecisionTreeRegressor(random_state=42)),
    ("RF", RandomForestRegressor(random_state=42)),
    ("SVR", SVR())]
print("\nCOMPARACION DE MODELOS (regresion)")
for name, model in models_r:
    print("Probando %s..." % name, flush=True)
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    pipe_r = Pipeline([("pre", pre_r), ("model", model)])
    cv_results_r = model_selection.cross_val_score(pipe_r, Xr_train, yr_train, cv=kf, scoring="r2", n_jobs=-1)
    print("%s: %f (%f)" % (name, cv_results_r.mean(), cv_results_r.std()), flush=True)
# RF (Random Forest) gano la comparacion, afinamos sus hiperparametros
print("\nGRIDSEARCHCV - RandomForestRegressor")
param_grid_r = {
    "model__n_estimators": [100, 200, 400],
    "model__max_depth": [None, 5, 10, 20],
    "model__min_samples_leaf": [1, 2, 4],
    "model__max_features": ["sqrt", "log2", None],}
rf_pipe = Pipeline([("pre", pre_r), ("model", RandomForestRegressor(random_state=42))])
rf_cv = GridSearchCV(rf_pipe, param_grid_r, cv=5, scoring="r2", n_jobs=-1)
rf_cv.fit(Xr_train, yr_train)
print("Mejores hiperparametros:", rf_cv.best_params_)
print("Mejor R2 promedio (cv=5):", rf_cv.best_score_)
modelo_regresion_test = rf_cv.best_estimator_
pred_r = modelo_regresion_test.predict(Xr_test)
print("\nREGRESION")
print("MAE:", mean_absolute_error(yr_test, pred_r))
print("RMSE:", mean_squared_error(yr_test, pred_r) ** 0.5)
print("R2:", r2_score(yr_test, pred_r))
# Modelo final con todos los registros, usando los mejores hiperparametros
best_rf_params = {k.replace("model__", ""): v for k, v in rf_cv.best_params_.items()}
modelo_regresion = Pipeline([
    ("pre", pre_r),
    ("model", RandomForestRegressor(random_state=42, **best_rf_params))])
modelo_regresion.fit(reg[features_r], reg[target_r])
joblib.dump(modelo_regresion, "ml_regresion_matriculados.joblib")
reg.to_csv(os.path.join(BASE_DIR, "data", "processed", "matricula_agregada_modelo.csv"), index=False, encoding="utf-8-sig")
print("\nModelos guardados correctamente.")