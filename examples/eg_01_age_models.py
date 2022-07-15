"""
Age models
^^^^^^^^^^
This module shows how paleos expects to receive age models

An age model is simply a mapping between age and depth at a given location. Age
models are expected to be described using pandas Series. For those unfamiliar
with pandas, please see the documentation.
"""
from pathlib import Path
import pandas as pd

# %%
# Age models should be 
data_path = Path("data")
age_model_path = data_path / "667.csv"

age_model_df = pd.read_csv(age_model_path, header=None)
print(age_model_df)