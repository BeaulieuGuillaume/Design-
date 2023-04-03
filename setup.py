# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 14:34:29 2022

@author: beaulieu
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="GB_Design",  # Replace with your own username
    version="0.1",
    author="Guillaume Beaulieu",
    author_email="guillaume.beaulieu@epfl.ch",
    description="Python module for GDS drawings",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)
