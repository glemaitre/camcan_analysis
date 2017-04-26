"""
This script aimed at extracting several time series using the Cam-CAN
results with different atlases and dump the results somewhere.
"""

import os

from camcan.datasets import load_camcan_rest
from camcan.preprocessing import extract_timeseries

from nilearn.datasets import (fetch_atlas_basc_multiscale_2015,
                              fetch_atlas_msdl)

from sklearn.externals import joblib

# path to the Cam-CAN data set
CAMCAN_PREPROCESSED = '/storage/data/camcan/camcan_preproc'
CAMCAN_PATIENTS_EXCLUDED = None
CAMCAN_TIMESERIES = '/storage/data/camcan/camcan_timeseries'
# path to the atlases
ATLASES = [fetch_atlas_basc_multiscale_2015.scale064,
           fetch_atlas_basc_multiscale_2015.scale122,
           fetch_atlas_msdl.maps]
ATLASES_DESCR = ['basc064', 'basc122', 'msdl']
# path for the caching
CACHE_TIMESERIES = '/storage/data/camcan/cache/timeseries'

N_JOBS = 20

# create the path to dump the results
for atlas_descr in ATLASES_DESCR:
    path_results = os.path.join(CAMCAN_TIMESERIES, atlas_descr)
    if not os.path.exists(path_results):
        os.makedirs(path_results)

dataset = load_camcan_rest(data_dir=CAMCAN_PREPROCESSED,
                           patients_excluded=CAMCAN_PATIENTS_EXCLUDED)
for atlas, atlas_descr in (ATLASES, ATLASES_DESCR):
    # with and without confounds
    for confounds in [None, dataset.motion]:
        time_series = extract_timeseries(dataset.func,
                                         atlas=atlas,
                                         confounds=confounds,
                                         memory=CACHE_TIMESERIES,
                                         memory_level=2,
                                         n_jobs=N_JOBS)

        if confounds is None:
            filename = os.path.join(CAMCAN_TIMESERIES, atlas_descr,
                                    'time_series.pkl')
        else:
            filename = os.path.join(CAMCAN_TIMESERIES, atlas_descr,
                                    'time_series_confounds.pkl')

        joblib.dump(time_series, filename)
