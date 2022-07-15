"""
This module has a selection of interpolation algorithms. Core samples are
usually irregularly sampled in age, meaning that interpolation of some form is
required to put any age indexed data on regular sampling.

The following techniques are provided here

- linear interpolation via scipy
- cubic interpolation via scipy
- spline interpolation via scipy
- lowess from statsmodels, which is a local least squares with a tricubic 
  weighting. Multiple iterations are performed here for robustness from outliers
- lowess from a custom function using a tricubic weight function
- loess from a custom function using a uniform weight function, meaning local
  least squares without any weighting
"""
from loguru import logger
from typing import Optional, Callable
import math
import numpy as np
import scipy.interpolate as scinterp
import pandas as pd
import statsmodels.api as sm


def tricubic_weights(x):
    """Tricubic weights for external LOWESS"""
    y = np.zeros_like(x)
    idx = (x >= -1) & (x <= 1)
    y[idx] = np.power(1.0 - np.power(np.abs(x[idx]), 3), 3)
    return y


def uniform_weights(x):
    """Uniform weights for external LOESS"""
    return np.ones_like(x)


class Loess(object):
    """Local linear regression
    
    This code was minimally modified from https://github.com/joaofig/pyloess to
    allow support for other weighting functions, in this case uniform weights
    or local linear regression (unweighted). 

    Copyright (c) 2019 João Paulo Figueira

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to 
    deal in the Software without restriction, including without limitation the
    rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
    sell copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in 
    all copies or substantial portions of the Software.
    """

    @staticmethod
    def normalize_array(array):
        min_val = np.min(array)
        max_val = np.max(array)
        return (array - min_val) / (max_val - min_val), min_val, max_val

    def __init__(self, xx, yy, degree=1, weight_fnc: Optional[Callable] = None):
        self.n_xx, self.min_xx, self.max_xx = self.normalize_array(xx)
        self.n_yy, self.min_yy, self.max_yy = self.normalize_array(yy)
        self.degree = degree
        self.weight_fnc = tricubic_weights if weight_fnc is None else weight_fnc

    @staticmethod
    def get_min_range(distances, window):
        min_idx = np.argmin(distances)
        n = len(distances)
        if min_idx == 0:
            return np.arange(0, window)
        if min_idx == n - 1:
            return np.arange(n - window, n)

        min_range = [min_idx]
        while len(min_range) < window:
            i0 = min_range[0]
            i1 = min_range[-1]
            if i0 == 0:
                min_range.append(i1 + 1)
            elif i1 == n - 1:
                min_range.insert(0, i0 - 1)
            elif distances[i0 - 1] < distances[i1 + 1]:
                min_range.insert(0, i0 - 1)
            else:
                min_range.append(i1 + 1)
        return np.array(min_range)

    def get_weights(self, distances, min_range):
        max_distance = np.max(distances[min_range])
        weights = self.weight_fnc(distances[min_range] / max_distance)
        return weights

    def normalize_x(self, value):
        return (value - self.min_xx) / (self.max_xx - self.min_xx)

    def denormalize_y(self, value):
        return value * (self.max_yy - self.min_yy) + self.min_yy

    def estimate(self, x, window, use_matrix=False, degree=1):
        n_x = self.normalize_x(x)
        distances = np.abs(self.n_xx - n_x)
        min_range = self.get_min_range(distances, window)
        weights = self.get_weights(distances, min_range)

        if use_matrix or degree > 1:
            wm = np.multiply(np.eye(window), weights)
            xm = np.ones((window, degree + 1))

            xp = np.array([[math.pow(n_x, p)] for p in range(degree + 1)])
            for i in range(1, degree + 1):
                xm[:, i] = np.power(self.n_xx[min_range], i)

            ym = self.n_yy[min_range]
            xmt_wm = np.transpose(xm) @ wm
            beta = np.linalg.pinv(xmt_wm @ xm) @ xmt_wm @ ym
            y = (beta @ xp)[0]
        else:
            xx = self.n_xx[min_range]
            yy = self.n_yy[min_range]
            sum_weight = np.sum(weights)
            sum_weight_x = np.dot(xx, weights)
            sum_weight_y = np.dot(yy, weights)
            sum_weight_x2 = np.dot(np.multiply(xx, xx), weights)
            sum_weight_xy = np.dot(np.multiply(xx, yy), weights)

            mean_x = sum_weight_x / sum_weight
            mean_y = sum_weight_y / sum_weight

            b = (sum_weight_xy - mean_x * mean_y * sum_weight) / (
                sum_weight_x2 - mean_x * mean_x * sum_weight
            )
            a = mean_y - b * mean_x
            y = a + b * n_x
        return self.denormalize_y(y)


def get_output_index(series: pd.Series, step: float = 0.1) -> np.ndarray:
    """Get output index given the index range in the series

    Args:
        series (pd.Series): pandas series
        step (float, optional): The step to use. Defaults to 0.1.

    Returns:
        np.ndarray: The output index
    """
    min_time = series.index.min()
    max_time = series.index.max()

    start = math.ceil(min_time / step) * step
    end = math.floor(max_time / step) * step
    logger.info(f"New ages from {start} to {end}")
    return np.arange(start, end, step=step)


def linear_interpolate(series: pd.Series, new_idxs: np.ndarray) -> pd.Series:
    """Interpolate values from series to new index using linear interpolation

    Args:
        series (pd.Series): pandas series to interpolate
        new_idxs (np.ndarray): The new index to interpolate to

    Returns:
        pd.Series: Interpolated pandas series
    """
    interp_fnc = scinterp.interp1d(
        series.index.values, series.values, bounds_error=False, fill_value="extrapolate"
    )
    new_values = interp_fnc(new_idxs)
    return pd.Series(data=new_values, index=new_idxs)


def cubic_interpolate(series: pd.Series, new_idxs: np.ndarray) -> pd.Series:
    """Interpolate values from series to new index using cubic interpolation

    Args:
        series (pd.Series): pandas series to interpolate
        new_idxs (np.ndarray): The new index to interpolate to

    Returns:
        pd.Series: Interpolated pandas series
    """
    interp_fnc = scinterp.interp1d(
        series.index.values,
        series.values,
        kind="cubic",
        bounds_error=False,
        fill_value="extrapolate",
    )
    new_values = interp_fnc(new_idxs)
    return pd.Series(data=new_values, index=new_idxs)


def spline_interpolate(
    series: pd.Series, new_idxs: np.ndarray, s: int = 0
) -> pd.Series:
    """Interpolate values from series to new index using spline interpolation.

    With s(moothing) = 0, this should match cubic interpolation

    Args:
        series (pd.Series): pandas series to interpolate
        new_idxs (np.ndarray): The new index to interpolate to

    Returns:
        pd.Series: Interpolated pandas series
    """
    interp_fnc = scinterp.splrep(series.index.values, series.values, s=s)
    new_values = scinterp.splev(new_idxs, interp_fnc, der=0)
    return pd.Series(data=new_values, index=new_idxs)


def lowess_sm_interpolate(
    series: pd.Series,
    new_idxs: np.ndarray,
    smoothing_factor: float,
    iterations: int = 3,
) -> pd.Series:
    """Perform local weighted least squares for interpolation

    This uses statsmodels internally

    Args:
        series (pd.Series): pandas series to interpolate
        new_idxs (np.ndarray): The new index to interpolate to
        smoothing_factor (float): The smoothing factor
        iterations (int, optional): [description]. Number of iterations to help robustness to 3.

    Returns:
        pd.Series: Interpolated pandas series
    """
    n_series = len(series.index)
    n_smooth = smoothing_factor * n_series
    logger.info(
        f"Series size {n_series}, smoothing factor {smoothing_factor}, points = {n_smooth}"
    )

    output = sm.nonparametric.lowess(
        series.values,
        series.index.values,
        frac=smoothing_factor,
        it=iterations,
        xvals=new_idxs,
    )
    return pd.Series(data=output, index=new_idxs)


def lowess_ext_interpolate(
    series: pd.Series,
    new_idxs: np.ndarray,
    smoothing_factor: float,
    use_matrix: bool = True,
    degree: int = 1,
) -> pd.Series:
    """Perform local weighted least squares for interpolation

    This uses custom code internally

    Args:
        series (pd.Series): pandas series to interpolate
        new_idxs (np.ndarray): The new index to interpolate to
        smoothing_factor (float): The smoothing factor
        use_matrix (bool, optional): Use matrix algebra to compute. Defaults to True.
        degree (int, optional): Polynomical degree, 1 means linear fit. Defaults to 1.

    Returns:
        pd.Series: Interpolated pandas series
    """
    n_series = len(series.index)
    n_smooth = int(smoothing_factor * n_series)
    logger.info(
        f"Series size {n_series}, smoothing factor {smoothing_factor}, points = {n_smooth}"
    )

    loess = Loess(series.index.values, series.values, weight_fnc=tricubic_weights)
    output_vals = []
    for age in new_idxs:
        val = loess.estimate(age, window=n_smooth, use_matrix=use_matrix, degree=degree)
        output_vals.append(val)
    return pd.Series(data=output_vals, index=new_idxs)


def loess_ext_interpolate(
    series: pd.Series,
    new_idxs: np.ndarray,
    smoothing_factor: float,
    use_matrix: bool = True,
    degree: int = 1,
) -> pd.Series:
    """Perform local least squares for interpolation

    This uses custom code internally

    Args:
        series (pd.Series): pandas series to interpolate
        new_idxs (np.ndarray): The new index to interpolate to
        smoothing_factor (float): The smoothing factor
        use_matrix (bool, optional): Use matrix algebra to compute. Defaults to True.
        degree (int, optional): Polynomical degree, 1 means linear fit. Defaults to 1.

    Returns:
        pd.Series: Interpolated pandas series
    """
    n_series = len(series.index)
    n_smooth = int(smoothing_factor * n_series)
    logger.info(
        f"Series size {n_series}, smoothing factor {smoothing_factor}, points = {n_smooth}"
    )

    loess = Loess(series.index.values, series.values, weight_fnc=uniform_weights)
    output_vals = []
    for age in new_idxs:
        val = loess.estimate(age, window=n_smooth, use_matrix=use_matrix, degree=degree)
        output_vals.append(val)
    return pd.Series(data=output_vals, index=new_idxs)
