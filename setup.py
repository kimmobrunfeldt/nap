"""Nap provides simple and easy way to request HTTP API resources. Stop coding needless code."""
#!/usr/bin/env python

import os
from distutils.core import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='nap',
    version='0.1.0',
    description=__doc__,
    long_description=read('README.md'),
    license='MIT',
    install_requires=[
        "requests"
    ],
    url='https://github.com/kimmobrunfeldt/nap',
    author='Kimmo Brunfeldt',
    author_email='kimmobrunfeldt+nap@gmail.com',
    packages=['nap']
)
