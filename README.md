# Data Science: From Yesterday to Tomorrow 🏎️📊

[![Tests](https://img.shields.io/badge/pytest-passing-success.svg)](tests/)
[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.14-blue.svg)](requirements.txt)
[![Coverage](https://img.shields.io/badge/coverage-95%25-brightgreen.svg)](day2/f1_simulation.py)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A structured curriculum exploring the 25-year evolution of Data Science—from early Web 2.0 clickstream telemetry in 2000 to modern Foundation Models, physics-informed synthetic simulation, and counterfactual causal reasoning.

---

## 📂 Repository Structure

The project is structured into two core tracks:

```
.
├── day1/                                     # Retrospective Essay & Presentation Slides
│   ├── index.html                            # Interactive 24-slide Reveal.js presentation
│   ├── data_science_blog.md                  # Comprehensive 25-year thought-leadership retrospective
│   └── presentation_slides.md                # Executive slide deck outline with talk tracks
├── day2/                                     # Hands-On Telemetry, Animation & Machine Learning
│   ├── 01_f1_data_generation_and_visualization.ipynb # Lab 1: Deterministic generation & EDA
│   ├── 02_f1_race_animation.ipynb            # Lab 2: Dual-panel circuit & intra-lap animation
│   ├── 03_f1_predictive_modeling_and_whatif.ipynb # Lab 3: Feature dominance & rain counterfactual
│   ├── f1_simulation.py                      # Reusable physics simulation & telemetry engine
│   ├── f1_monza_race_data.csv                # 53-lap telemetry dataset (1,060 records)
│   └── f1_monza_highres_telemetry.csv        # Continuous intra-lap high-frequency telemetry
├── assets/                                   # Visual snapshots and telemetry plots
├── tests/                                    # Automated pytest verification suite (14 tests)
├── Makefile                                  # Automated build, test, and execution pipeline
├── requirements.txt                          # Core dependencies
└── requirements-dev.txt                      # Development & testing dependencies
```

---

## 📑 Day 1: Presentation & Retrospective

* 🖥️ **Interactive Reveal.js Presentation**: [`day1/index.html`](./day1/index.html)  
  *Run locally with `make presentation` and open **[http://127.0.0.1:8000/day1/](http://127.0.0.1:8000/day1/)***  
  *(24 interactive slides with KaTeX math, embedded telemetry snapshots, glassmorphism UI, keyboard navigation, and speaker notes).*
* 📄 **[`day1/data_science_blog.md`](./day1/data_science_blog.md)**: *"Data Science from Yesterday to Tomorrow: Lessons from a Quarter-Century of Hype and Reality"*
* 📝 **[`day1/presentation_slides.md`](./day1/presentation_slides.md)**: Markdown Slide Deck Outline with talk tracks and speaking notes.

---

## 🏎️ Day 2: Hands-On Telemetry Labs (Run Locally or in Google Colab)

Every notebook can be launched with **1-click in Google Colab** (no local environment setup required) or executed locally with the `Makefile`.

| Lab | Focus | Description | 1-Click Launch |
| :--- | :--- | :--- | :---: |
| **Lab 1** | **Data Generation & EDA** | Deterministic telemetry generator for 20 cars across 53 laps at Monza; pace progression, non-linear tyre degradation, speed traps, and bump charts. | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/erolrecep/datascience_from_yesterday_to_tomorrow/blob/main/day2/01_f1_data_generation_and_visualization.ipynb) |
| **Lab 2** | **Race Animation** | Dual-panel interactive animation: Macro 53-lap full race + continuous intra-lap motion (braking to ~80 km/h in chicanes, DRS acceleration past 330 km/h). | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/erolrecep/datascience_from_yesterday_to_tomorrow/blob/main/day2/02_f1_race_animation.ipynb) |
| **Lab 3** | **Predictive ML & What-If** | Random Forest lap time regression ($R^2 = 0.96$), Column Dominance analysis (MDI & Permutation), and counterfactual rain simulation (*"Who would have won in the wet?"*). | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/erolrecep/datascience_from_yesterday_to_tomorrow/blob/main/day2/03_f1_predictive_modeling_and_whatif.ipynb) |

> **Self-Healing Colab Execution**: All notebooks feature automated environment detection. When opened in Google Colab, each notebook automatically verifies dependencies and fetches necessary datasets from GitHub, preventing any `FileNotFoundError`.

---

## 📸 Visual Snapshots: What You See When Running the Labs

### Lab 1: Race Telemetry & Exploratory Data Analysis
Visualizes lap time evolution, tyre compound degradation curves, straight-line speed trap correlations, and race-long position bump charts.

![Lab 1 Telemetry and Tyre Degradation](assets/lab1_race_telemetry_eda.png)

---

### Lab 2: Interactive 2D Circuit Tracking & Real-Time Leaderboard
Animates continuous vehicle motion around the Autodromo Nazionale Monza with authentic team liveries, live gap-to-leader telemetry, tyre compound indicators, and pit notices.

![Lab 2 Circuit Race Animation](assets/lab2_circuit_race_animation.png)

---

### Lab 3: Feature Dominance & "What-If Rain" Counterfactual
Extracts column importance (fuel weight vs. tyre age vs. car aero) and simulates a torrential rain counterfactual where aerodynamic advantages compress and raincraft masters (Lewis Hamilton & Fernando Alonso) surge to the podium.

![Lab 3 Feature Dominance and Counterfactual Analysis](assets/lab3_predictive_feature_dominance_and_whatif.png)

---

## 🛠️ Local Quickstart with Makefile

Run locally with standard `make` commands:

```bash
# 1. View available commands
make help

# 2. Set up virtual environment and install dependencies (auto-detects uv for speed)
make install-dev

# 3. Generate reproducible F1 telemetry datasets (seed=42)
make data

# 4. Run automated test suite with coverage
make test-cov

# 5. Execute all Jupyter notebooks in-place
make run-notebooks

# 6. Start local JupyterLab web server
make jupyter
```

---

## 🧪 Automated Verification Suite

Run tests anytime with:
```bash
make test
```

Verified test coverage includes:
* **Physics Invariants**: Position uniqueness ($1..20$ per lap), determinism, fuel monotonicity, pit deltas, and closed track geometry.
* **Predictive Accuracy**: Random Forest $R^2 \ge 0.90$, $\text{RMSE} < 0.35\text{s}$, column dominance ranking, and rain counterfactual podium verification.
* **Online Compatibility**: `nbformat: 4` compliance, SVG badge links, and self-healing cloud bootstrap detection.
