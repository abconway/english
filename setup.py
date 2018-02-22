from setuptools import setup, find_packages
import os
import sys


__version__ = '0.0.1'
__requirements__ = [
    'Click',
    'requests',
]


setup(
    name='english',
    version=__version__,
    py_modules=['main'],
    install_requires=__requirements__,
    entry_points='''
        [console_scripts]
        english=main:cli
    ''',
)
