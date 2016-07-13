#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


readme = """Read docs from GitHub_

.. _GitHub: https://github.com/kimmobrunfeldt/nap
"""

setup(
    name='nap',
    version='2.0.0-dev',
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
    install_requires=[
        'requests>=2.2.1,<3.0.0'
    ],
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
