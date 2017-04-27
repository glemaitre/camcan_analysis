from os.path import join, split

from sklearn.utils.testing import (assert_equal, assert_true,
                                   assert_array_equal,
                                   assert_raises_regex)

from camcan.datasets.camcan import _validate_patients_excluded
from camcan.datasets.camcan import _exclude_patients
from camcan.datasets.camcan import _load_camcan_scores


def test_validate_patients_excluded_errors():
    assert_raises_regex(ValueError, 'should be a tuple.',
                        _validate_patients_excluded, 0)
    assert_raises_regex(ValueError, "follow the pattern 'sub-'",
                        _validate_patients_excluded, tuple('random'))
    assert_raises_regex(ValueError, "a csv file is required",
                        _validate_patients_excluded, 'file.rnd')
    assert_raises_regex(ValueError, "File not found.",
                        _validate_patients_excluded, "file.csv")


def test_validate_patients_excluded():
    patients_excluded = _validate_patients_excluded(None)
    assert_equal(patients_excluded, tuple([]))

    patients_excluded = _validate_patients_excluded(('sub-0', 'sub-1'))
    assert_equal(patients_excluded, ('sub-0', 'sub-1'))

    current_dir = split(__file__)[0]
    filename = join(current_dir, "data", "patients_selection.csv")
    patients_excluded = _validate_patients_excluded(filename)
    assert_equal(patients_excluded, ('sub-0', 'sub-2', 'sub-3'))


def test_exclude_patients():
    current_dir = split(__file__)[0]
    patients_dir = _exclude_patients(join(current_dir, 'data'), tuple([]))
    assert_equal(len(patients_dir), 2)
    for patient_idx, patient_dir in enumerate(patients_dir):
        assert_true('data/sub-' + str(patient_idx) in patient_dir)

    patients_dir = _exclude_patients(join(current_dir, 'data'),
                                     tuple(['sub-0']))
    assert_equal(len(patients_dir), 1)
    assert_true('data/sub-1' in patient_dir)


def test_load_camcan_scores_error():
    assert_raises_regex(ValueError, 'does not exist.',
                        _load_camcan_scores, 'file.csv', ['sub-0'])
    current_dir = split(__file__)[0]
    assert_raises_regex(ValueError, 'is not a CSV file.',
                        _load_camcan_scores, join(current_dir, '__init__.py'),
                        ['sub-0'])


def test_load_camcan_scores():
    current_dir = split(__file__)[0]
    filename = join(current_dir, 'data', 'participants_info.csv')
    scores = _load_camcan_scores(filename, ['sub-CC0', 'sub-CC1'])
    assert_array_equal(scores.age, [18, 20])
    assert_array_equal(scores.hand, [-100, 100])
    assert_array_equal(scores.gender_text, ['FEMALE', 'MALE'])
