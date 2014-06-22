#!/usr/bin/env python

from pip.req import parse_requirements

# parse_requirements() returns generator of pip.req.InstallRequirement objects

install_reqs = parse_requirements('requirements.txt')

# reqs is a list of requirement
# e.g. ['django==1.5.1', 'mezzanine==1.4.6']
reqs = [str(ir.req) for ir in install_reqs]

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


readme = """Read docs from GitHub_

.. _GitHub: https://github.com/kimmobrunfeldt/nap
"""

setup(
    name='nap',
    version='1.0.1-dev',
    description='Convenient way to request HTTP APIs',
    long_description=readme,
    author='Kimmo Brunfeldt',
    author_email='kimmobrunfeldt@gmail.com',
    url='https://github.com/kimmobrunfeldt/nap',
    packages=[
        'nap',
    ],
    package_dir={'nap': 'nap'},
    include_package_data=True,
    install_requires=reqs,
    license='MIT',
    zip_safe=False,
    keywords='nap rest requests http',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
)
