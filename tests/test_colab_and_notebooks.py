import os
import json
import pytest

WORKDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HANDSON_DIR = os.path.join(WORKDIR, "hands-on")

NOTEBOOKS = [
    "01_f1_data_generation_and_visualization.ipynb",
    "02_f1_race_animation.ipynb",
    "03_f1_predictive_modeling_and_whatif.ipynb"
]

@pytest.mark.parametrize("nb_name", NOTEBOOKS)
def test_notebook_structure_and_colab_badge(nb_name):
    nb_path = os.path.join(HANDSON_DIR, nb_name)
    assert os.path.exists(nb_path), f"Notebook missing: {nb_name}"
    
    with open(nb_path, "r", encoding="utf-8") as f:
        nb = json.load(f)
        
    assert "cells" in nb, "Notebook must contain cells."
    assert "metadata" in nb, "Notebook must contain metadata."
    assert nb["nbformat"] == 4, "Notebook format version must be 4."
    
    # Check Colab badge in first markdown cell
    first_cell_src = "".join(nb["cells"][0]["source"])
    assert "colab-badge.svg" in first_cell_src, f"Colab badge missing from {nb_name}"
    assert "colab.research.google.com" in first_cell_src, f"Colab URL missing from {nb_name}"
    assert "hands-on" in first_cell_src, f"Colab URL in {nb_name} should point to hands-on directory"

@pytest.mark.parametrize("nb_name", NOTEBOOKS)
def test_notebook_colab_bootstrap(nb_name):
    nb_path = os.path.join(HANDSON_DIR, nb_name)
    with open(nb_path, "r", encoding="utf-8") as f:
        nb = json.load(f)
        
    has_colab_check = False
    for cell in nb["cells"]:
        if cell["cell_type"] == "code":
            src = "".join(cell["source"])
            if "IN_COLAB" in src or "google.colab" in src:
                has_colab_check = True
                break
                
    assert has_colab_check, f"Self-healing Colab check missing from {nb_name}"
