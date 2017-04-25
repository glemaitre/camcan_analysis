#!/usr/bin/env python
"""Package to play with Cam-CAN data."""

import codecs
import os

from setuptools import find_packages, setup

# Make sources available using relative paths from this file's directory.
os.chdir(os.path.dirname(os.path.abspath(__file__)))

DISTNAME = 'camcan'
DESCRIPTION = 'Package to play with Cam-CAN data.'
with codecs.open('README.rst', encoding='utf-8-sig') as f:
    LONG_DESCRIPTION = f.read()
MAINTAINER = 'Some people'
MAINTAINER_EMAIL = ('some.people@example.com')
URL = 'https://github.com/mrahim/camcan_analysis'
LICENSE = 'new BSD'
DOWNLOAD_URL = 'https://github.com/mrahim/camcan_analysis'
VERSION = '0.0.1dev'


def configuration(parent_package='', top_path=None):
    if os.path.exists('MANIFEST'):
        os.remove('MANIFEST')

    from numpy.distutils.misc_util import Configuration
    config = Configuration(None, parent_package, top_path)

    config.add_subpackage('camcan')

    return config


if __name__ == "__main__":
    setup(configuration=configuration,
          name=DISTNAME,
          maintainer=MAINTAINER,
          maintainer_email=MAINTAINER_EMAIL,
          description=DESCRIPTION,
          license=LICENSE,
          url=URL,
          version=VERSION,
          download_url=DOWNLOAD_URL,
          long_description=LONG_DESCRIPTION,
          zip_safe=False,  # the package can run out of an .egg file
          classifiers=[
              'Intended Audience :: Science/Research',
              'Intended Audience :: Developers',
              'License :: OSI Approved',
              'Programming Language :: Python',
              'Topic :: Software Development',
              'Topic :: Scientific/Engineering',
              'Operating System :: Microsoft :: Windows',
              'Operating System :: POSIX',
              'Operating System :: Unix',
              'Operating System :: MacOS',
              'Programming Language :: Python :: 2.7',
              'Programming Language :: Python :: 3.5',
              'Programming Language :: Python :: 3.6'
          ],
          packages=find_packages(),
          install_requires=['scipy>=0.9',
                            'numpy>=1.6.1',
                            'scikit-learn>=0.14.1',
                            'nibabel>=1.2.0',
                            'nilearn>=0.3.0'])
