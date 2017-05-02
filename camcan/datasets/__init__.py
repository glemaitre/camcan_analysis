"""
The :mod:`camcan.datasets` module includes utilities to load datasets.
"""
from .camcan import load_camcan_rest
from .camcan import load_camcan_timeseries_rest
from .camcan import load_camcan_connectivity_rest
from .camcan import load_camcan_contrast_maps

__all__ = ['load_camcan_rest',
           'load_camcan_timeseries_rest',
           'load_camcan_connectivity_rest',
           'load_camcan_contrast_maps']
