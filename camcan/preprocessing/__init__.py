"""
The :mod:`camcan.preprocessing` module includes methods to extract time series.
"""
from .temporal_series import extract_timeseries
from .connectivity import extract_connectivity

__all__ = ['extract_timeseries',
           'extract_connectivity']
