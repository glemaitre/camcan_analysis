import argparse

from camcan import datasets

parser = argparse.ArgumentParser()
parser.add_argument('--contrast_name', type=str, default='.*')
parser.add_argument('--statistic_type', type=str, default='z_score')
parser.add_argument('--data_dir', type=str,
                    default=datasets.camcan.CAMCAN_DRAGO_STORE_CONTRASTS)
parser.add_argument('--patients_excluded', type=str, default=None)
parser.add_argument('--mask_file', type=str, default=None)

args = parser.parse_args()
kwargs = dict(vars(args))
kwargs.pop('contrast_name')

for masked in datasets.iterate_masked_contrast_maps(args.contrast_name,
                                                    **kwargs):
    print(masked[0].contrast_name.iloc[0])
