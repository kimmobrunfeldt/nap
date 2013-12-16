"""Nap provides simple and easy way to request HTTP API resources. Stop coding needless code."""
#!/usr/bin/env python

from distutils.core import setup

setup(
    name='Nap',
    version='0.1.0',
    description=__doc__,
    license='MIT',
    install_requires=[
        "requests"
    ],
    url='https://github.com/kimmobrunfeldt/nap',
    author='Kimmo Brunfeldt',
    packages=['nap']
)
