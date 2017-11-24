#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Define the setup options."""

try:
    import distribute_setup
    distribute_setup.use_setuptools()
except:
    pass

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

import os
import re


with open(os.path.join(os.path.dirname(__file__), 'openfalconclient', '__init__.py')) as f:
    version = re.search("__version__ = '([^']+)'", f.read()).group(1)

with open('README.txt', 'r') as f:
    readme = f.read()


setup(
    name='openfalconclient',
    version=version,
    description="open-falcon client",
    long_description=readme,
    url='https://github.com/willhope/open-falcon-api-python-cleint.git',
    license='MIT License',
    author = 'zengwh',
    author_email = 'zengwh513@163.com',
    packages=find_packages(exclude=['tests']),
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ),
)
