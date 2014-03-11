#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = """Read docs from GitHub_

.. _GitHub: https://github.com/kimmobrunfeldt/nap
"""

setup(
    name='nap',
    version='0.1.0',
    description='Clean way to request HTTP API resources',
    long_description=readme,
    author='Kimmo Brunfeldt',
    author_email='kimmobrunfeldt@gmail.com',
    url='https://github.com/kimmobrunfeldt/nap',
    packages=[
        'nap',
    ],
    package_dir={'nap': 'nap'},
    include_package_data=True,
    install_requires=[
    ],
    license='MIT',
    zip_safe=False,
    keywords='nap',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
)