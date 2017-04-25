"""
Loader for the Cam-CAN data set.
"""

import re
import glob
import warnings

from os.path import join, isdir, relpath, dirname, isfile

import numpy as np
import pandas as pd

from sklearn.externals import six
from sklearn.datasets.base import Bunch

# root path
CAMCAN_DRAGO_STORE = '/storage/data/camcan/camcan_preprocess'

# path for anatomical and functional images - BIDS format
FUNCTIONAL_PATH = 'func'
ANATOMICAL_PATH = 'anat'

# pattern of the different files of interests
FUNC_PATTERN = 'wrsub-*.nii.gz'
MVT_PATTERN = 'rp*.txt'
ANAT_PATTERN = 'wsub-*.nii.gz'
TISSUES_PATTERN = ['mwc1sub-*.nii.gz', 'mwc2sub-*.nii.gz', 'mwc3sub-*.nii.gz']


def _patients_id_from_csv(csv_file):
    """Private function to extract the patient IDs which need to be excluded.

    Parameters
    ----------
    csv_file : str,
        Filename of the CSV file from which we will extract the information.

    Returns
    -------
    patients_excluded_ : tuple of str,
        The validated list of patient IDs to exclude.

    """
    if isfile(csv_file):
        df = pd.read_csv(csv_file)
        # go line by line and check the validity for each subject
        return tuple([df.iloc[i, 0] for i in range(df.shape[0])
                      if not np.all(df.iloc[i, 1:])])
    else:
        raise ValueError('{}: File not found.'.format(csv_file))


def _check_patients_excluded(patients_excluded):
    """Private function to validate ``patients_excluded``.

    Parameters
    ----------
    patients_excluded : str, tuple of str or None, optional (default=None)
        - If a string, corresponds to the path of a csv file.
        - If a tuple of strings, contains the ID of the patient to be
        excluded. The string provided should follow the BIDS standard (e.g.,
        'sub-******').

    Returns
    -------
    patients_excluded_ : tuple of str,
        The validated list of patient IDs to exclude.

    """
    if patients_excluded is None:
        patients_excluded_ = tuple([])
    elif isinstance(patients_excluded, tuple):
        # pattern imposed by BIDS standard
        pattern = re.compile('sub-*')
        # check that all string in the tuple follow the correct pattern
        if all(map(lambda patient_id:
                   True if pattern.match(patient_id) is not None else False,
               patients_excluded)):
            patients_excluded_ = patients_excluded
        else:
            raise ValueError("All patient IDs to be excluded should follow"
                             " the pattern 'sub-'.")
    elif isinstance(patients_excluded, six.string_types):
        if patients_excluded.endswith('.csv'):
            patients_excluded_ = _patients_id_from_csv(patients_excluded)
        else:
            raise ValueError('If a string is provided, a csv file needs'
                             ' to be given.')
    else:
        raise ValueError("'patients_excluded' should be a tuple. Got {}"
                         " instead.".format(type(patients_excluded)))

    return patients_excluded_


def load_camcan_rest(data_dir=CAMCAN_DRAGO_STORE, patients_excluded=None):
    """Path loader for the Cam-CAN resting-state fMRI data.

    This loader returns a Bunch object containing the paths to the data of
    interests. The data which can be loaded are:

    - Functional images;
    - Anatomical images;
    - Motion correction;
    - Tissues segmentation;
    - Patient ID;
    - Scores.

    See the description of the data to get all the information.

    Parameters
    ----------
    data_dir : str,
        Root directory containing the root data.

    patients_excluded : str, tuple of str or None, optional (default=None)
        - If a string, corresponds to the path of a csv file.
        - If a tuple of strings, contains the ID of the patient to be
        excluded. The string provided should follow the BIDS standard (e.g.,
        'sub-******').

    Returns
    -------
    data : Bunch,
        Dictionary-like object. The interesting attributes are:

        - 'func', the path to the functional images;
        - 'anat', the path to the anatomical images;
        - 'motion', the path of the file containing the motion parameters
        from the rigid registration performed on the functional images;
        - 'tissues', the path to the images containing the segmentation of the
        brain tissues from the anatomical images;
        - 'subject_id', the ID of the patient;
        - 'scores', a dictionary containing the different scores;
        - 'DESCR', the description of the full dataset.

    """
    patients_excluded_ = _check_patients_excluded(patients_excluded)

    if not isdir(data_dir):
        raise ValueError("The directory '{}' does not exist.".format(data_dir))

    subjects_dir = sorted(glob.glob(join(data_dir, 'sub-*')))
    dir_idx_kept = [dir_idx for dir_idx in range(len(subjects_dir))
                    if relpath(subjects_dir[dir_idx], data_dir)
                    not in patients_excluded_]
    subjects_dir = [subjects_dir[i] for i in dir_idx_kept]

    module_path = dirname(__file__)
    with open(join(module_path, 'descr', 'camcan.rst')) as rst_file:
        fdescr = rst_file.read()

    dataset = {'func': [],
               'motion': [],
               'anat': [],
               'tissues': [],
               'subject_id': [],
               'DESCR': fdescr}

    for subject_dir in subjects_dir:
        dataset['subject_id'].append(relpath(subject_dir, data_dir))
        # Discover one after the other:
        # - functional images;
        # - motion parameters;
        # - anatomical images;
        # - tissues segmented.
        for p, f, k in zip([FUNCTIONAL_PATH] * 2 + [ANATOMICAL_PATH] * 4,
                           [FUNC_PATTERN, MVT_PATTERN, ANAT_PATTERN] +
                           TISSUES_PATTERN,
                           ['func', 'motion', 'anat'] + ['tissues'] * 3):

            nifti_path = glob.glob(join(subject_dir, p, f))
            if not nifti_path:
                warnings.warn("No file match the regular expression {} for"
                              " the subject ID {}".format(
                                  join(p, f), relpath(subject_dir, data_dir)))
                dataset[k].append(None)
            else:
                dataset[k].append(nifti_path[0])

    return Bunch(**dataset)
