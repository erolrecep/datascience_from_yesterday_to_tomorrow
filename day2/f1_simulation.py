"""
Formula 1 Race Telemetry Simulation Engine
Topic: Autodromo Nazionale Monza - Macro 53 Laps & Continuous Intra-Lap Telemetry
Used by Day 2 interactive notebooks, animation studio, and automated pytest test suites.
"""

import numpy as np
import pandas as pd

DRIVERS_GRID = [
    {"driver": "VER", "name": "Max Verstappen", "team": "Red Bull Racing", "car_base": 9.6, "dry_skill": 9.8, "wet_skill": 9.9, "color": "#1E41B0", "pit_laps": [24]},
    {"driver": "NOR", "name": "Lando Norris", "team": "McLaren", "car_base": 9.5, "dry_skill": 9.6, "wet_skill": 9.5, "color": "#FF8000", "pit_laps": [22]},
    {"driver": "LEC", "name": "Charles Leclerc", "team": "Ferrari", "car_base": 9.3, "dry_skill": 9.7, "wet_skill": 9.4, "color": "#E80020", "pit_laps": [20]},
    {"driver": "HAM", "name": "Lewis Hamilton", "team": "Mercedes", "car_base": 9.1, "dry_skill": 9.6, "wet_skill": 9.95, "color": "#27F4D2", "pit_laps": [26]},
    {"driver": "PIA", "name": "Oscar Piastri", "team": "McLaren", "car_base": 9.5, "dry_skill": 9.4, "wet_skill": 9.3, "color": "#E56B00", "pit_laps": [23]},
    {"driver": "SAI", "name": "Carlos Sainz", "team": "Ferrari", "car_base": 9.3, "dry_skill": 9.4, "wet_skill": 9.3, "color": "#CC0000", "pit_laps": [21]},
    {"driver": "RUS", "name": "George Russell", "team": "Mercedes", "car_base": 9.1, "dry_skill": 9.4, "wet_skill": 9.4, "color": "#00A19B", "pit_laps": [25]},
    {"driver": "PER", "name": "Sergio Perez", "team": "Red Bull Racing", "car_base": 9.6, "dry_skill": 8.9, "wet_skill": 8.8, "color": "#001A72", "pit_laps": [27]},
    {"driver": "ALO", "name": "Fernando Alonso", "team": "Aston Martin", "car_base": 8.7, "dry_skill": 9.5, "wet_skill": 9.8, "color": "#229971", "pit_laps": [19]},
    {"driver": "ALB", "name": "Alexander Albon", "team": "Williams", "car_base": 8.5, "dry_skill": 9.0, "wet_skill": 9.1, "color": "#64C4FF", "pit_laps": [22]},
    {"driver": "STR", "name": "Lance Stroll", "team": "Aston Martin", "car_base": 8.7, "dry_skill": 8.5, "wet_skill": 9.2, "color": "#00594F", "pit_laps": [18]},
    {"driver": "TSU", "name": "Yuki Tsunoda", "team": "RB", "car_base": 8.4, "dry_skill": 8.7, "wet_skill": 8.7, "color": "#6692FF", "pit_laps": [20]},
    {"driver": "HUL", "name": "Nico Hulkenberg", "team": "Haas", "car_base": 8.3, "dry_skill": 8.8, "wet_skill": 8.9, "color": "#B6BABD", "pit_laps": [21]},
    {"driver": "RIC", "name": "Daniel Ricciardo", "team": "RB", "car_base": 8.4, "dry_skill": 8.6, "wet_skill": 8.6, "color": "#1634CB", "pit_laps": [22]},
    {"driver": "GAS", "name": "Pierre Gasly", "team": "Alpine", "car_base": 8.2, "dry_skill": 8.7, "wet_skill": 8.8, "color": "#0093CC", "pit_laps": [19]},
    {"driver": "OCO", "name": "Esteban Ocon", "team": "Alpine", "car_base": 8.2, "dry_skill": 8.7, "wet_skill": 9.0, "color": "#FF87BC", "pit_laps": [20]},
    {"driver": "MAG", "name": "Kevin Magnussen", "team": "Haas", "car_base": 8.3, "dry_skill": 8.5, "wet_skill": 8.6, "color": "#787878", "pit_laps": [23]},
    {"driver": "BOT", "name": "Valtteri Bottas", "team": "Kick Sauber", "car_base": 7.9, "dry_skill": 8.6, "wet_skill": 8.7, "color": "#52E252", "pit_laps": [19]},
    {"driver": "ZHO", "name": "Zhou Guanyu", "team": "Kick Sauber", "car_base": 7.9, "dry_skill": 8.3, "wet_skill": 8.3, "color": "#00B800", "pit_laps": [18]},
    {"driver": "SAR", "name": "Logan Sargeant", "team": "Williams", "car_base": 8.5, "dry_skill": 8.0, "wet_skill": 7.9, "color": "#003366", "pit_laps": [17]}
]

def generate_f1_race_telemetry(seed=42, total_laps=53, drivers=None):
    """
    Generates deterministic macro F1 race telemetry for Monza over 53 laps.
    """
    if drivers is None:
        drivers = DRIVERS_GRID
        
    np.random.seed(seed)
    base_lap_time = 84.0
    records = []
    
    for grid_idx, meta in enumerate(drivers):
        current_compound = "Medium"
        tyre_age = 0
        cum_time = grid_idx * 0.40
        fuel = 100.0
        pit_count = 0
        
        for lap in range(1, total_laps + 1):
            fuel_burn = 1.80
            fuel = max(5.0, 100.0 - (lap - 1) * fuel_burn)
            
            is_pit = lap in meta.get("pit_laps", [])
            if is_pit:
                pit_count += 1
                pit_loss = 22.50
                current_compound = "Hard"
                tyre_age = 0
            else:
                pit_loss = 0.0
                tyre_age += 1
                
            deg_rate = 0.045 if current_compound == "Medium" else 0.022
            tyre_penalty = (tyre_age ** 1.15) * deg_rate
            compound_pace_benefit = -0.40 if current_compound == "Medium" else 0.0
            fuel_penalty = fuel * 0.033
            
            car_benefit = (meta["car_base"] - 8.0) * 0.35
            driver_benefit = (meta["dry_skill"] - 8.0) * 0.25
            noise = np.random.normal(0, 0.12)
            
            lap_time = (base_lap_time 
                        + compound_pace_benefit 
                        + fuel_penalty 
                        + tyre_penalty 
                        + pit_loss 
                        - car_benefit 
                        - driver_benefit 
                        + noise)
            
            cum_time += lap_time
            speed_trap = 330.0 + (meta["car_base"] - 8.0) * 5.5 + np.random.normal(0, 1.2) - (fuel * 0.03)
            track_temp = 38.0 + (lap / total_laps) * 2.5 + np.random.normal(0, 0.2)
            
            records.append({
                "lap": lap,
                "driver": meta["driver"],
                "driver_name": meta["name"],
                "team": meta["team"],
                "car_base_performance": meta["car_base"],
                "driver_dry_skill": meta["dry_skill"],
                "driver_wet_skill": meta["wet_skill"],
                "tyre_compound": current_compound,
                "tyre_age": tyre_age,
                "fuel_load_kg": round(fuel, 2),
                "track_temp_c": round(track_temp, 2),
                "speed_trap_kmh": round(speed_trap, 2),
                "pit_stop_this_lap": 1 if is_pit else 0,
                "pit_stops_total": pit_count,
                "lap_time_s": round(lap_time, 3),
                "cumulative_time_s": round(cum_time, 3)
            })
            
    df = pd.DataFrame(records)
    df["position"] = df.groupby("lap")["cumulative_time_s"].rank(method="min").astype(int)
    leaders = df.groupby("lap")["cumulative_time_s"].transform("min")
    df["gap_to_leader_s"] = (df["cumulative_time_s"] - leaders).round(3)
    return df

def simulate_wet_race(seed=42, total_laps=53, drivers=None):
    """
    Counterfactual simulation under heavy rain conditions.
    """
    if drivers is None:
        drivers = DRIVERS_GRID
        
    np.random.seed(seed)
    base_wet_lap = 96.0
    records = []
    
    for grid_idx, meta in enumerate(drivers):
        cum_time = grid_idx * 0.40
        tyre_age = 0
        fuel = 100.0
        
        for lap in range(1, total_laps + 1):
            fuel_burn = 1.75
            fuel = max(5.0, 100.0 - (lap - 1) * fuel_burn)
            tyre_age += 1
            
            tyre_penalty = (tyre_age ** 1.10) * 0.035
            fuel_penalty = fuel * 0.028
            
            team_wet_bonus = 0.30 if meta["team"] in ["Mercedes", "Aston Martin"] else 0.0
            car_benefit = (meta["car_base"] - 8.0) * 0.10 + team_wet_bonus
            driver_benefit = (meta["wet_skill"] - 8.0) * 0.85
            wet_noise = np.random.normal(0, 0.28)
            
            is_pit = (lap == 24)
            pit_loss = 23.5 if is_pit else 0.0
            if is_pit:
                tyre_age = 0
                
            lap_time = (base_wet_lap + fuel_penalty + tyre_penalty + pit_loss 
                        - car_benefit - driver_benefit + wet_noise)
            cum_time += lap_time
            
            records.append({
                "lap": lap,
                "driver": meta["driver"],
                "driver_name": meta["name"],
                "team": meta["team"],
                "car_base_performance": meta["car_base"],
                "driver_wet_skill": meta["wet_skill"],
                "lap_time_s": round(lap_time, 3),
                "cumulative_time_s": round(cum_time, 3)
            })
            
    df_wet = pd.DataFrame(records)
    df_wet["position"] = df_wet.groupby("lap")["cumulative_time_s"].rank(method="min").astype(int)
    leaders = df_wet.groupby("lap")["cumulative_time_s"].transform("min")
    df_wet["gap_to_leader_s"] = (df_wet["cumulative_time_s"] - leaders).round(3)
    return df_wet

def get_monza_circuit_track(num_points=1000):
    """
    Parametric geometry for Monza circuit.
    """
    t = np.linspace(0, 2 * np.pi, num_points, endpoint=False)
    x = 6.0 * np.cos(t) + 1.2 * np.cos(2 * t) - 0.4 * np.sin(3 * t)
    y = 2.4 * np.sin(t) - 0.8 * np.sin(2 * t) + 0.3 * np.cos(3 * t)
    theta = np.radians(25)
    xr = x * np.cos(theta) - y * np.sin(theta)
    yr = x * np.sin(theta) + y * np.cos(theta)
    return xr, yr

def get_monza_speed_profile(progress_fraction):
    """
    Returns realistic corner/straight speed (km/h) along Monza track progress fraction [0, 1).
    Landmarks:
      0.00 - 0.12: Main Straight (Rettifilo Tribune) ~340 km/h
      0.12 - 0.18: Turn 1-2 Variante del Rettifilo Chicane (Heavy braking to 80 km/h)
      0.18 - 0.32: Curva Grande (High speed curve) ~280 km/h
      0.32 - 0.40: Variante della Roggia Chicane ~115 km/h
      0.40 - 0.60: Curva di Lesmo 1 & 2 ~175 km/h
      0.60 - 0.70: Curva del Serraglio Straight ~320 km/h
      0.70 - 0.80: Variante Ascari Chicane ~190 km/h
      0.80 - 0.90: Back Straight (Opposite Tribune) ~335 km/h
      0.90 - 1.00: Curva Parabolica / Alboreto ~215-280 km/h
    """
    p = progress_fraction % 1.0
    if p < 0.12:
        return 340.0 - (p / 0.12) * 20.0
    elif p < 0.18:
        return 80.0 + ((p - 0.12) / 0.06) * 45.0
    elif p < 0.32:
        return 280.0 + np.sin((p - 0.18) / 0.14 * np.pi) * 25.0
    elif p < 0.40:
        return 115.0
    elif p < 0.60:
        return 175.0
    elif p < 0.70:
        return 320.0
    elif p < 0.80:
        return 190.0
    elif p < 0.90:
        return 335.0
    else:
        return 215.0 + ((p - 0.90) / 0.10) * 105.0

def generate_highres_telemetry(df_macro_data=None, start_lap=1, end_lap=2, steps_per_lap=30, seed=42):
    """
    Generates continuous intra-lap high-resolution telemetry.
    Discretizes each lap into sub-second steps so cars can be animated continuously 
    gliding through corners, braking into chicanes, and overtaking on straights.
    """
    if df_macro_data is None:
        df_macro_data = generate_f1_race_telemetry(seed=seed)
        
    track_x, track_y = get_monza_circuit_track(num_points=1000)
    total_points = len(track_x)
    records = []
    
    sub_macro = df_macro_data[(df_macro_data["lap"] >= start_lap) & (df_macro_data["lap"] <= end_lap)]
    
    for lap in range(start_lap, end_lap + 1):
        lap_drivers = sub_macro[sub_macro["lap"] == lap].sort_values("position")
        
        for step in range(steps_per_lap):
            frac = step / float(steps_per_lap)
            
            for _, d_row in lap_drivers.iterrows():
                driver = d_row["driver"]
                car_gap = d_row["gap_to_leader_s"]
                
                # Intra-lap progress offset based on gap to leader
                car_progress = (frac - (car_gap / 84.0)) % 1.0
                track_idx = int(car_progress * total_points) % total_points
                
                cx = track_x[track_idx]
                cy = track_y[track_idx]
                
                # Speed profile modified by car engine performance
                base_spd = get_monza_speed_profile(car_progress)
                speed_kmh = base_spd + (d_row["car_base_performance"] - 8.0) * 4.0
                
                records.append({
                    "lap": lap,
                    "step": step,
                    "global_frame": (lap - start_lap) * steps_per_lap + step,
                    "driver": driver,
                    "driver_name": d_row["driver_name"],
                    "team": d_row["team"],
                    "position": d_row["position"],
                    "gap_to_leader_s": d_row["gap_to_leader_s"],
                    "track_progress": round(car_progress, 4),
                    "pos_x": round(cx, 3),
                    "pos_y": round(cy, 3),
                    "speed_kmh": round(speed_kmh, 1),
                    "tyre_compound": d_row["tyre_compound"],
                    "pit_stop_this_lap": d_row["pit_stop_this_lap"]
                })
                
    return pd.DataFrame(records)

if __name__ == "__main__":
    df = generate_f1_race_telemetry()
    df.to_csv("f1_monza_race_data.csv", index=False)
    print(f"Generated {len(df)} rows to 'f1_monza_race_data.csv'")
    
    df_hi = generate_highres_telemetry(df, start_lap=1, end_lap=2, steps_per_lap=30)
    df_hi.to_csv("f1_monza_highres_telemetry.csv", index=False)
    print(f"Generated {len(df_hi)} high-resolution rows to 'f1_monza_highres_telemetry.csv'")
