# ==============================================================================
# Makefile: Data Science - From Yesterday to Tomorrow
# Topic: Formula 1 Race Telemetry, Simulation, Animation & Predictive ML
# ==============================================================================

SHELL := /bin/bash
.DEFAULT_GOAL := help

# Environment configuration
VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
PYTEST := $(VENV)/bin/pytest
JUPYTER := $(VENV)/bin/jupyter

# Check if uv is available for 10-100x faster package resolution
UV := $(shell command -v uv 2>/dev/null)

# Colors for terminal output
COLOR_RESET   := \033[0m
COLOR_INFO    := \033[36m
COLOR_SUCCESS := \033[32m
COLOR_WARNING := \033[33m

.PHONY: help venv install install-dev data test test-cov run-notebooks jupyter presentation colab clean distclean all

help: ## Show this help message with available commands
	@echo ""
	@echo -e "$(COLOR_INFO)======================================================================$(COLOR_RESET)"
	@echo -e "$(COLOR_INFO)  Data Science: From Yesterday to Tomorrow (F1 Edition)               $(COLOR_RESET)"
	@echo -e "$(COLOR_INFO)======================================================================$(COLOR_RESET)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(COLOR_SUCCESS)%-18s$(COLOR_RESET) %s\n", $$1, $$2}'
	@echo ""

venv: ## Create local virtual environment (.venv) using uv or standard venv
	@if [ ! -d "$(VENV)" ]; then \
		echo -e "$(COLOR_INFO)--> Creating virtual environment...$(COLOR_RESET)"; \
		if [ -n "$(UV)" ]; then \
			$(UV) venv $(VENV); \
		else \
			python3 -m venv $(VENV); \
		fi; \
		echo -e "$(COLOR_SUCCESS)--> Virtual environment created at $(VENV)$(COLOR_RESET)"; \
	else \
		echo -e "$(COLOR_WARNING)--> Virtual environment already exists at $(VENV)$(COLOR_RESET)"; \
	fi

install: venv ## Install core project dependencies
	@echo -e "$(COLOR_INFO)--> Installing core dependencies from requirements.txt...$(COLOR_RESET)"
	@if [ -n "$(UV)" ]; then \
		$(UV) pip install --python $(VENV) -r requirements.txt; \
	else \
		$(PIP) install -r requirements.txt; \
	fi
	@echo -e "$(COLOR_SUCCESS)--> Core dependencies installed successfully.$(COLOR_RESET)"

install-dev: venv ## Install development and testing dependencies (pytest, nbconvert)
	@echo -e "$(COLOR_INFO)--> Installing development dependencies from requirements-dev.txt...$(COLOR_RESET)"
	@if [ -n "$(UV)" ]; then \
		$(UV) pip install --python $(VENV) -r requirements-dev.txt; \
	else \
		$(PIP) install -r requirements-dev.txt; \
	fi
	@echo -e "$(COLOR_SUCCESS)--> Development dependencies installed successfully.$(COLOR_RESET)"

data: install ## Generate reproducible F1 telemetry datasets in hands-on/
	@echo -e "$(COLOR_INFO)--> Generating deterministic F1 Monza telemetry dataset...$(COLOR_RESET)"
	@cd hands-on && ../$(PYTHON) f1_simulation.py
	@echo -e "$(COLOR_SUCCESS)--> Datasets generated at hands-on/f1_monza_race_data.csv and hands-on/f1_monza_highres_telemetry.csv$(COLOR_RESET)"

test: install-dev ## Run automated pytest verification suite
	@echo -e "$(COLOR_INFO)--> Running test suite across simulation, models, and notebooks...$(COLOR_RESET)"
	@PYTHONPATH=. $(PYTEST) -v tests/
	@echo -e "$(COLOR_SUCCESS)--> All tests passed successfully!$(COLOR_RESET)"

test-cov: install-dev ## Run test suite with coverage report
	@echo -e "$(COLOR_INFO)--> Running test suite with coverage analysis...$(COLOR_RESET)"
	@PYTHONPATH=hands-on $(PYTEST) --cov=f1_simulation --cov-report=term-missing tests/
	@echo -e "$(COLOR_SUCCESS)--> Coverage analysis complete.$(COLOR_RESET)"

run-notebooks: install-dev data ## Execute all Hands-On Jupyter notebooks in-place
	@echo -e "$(COLOR_INFO)--> Executing hands-on/01_f1_data_generation_and_visualization.ipynb...$(COLOR_RESET)"
	@$(JUPYTER) nbconvert --to notebook --execute --inplace hands-on/01_f1_data_generation_and_visualization.ipynb
	@echo -e "$(COLOR_INFO)--> Executing hands-on/02_f1_race_animation.ipynb...$(COLOR_RESET)"
	@$(JUPYTER) nbconvert --to notebook --execute --inplace hands-on/02_f1_race_animation.ipynb
	@echo -e "$(COLOR_INFO)--> Executing hands-on/03_f1_predictive_modeling_and_whatif.ipynb...$(COLOR_RESET)"
	@$(JUPYTER) nbconvert --to notebook --execute --inplace hands-on/03_f1_predictive_modeling_and_whatif.ipynb
	@echo -e "$(COLOR_SUCCESS)--> All notebooks executed successfully with valid outputs!$(COLOR_RESET)"

jupyter: install ## Launch local JupyterLab web server on port 8888
	@echo -e "$(COLOR_INFO)--> Starting JupyterLab on http://127.0.0.1:8888/lab ...$(COLOR_RESET)"
	@$(PYTHON) -m jupyterlab --no-browser --port=8888 --ip=127.0.0.1 --ServerApp.token='' --ServerApp.password=''

presentation: ## Open Reveal.js keynote presentation in browser
	@echo -e "$(COLOR_INFO)--> Opening Reveal.js keynote presentation at https://erolrecep.github.io/datascience_from_yesterday_to_tomorrow/ ...$(COLOR_RESET)"
	@python3 -m webbrowser "https://erolrecep.github.io/datascience_from_yesterday_to_tomorrow/" || open "https://erolrecep.github.io/datascience_from_yesterday_to_tomorrow/"

colab: ## Print Google Colab direct-launch links
	@echo ""
	@echo -e "$(COLOR_INFO)======================================================================$(COLOR_RESET)"
	@echo -e "$(COLOR_INFO)             GOOGLE COLAB ONE-CLICK LAB LINKS                         $(COLOR_RESET)"
	@echo -e "$(COLOR_INFO)======================================================================$(COLOR_RESET)"
	@echo ""
	@echo -e "Open notebooks directly in Google Colab (no local installation required):"
	@echo ""
	@echo -e "  $(COLOR_SUCCESS)Lab 1 (Data Gen & EDA):$(COLOR_RESET)"
	@echo -e "  https://colab.research.google.com/github/erolrecep/datascience_from_yesterday_to_tomorrow/blob/main/hands-on/01_f1_data_generation_and_visualization.ipynb"
	@echo ""
	@echo -e "  $(COLOR_SUCCESS)Lab 2 (Race Animation):$(COLOR_RESET)"
	@echo -e "  https://colab.research.google.com/github/erolrecep/datascience_from_yesterday_to_tomorrow/blob/main/hands-on/02_f1_race_animation.ipynb"
	@echo ""
	@echo -e "  $(COLOR_SUCCESS)Lab 3 (Predictive & What-If):$(COLOR_RESET)"
	@echo -e "  https://colab.research.google.com/github/erolrecep/datascience_from_yesterday_to_tomorrow/blob/main/hands-on/03_f1_predictive_modeling_and_whatif.ipynb"
	@echo ""
	@echo -e "$(COLOR_WARNING)Note: All notebooks include self-healing dataset loaders for Colab.$(COLOR_RESET)"
	@echo ""

clean: ## Clean Python caches, build artifacts, and checkpoints
	@echo -e "$(COLOR_INFO)--> Cleaning temporary caches and build artifacts...$(COLOR_RESET)"
	@rm -rf __pycache__ tests/__pycache__ hands-on/__pycache__ .pytest_cache .coverage
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".ipynb_checkpoints" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo -e "$(COLOR_SUCCESS)--> Clean complete.$(COLOR_RESET)"

distclean: clean ## Completely remove virtual environment (.venv)
	@echo -e "$(COLOR_INFO)--> Removing virtual environment...$(COLOR_RESET)"
	@rm -rf $(VENV)
	@echo -e "$(COLOR_SUCCESS)--> Environment removed.$(COLOR_RESET)"

all: install-dev data test run-notebooks colab ## Full pipeline: setup, generate data, test, execute notebooks, and display Colab URLs
