from setuptools import find_packages, setup
import re

from sys import version_info

class NotSupportedException(BaseException): pass

if version_info.major >= 3:
    raise NotSupportedException("Only Python 2.x Supported")

setup(
    name='dyck',
    description='Meta-grammar utilities for multi-dimensional Dyck languages.',
    entry_points = { "console_scripts": ['dyck = dyck.dyck:main'] },
    version = '0.2.0',
    author='Orestis Melkonian, Konstantinos Kogkalidis',
    author_email='melkon.or@gmail.com, konstantinos@riseup.net',
    url='http://github.com/omelkonian/dyck',
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    python_requires='<3',
    install_requires=[
        'numpy==1.14.0',
    ],
)
