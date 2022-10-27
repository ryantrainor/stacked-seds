#!/usr/bin/env python
"""
Setup script for SED Project: Galaxy Stacking and Photometry
"""

from setuptools import setup, find_packages
import os


# Read README for long description
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()


# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [
            line.strip() for line in fh if line.strip() and not line.startswith("#")
        ]


# Get version from package
def get_version():
    version_file = os.path.join("stacked_seds", "__init__.py")
    with open(version_file, "r", encoding="utf-8") as fh:
        for line in fh:
            if line.startswith("__version__"):
                return line.split("=")[1].strip().strip('"').strip("'")
    return "0.1.0"


setup(
    name="stacked-seds",
    version=get_version(),
    author="O. Abraham, C. Chapman, E. Garcia, R. Trainor",
    author_email="ryan.trainor@fandm.edu",
    description="A Python package to stack faint galaxy images and prepare them for SED analysis",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/ryantrainor/stacked-seds",
    project_urls={
        "Bug Tracker": "https://github.com/ryantrainor/stacked-seds/issues",
        "Documentation": "https://github.com/ryantrainor/stacked-seds#readme",
        "Source Code": "https://github.com/ryantrainor/stacked-seds",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Astronomy",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "black>=22.0",
            "flake8>=4.0",
            "pytest>=6.0",
            "pytest-cov>=3.0",
            "pre-commit>=2.0",
        ],
        "docs": [
            "sphinx>=4.0",
            "sphinx-rtd-theme>=1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "sed-stack=stacked_seds.scripts.run_stacking:main",
            "sed-photom=stacked_seds.scripts.run_photometry:main",
        ],
    },
    include_package_data=True,
    package_data={
        "stacked_seds": [
            "config/params.yml",
        ],
    },
    keywords=[
        "astronomy",
        "astrophysics",
        "galaxy",
        "photometry",
        "sed",
        "stacking",
        "image-processing",
    ],
    zip_safe=False,
)
