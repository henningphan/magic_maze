#!/usr/bin/env python
from setuptools import setup, find_packages

print(find_packages())
setup(
    name='magic_maze',
    version='0.1.0',
    packages=find_packages(include=".")
)
