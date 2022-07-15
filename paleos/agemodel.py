"""
Module to help resample or interpolate age models to new depths

Age models are assumed to be a pandas Series object with depth as index and age
as value.
"""
from loguru import logger
import numpy as np
import pandas as pd

import paleos.interpolate as pin


def add_point(
    age_model: pd.Series, depth: float = 0, age: float = 0, sort_result: bool = True
) -> pd.Series:
    """Add a point to an age model

    Args:
        age_model (pd.Series): The age model
        depth (float): The depth for the point. Defaults to 0.
        age (float): The age for the point. Defaults to 0.
        sort_result (bool, optional): Sort the result. Defaults to True.

    Returns:
        pd.Series: Age model with point added
    """
    new_point = pd.Series(data=[age], index=[depth], dtype=age_model.dtype)
    if sort_result:
        return pd.concat((age_model, new_point)).sort_index()
    return pd.concat((age_model, new_point))


def clip_age_reversals(age_model: pd.Series) -> pd.Series:
    """
    Remove reversals in age models

    Args:
        age_model (pd.Series): The age model

    Returns:
        pd.Series: The age model with age reverals removed
    """
    return age_model.cummax()


def resample_linear(age_model: pd.Series, depths: np.ndarray) -> pd.Series:
    """Resample age model onto new depths using linear interpolation

    Args:
        age_model (pd.Series): Age model
        depths (np.ndarray): Depths for which to calculate out ages

    Returns:
        pd.Series: Ages for depths
    """
    return pin.linear_interpolate(age_model, depths)


def resample_cubic(age_model: pd.Series, depths: np.ndarray) -> pd.Series:
    """Resample age model onto new depths using cubic interpolation

    Args:
        age_model (pd.Series): Age model
        depths (np.ndarray): Depths for which to calculate out ages

    Returns:
        pd.Series: Ages for depths
    """
    return pin.cubic_interpolate(age_model, depths)


def resample_spline(age_model: pd.Series, depths: np.ndarray):
    """Resample age model onto new depths using spline interpolation

    Args:
        age_model (pd.Series): Age model
        depths (np.ndarray): Depths for which to calculate out ages

    Returns:
        pd.Series: Ages for depths
    """
    return pin.spline_interpolate(age_model, depths)


def resample_loess(
    age_model: pd.Series, depths: np.ndarray, smoothing_factor: float = 0.33
) -> pd.Series:
    """Resample age model onto new depths using local linear regression

    Args:
        age_model (pd.Series): Age model
        depths (np.ndarray): Depths for which to calculate out ages
        smoothing_factor (float, optional): Smoothing factor to use. Defaults to 0.33.

    Returns:
        pd.Series: Ages for depths
    """
    return pin.loess_ext_interpolate(age_model, depths, smoothing_factor)


def resample_lowess(
    age_model: pd.Series, depths: np.ndarray, smoothing_factor: float = 0.33
):
    """Resample age model onto new depths using local weighted linear regression

    Args:
        age_model (pd.Series): Age model
        depths (np.ndarray): Depths for which to calculate out ages
        smoothing_factor (float, optional): Smoothing factor to use. Defaults to 0.33.

    Returns:
        pd.Series: Ages for depths
    """
    return pin.lowess_sm_interpolate(age_model, depths, smoothing_factor)
