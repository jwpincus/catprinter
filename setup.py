#!/usr/bin/env python3
"""
Setup script for catprinter package
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="catprinter",
    version="1.0.0",
    author="Jack Pincus",
    description="Command line utilities for printing to cat thermal printers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jackpincus/catprinter",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "catprint-image=catprinter.cli:main_image",
            "catprint-text=catprinter.cli:main_text",
            "catprint=catprinter.cli:main_image",  # Alias for image printing
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
