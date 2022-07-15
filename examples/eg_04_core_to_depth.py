"""
Extracting sample depths
^^^^^^^^^^^^^^^^^^^^^^^^

This example merges core section top depth and sample depth to provide depths
for individual samples. It does not require paleos at all and is here to serve
as an example for those who have a similar challenge.
"""
from pathlib import Path
import pandas as pd

# %%
# Begin by defining the location of our data
data_path = Path("data")
samples_path = data_path / "samples_biom_730.csv"
depth_path = data_path / "section_summary_730.csv"

# %%
# Read in the sample data
df_samples = pd.read_csv(samples_path)
df_samples["Hole"] = [x.strip("'") for x in df_samples["Hole"]]
df_samples.loc[df_samples["Section"] == "CC", "Section"] = 20
df_samples["Section"] = df_samples["Section"].astype(int)
print(df_samples)

# %%
# Read in depth data for the core
df_depth = pd.read_csv(depth_path)
df_depth = df_depth.dropna(subset=["Section"])
df_depth.loc[df_depth["Section"].str.contains("CC"), "Section"] = 20
df_depth["Section"] = df_depth["Section"].astype(int)
print(df_depth)

# %%
# Use pandas merging to put the two together and get sample depth
df = pd.merge(
    df_samples,
    df_depth,
    how="left",
    left_on=["Hole", "Core", "Section"],
    right_on=["Hole", "Core", "Section"],
)
df["Depth"] = df["Top depth CSF-A (m)"] + (df["Top (cm)"]/100)
df.to_csv("samples_with_depth.csv", index=False)
print(df)