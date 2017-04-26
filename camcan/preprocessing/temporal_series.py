"""Extract temporal series from Nifti images"""

import numpy as np

from nilearn.datasets import fetch_atlas_basc_multiscale_2015

from ..utils import make_masker_from_atlas


def extract_timeseries(func,
                       atlas=fetch_atlas_basc_multiscale_2015().scale064,
                       confounds=None,
                       memory=None,
                       memory_level=1):
    """Extract time series for a list of functional volume.

    Parameters
    ----------
    func : str,
        Path of Nifti volumes.

    atlas : str or 3D/4D Niimg-like object, (default=BASC64)
        The atlas to use to create the masker. If string, it should corresponds
        to the path of a Nifti image.

    confounds : str,
        Path containing the confounds.

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
        confounds_ = np.loadtxt(confounds)
    else:
        confounds_ = None

    return masker.transform(func, confounds=confounds_)
