"""
Resampling methods
^^^^^^^^^^^^^^^^^^

An example to compare different resampling methods for age models. Usually, age
models are not sampled on regular depth intervals. It can often be useful to
have age models that are regularly sampled. There are several methods in paleos
for achieving this including:

- linear resample
- cubic resample
- spline resample
- LOESS resample (local least squares)
- LOWESS resample (locally weighted least squares)

Each of these will give a different result. Expert discretion should be used
when choosing the best method to use. Each method will have pros and cons.
"""
import numpy as np
import pandas as pd
import plotly
import plotly.graph_objects as go
import paleos.common as pcm
import paleos.agemodel as pam

# %%
# Read in the original age model data
age_model = pd.read_csv("data/NathanLeckie_1146_GTS12.csv", header=None)
age_model.columns=["Depth", "Age"]
age_model = age_model.set_index("Depth").squeeze("columns")
print(age_model)

# %%
# There are some duplicated depths, let's average out the ages for those depths
age_model = age_model.sort_index().dropna()
age_model = pcm.average_duplicated(age_model)
print(age_model)

# %%
# Define the new depths to interpolate/resample on to
new_depths = np.arange(300.0, 650.0, step=10.0)

# %%
# Do the resampling with a selection of methods
linear = pam.resample_linear(age_model, new_depths)
cubic = pam.resample_cubic(age_model, new_depths)
spline = pam.resample_spline(age_model, new_depths)
loess = pam.resample_loess(age_model, new_depths, smoothing_factor=0.4)
lowess = pam.resample_lowess(age_model, new_depths, smoothing_factor=0.4)

# %%
# Compare the original age model with the resampled data
fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=age_model.values, y=age_model.index, mode="lines+markers", name="original"
    )
)
fig.add_trace(
    go.Scatter(
        x=linear.values, y=linear.index, mode="lines+markers", name="Linear resample"
    )
)
fig.add_trace(
    go.Scatter(
        x=cubic.values, y=cubic.index, mode="lines+markers", name="Cubic resample"
    )
)
fig.add_trace(
    go.Scatter(
        x=spline.values, y=spline.index, mode="lines+markers", name="Spline resample"
    )
)
fig.add_trace(
    go.Scatter(
        x=loess.values, y=loess.index, mode="lines+markers", name="LOESS resample"
    )
)
fig.add_trace(
    go.Scatter(
        x=lowess.values, y=lowess.index, mode="lines+markers", name="LOWESS resample"
    )
)
fig.update_yaxes(autorange="reversed")
fig.update_layout(width=700, height=1000, margin=go.layout.Margin(l=0, r=0, t=40, b=20))
fig.update_layout(
    title="Age model resampling", xaxis_title="Age (Ma)", yaxis_title="Depth (m)"
)
plotly.io.show(fig)
