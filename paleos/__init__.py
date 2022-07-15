"""
Paleos is a handy set of python utilities for paleoclimate/paleocean analysis.

The heavy lifting in paleos is done by the standard python scientific stack
including numpy, scipy and pandas. The main objective of paleos is to be a
simpler entry point for those who are coming from the domain first and are 
less experienced with programming.
"""
from importlib.metadata import version, PackageNotFoundError

__name__ = "paleos"
try:
    __version__ = version(__name__)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"