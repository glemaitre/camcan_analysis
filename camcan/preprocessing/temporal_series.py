"""Extract temporal series from Nifti images"""

import numpy as np

from nilearn.datasets import fetch_atlas_basc_multiscale_2015

from sklearn.externals.joblib import Parallel, delayed

from ..utils import make_masker_from_atlas


def _transform_one_func(masker, func, confounds):
    """Private function to make parallel the extraction of times series."""

    return masker.transform(func, confounds=confounds)


def extract_timeseries(funcs,
                       atlas=fetch_atlas_basc_multiscale_2015().scale064,
                       confounds=None,
                       memory=None,
                       memory_level=1,
                       n_jobs=1):
    """Extract time series for a list of functional volume.

    Parameters
    ----------
    funcs : list of str,
        A list of path of Nifti volumes.

    atlas : str or 3D/4D Niimg-like object, (default=BASC64)
        The atlas to use to create the masker. If string, it should corresponds
        to the path of a Nifti image.

    confounds : list of str,
        A list of path containing the confounds.

    memory : instance of joblib.Memory or string, (default=None)
        Used to cache the masking process. By default, no caching is done. If a
        string is given, it is the path to the caching directory.

    memory_level : integer, optional (default=1)
        Rough estimator of the amount of memory used by caching. Higher value
        means more memory for caching.

    n_jobs : integer, optional (default=1)
        Used to process several patients in parallel.
        If -1, then the number of jobs is set to the number of
        cores.

    """

    masker = make_masker_from_atlas(atlas, memory=memory,
                                    memory_level=memory_level)
    masker.fit()

    if confounds is not None:
        confounds_ = [np.loadtxt(filename) for filename in confounds]
    else:
        confounds_ = [None] * len(funcs)

    time_series = Parallel(n_jobs=n_jobs, verbose=1)(delayed(
        _transform_one_func)(masker, f, c) for f, c in zip(funcs, confounds_))

    return time_series
