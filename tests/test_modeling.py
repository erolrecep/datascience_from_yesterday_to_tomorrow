import sys
import os
import pytest
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.inspection import permutation_importance
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'hands-on'))
from f1_simulation import generate_f1_race_telemetry, simulate_wet_race

@pytest.fixture(scope="module")
def race_data():
    return generate_f1_race_telemetry(seed=42)

def test_predictive_model_accuracy(race_data):
    df_racing = race_data[race_data["pit_stop_this_lap"] == 0].copy()
    df_racing["compound_code"] = (df_racing["tyre_compound"] == "Hard").astype(int)
    
    features = [
        "fuel_load_kg", "tyre_age", "compound_code",
        "car_base_performance", "driver_dry_skill",
        "speed_trap_kmh", "track_temp_c"
    ]
    X = df_racing[features]
    y = df_racing["lap_time_s"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    
    assert r2 >= 0.90, f"Expected R² >= 0.90, got {r2:.4f}"
    assert rmse < 0.35, f"Expected RMSE < 0.35 seconds, got {rmse:.4f}"

def test_feature_dominance_ranking(race_data):
    df_racing = race_data[race_data["pit_stop_this_lap"] == 0].copy()
    df_racing["compound_code"] = (df_racing["tyre_compound"] == "Hard").astype(int)
    
    features = [
        "fuel_load_kg", "tyre_age", "compound_code",
        "car_base_performance", "driver_dry_skill",
        "speed_trap_kmh", "track_temp_c"
    ]
    X = df_racing[features]
    y = df_racing["lap_time_s"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    model = RandomForestRegressor(n_estimators=80, max_depth=8, random_state=42)
    model.fit(X_train, y_train)
    
    perm = permutation_importance(model, X_test, y_test, n_repeats=5, random_state=42)
    top_features = [features[i] for i in perm.importances_mean.argsort()[::-1]]
    
    top_4 = set(top_features[:4])
    assert "compound_code" in top_4
    assert "car_base_performance" in top_4
    assert "fuel_load_kg" in top_4

def test_wet_weather_counterfactual(race_data):
    df_wet = simulate_wet_race(seed=42)
    assert len(df_wet) == 1060
    
    dry_p1 = race_data[(race_data["lap"] == 53) & (race_data["position"] == 1)]["driver"].iloc[0]
    wet_p1 = df_wet[(df_wet["lap"] == 53) & (df_wet["position"] == 1)]["driver"].iloc[0]
    
    assert dry_p1 == "VER", f"Expected VER dry winner, got {dry_p1}"
    assert wet_p1 == "HAM", f"Expected HAM wet winner, got {wet_p1}"
    
    dry_alo_pos = race_data[(race_data["lap"] == 53) & (race_data["driver"] == "ALO")]["position"].iloc[0]
    wet_alo_pos = df_wet[(df_wet["lap"] == 53) & (df_wet["driver"] == "ALO")]["position"].iloc[0]
    assert wet_alo_pos < dry_alo_pos - 3, f"Expected ALO to gain >= 4 positions, dry: {dry_alo_pos}, wet: {wet_alo_pos}"
