"""
SED Project: Galaxy Stacking and Photometry

A Python package to stack faint galaxy images from multiple broadband filters
and prepare them for Spectral Energy Distribution (SED) analysis.
"""

__version__ = "1.0.0"
__author__ = "O. Abraham, C. Chapman, E. Garcia, R. Trainor"
__email__ = "ryan.trainor@fandm.edu"

# Import main modules for easy access
from . import stacking
from . import photometry
from . import plotting
from . import utils

__all__ = ["stacking", "photometry", "plotting", "utils"]
