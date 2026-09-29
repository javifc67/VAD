"""
Módulo de Machine Learning para el Observatorio Europeo (Demo Day 2).
Entrena modelos Random Forest para predecir el impacto de políticas públicas
(inversión en I+D, Sanidad y Renovables) sobre el PIB per cápita y la Esperanza de Vida.
"""

import os
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.model_selection import train_test_split

MODEL_FILE = os.path.join(os.path.dirname(__file__), 'data', 'models_rf.joblib')

FEATURES = [
    'rd_expenditure',
    'health_expenditure',
    'renewable_energy_pct',
    'unemployment_rate',
    'inflation_rate',
    'exports_pct_gdp',
]


def entrenar_modelos(data_path=None):
    """Entrena y persiste dos regresores Random Forest con evaluación de métricas."""
    if data_path is None:
        data_path = os.path.join(os.path.dirname(__file__), 'data', 'europe_macro_historical.csv')

    df = pd.read_csv(data_path)
    X = df[FEATURES]
    y_gdp = df['gdp_per_capita']
    y_life = df['life_expectancy']

    # División entrenamiento / test
    X_train, X_test, y_gdp_train, y_gdp_test, y_life_train, y_life_test = train_test_split(
        X, y_gdp, y_life, test_size=0.2, random_state=42
    )

    # 1. Regresor de PIB per cápita
    rf_gdp = RandomForestRegressor(n_estimators=100, max_depth=12, random_state=42)
    rf_gdp.fit(X_train, y_gdp_train)
    pred_gdp = rf_gdp.predict(X_test)
    r2_gdp = r2_score(y_gdp_test, pred_gdp)
    mae_gdp = mean_absolute_error(y_gdp_test, pred_gdp)

    # 2. Regresor de Esperanza de Vida
    rf_life = RandomForestRegressor(n_estimators=100, max_depth=12, random_state=42)
    rf_life.fit(X_train, y_life_train)
    pred_life = rf_life.predict(X_test)
    r2_life = r2_score(y_life_test, pred_life)
    mae_life = mean_absolute_error(y_life_test, pred_life)

    # Importancia de variables para explicabilidad
    importancias_gdp = dict(zip(FEATURES, rf_gdp.feature_importances_))
    importancias_life = dict(zip(FEATURES, rf_life.feature_importances_))

    resultados = {
        'rf_gdp': rf_gdp,
        'rf_life': rf_life,
        'features': FEATURES,
        'metrics': {
            'gdp': {'r2': r2_gdp, 'mae': mae_gdp, 'importances': importancias_gdp},
            'life': {'r2': r2_life, 'mae': mae_life, 'importances': importancias_life},
        }
    }

    joblib.dump(resultados, MODEL_FILE)
    print(f"Modelos entrenados y guardados en {MODEL_FILE}")
    print(f"  PIB per cápita   -> R²: {r2_gdp:.3f} | MAE: ${mae_gdp:,.0f}")
    print(f"  Esperanza de vida -> R²: {r2_life:.3f} | MAE: {mae_life:.2f} años")
    return resultados


def cargar_modelos():
    """Carga los modelos entrenados. Si no existen, los entrena."""
    if not os.path.exists(MODEL_FILE):
        return entrenar_modelos()
    return joblib.load(MODEL_FILE)


def simular_politica(features_base, delta_rd=0.0, delta_health=0.0, delta_renew=0.0):
    """
    Simula el impacto de variaciones en I+D, salud y renovables
    respecto a las condiciones de partida de un país.
    """
    modelos = cargar_modelos()
    rf_gdp = modelos['rf_gdp']
    rf_life = modelos['rf_life']

    # Vector base y simulado como DataFrames con nombres de columnas
    df_base = pd.DataFrame([[features_base[f] for f in FEATURES]], columns=FEATURES)

    # Vector simulado
    feat_sim = dict(features_base)
    feat_sim['rd_expenditure'] = max(0.1, feat_sim['rd_expenditure'] + delta_rd)
    feat_sim['health_expenditure'] = max(1.0, feat_sim['health_expenditure'] + delta_health)
    feat_sim['renewable_energy_pct'] = min(100.0, max(0.0, feat_sim['renewable_energy_pct'] + delta_renew))
    df_sim = pd.DataFrame([[feat_sim[f] for f in FEATURES]], columns=FEATURES)

    # Predicciones
    base_gdp_pred = rf_gdp.predict(df_base)[0]
    sim_gdp_pred = rf_gdp.predict(df_sim)[0]

    base_life_pred = rf_life.predict(df_base)[0]
    sim_life_pred = rf_life.predict(df_sim)[0]

    return {
        'gdp_base': base_gdp_pred,
        'gdp_sim': sim_gdp_pred,
        'gdp_delta': sim_gdp_pred - base_gdp_pred,
        'life_base': base_life_pred,
        'life_sim': sim_life_pred,
        'life_delta': sim_life_pred - base_life_pred,
        'features_sim': feat_sim,
    }


if __name__ == '__main__':
    entrenar_modelos()
