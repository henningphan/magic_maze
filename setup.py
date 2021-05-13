#!/usr/bin/env python
from setuptools import setup, find_packages

print(find_packages())
setup(
    name='magicmaze',
    version='0.1.0',
    packages=find_packages(include=".")
)
