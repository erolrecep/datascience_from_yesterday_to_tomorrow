import sys
import os
import pytest
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'day2'))

from f1_simulation import (
    generate_f1_race_telemetry,
    simulate_wet_race,
    get_monza_circuit_track,
    get_monza_speed_profile,
    generate_highres_telemetry,
    DRIVERS_GRID
)

def test_drivers_grid_integrity():
    assert len(DRIVERS_GRID) == 20, "Expected full 20-driver grid."
    teams = {d["team"] for d in DRIVERS_GRID}
    assert len(teams) == 10, "Expected exactly 10 Formula 1 constructors."
    for d in DRIVERS_GRID:
        assert "driver" in d and len(d["driver"]) == 3
        assert 7.0 <= d["car_base"] <= 10.0
        assert 7.0 <= d["dry_skill"] <= 10.0
        assert 7.0 <= d["wet_skill"] <= 10.0
        assert "color" in d and d["color"].startswith("#")

def test_data_generation_shape_and_determinism():
    df1 = generate_f1_race_telemetry(seed=42, total_laps=53)
    df2 = generate_f1_race_telemetry(seed=42, total_laps=53)
    
    assert len(df1) == 53 * 20, f"Expected 1060 records, got {len(df1)}"
    assert list(df1.columns) == list(df2.columns)
    assert len(df1.columns) == 18
    pd.testing.assert_frame_equal(df1, df2)

def test_physical_invariants():
    df = generate_f1_race_telemetry(seed=42, total_laps=53)
    
    for lap in range(1, 54):
        lap_df = df[df["lap"] == lap]
        positions = sorted(lap_df["position"].tolist())
        assert positions == list(range(1, 21)), f"Positions on lap {lap} are not 1..20"
        
    leaders = df[df["position"] == 1]
    assert (leaders["gap_to_leader_s"] == 0.0).all()
    
    ver_df = df[df["driver"] == "VER"].sort_values("lap")
    assert ver_df["fuel_load_kg"].iloc[0] == 100.0
    assert ver_df["fuel_load_kg"].iloc[-1] < 10.0
    assert (ver_df["fuel_load_kg"].diff().dropna() <= 0).all()
    
    pit_laps = df[df["pit_stop_this_lap"] == 1]
    non_pit_laps = df[df["pit_stop_this_lap"] == 0]
    assert pit_laps["lap_time_s"].mean() > non_pit_laps["lap_time_s"].mean() + 18.0

def test_circuit_geometry():
    x, y = get_monza_circuit_track(num_points=300)
    assert isinstance(x, np.ndarray) and isinstance(y, np.ndarray)
    assert len(x) == len(y) == 300
    dx = x[0] - x[-1]
    dy = y[0] - y[-1]
    dist = np.sqrt(dx**2 + dy**2)
    assert dist < 0.5, "Track should be a closed circuit curve."

def test_speed_profile_and_highres_telemetry():
    straight_spd = get_monza_speed_profile(0.05)
    chicane_spd = get_monza_speed_profile(0.15)
    assert straight_spd > 300.0, f"Expected straight speed > 300, got {straight_spd}"
    assert chicane_spd < 110.0, f"Expected chicane speed < 110, got {chicane_spd}"

    df_hi = generate_highres_telemetry(start_lap=1, end_lap=2, steps_per_lap=25, seed=42)
    assert len(df_hi) == 2 * 25 * 20, f"Expected 1000 rows, got {len(df_hi)}"
    assert "speed_kmh" in df_hi.columns
    assert "pos_x" in df_hi.columns
    assert "pos_y" in df_hi.columns
    assert df_hi["speed_kmh"].min() > 60.0
    assert df_hi["speed_kmh"].max() > 320.0
