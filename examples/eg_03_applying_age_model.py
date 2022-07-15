"""
Applying age models
^^^^^^^^^^^^^^^^^^^

In this scenario, the challenge is to apply an age model to a new selection of
depths. This situation may occur when sampling a core. 
"""
from pathlib import Path
import pandas as pd
import plotly
import plotly.graph_objects as go
import paleos.agemodel as pam
import paleos.common as pcm

# %%
# Begin by defining the location of our age model data and the selection of
# depths for which to calculate ages.
data_path = Path("data")
age_model_path = data_path / "667.csv"
depths_path = data_path / "depth_667.csv"

if not age_model_path.exists():
    raise FileExistsError(f"Unable to find age model {age_model_path}")
if not data_path.exists():
    raise FileExistsError(f"Unable to find data file {data_path}")

# %%
# Next, read in the age model, remove NaNs and provide column names
age_model_df = pd.read_csv(age_model_path, header=None)
age_model_df = age_model_df.dropna()
age_model_df.columns = ["depth", "age"]
print(age_model_df)

# %%
# Set the index to depth, and create a pandas Series by explicitly taking the
# age column
age_model_df = age_model_df.set_index("depth")
age_model = age_model_df["age"]
print(age_model)

# %%
# Add a (0,0) origin point and remove any duplicated depths 
age_model = pam.add_point(age_model, depth=0, age=0, sort_result=True)
age_model = pcm.average_duplicated(age_model)
print(age_model)

# %%
# The next step is to get the depths to calculate ages for
new_depths = pd.read_csv(depths_path, header=None).squeeze("columns")
print(new_depths)

# %%
# Now we have both the age model and the depths we want to apply it to, we can
# do the application using linear resampling from paleos. In this example, 
# linear resampling on to depths is used but there are other options.
new_depth_age = pam.resample_linear(age_model, new_depths.values)
new_depth_age.name = "age"
new_depth_age.index.name = "depth"
print(new_depth_age)

# %%
# Finally plot the original age model and the interpolated values on the new
# depths
fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=age_model.values,
        y=age_model.index,
        mode="lines+markers",
        marker=dict(color="red", symbol="circle", size=10),
        name="age model",
    )
)
fig.add_trace(
    go.Scatter(
        x=new_depth_age.values,
        y=new_depth_age.index,
        mode="markers",
        marker=dict(color="blue", symbol="x"),
        name="depth with age model",
    )
)
fig.update_layout(
    title_text=f"{data_path.stem} with age model {age_model_path.stem}",
    height=800,
    yaxis_title="Depth (m)",
    xaxis_title="Age (Ma)",
)
fig.update_yaxes(autorange="reversed")
plotly.io.show(fig)