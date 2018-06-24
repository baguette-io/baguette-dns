#-*- coding:utf-8 -*-
"""
Setup for baguette-dns package.
"""
from setuptools import find_packages, setup

setup(
    name='baguette-dns',
    version='0.1',
    url='baguette.io',
    author_email='dev@baguette.io',
    packages=find_packages(),
    platforms=[
        'Linux/UNIX',
        'MacOS',
        'Windows'
    ],
    install_requires=[
        'baguette-messaging',
        'baguette-utils',
    ],
    extras_require={
        'testing': [
            'baguette-messaging[testing]',
        ],
        'doc': [
            'Sphinx',
        ],
    },
    package_data={
        'levain.tests': ['farine.ini', 'pytest.ini'],
    },
)
