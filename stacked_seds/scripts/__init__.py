"""
Command-line scripts for Stacked SEDs.
"""

from .run_stacking import main as stack_main
from .run_photometry import main as photom_main

__all__ = ["stack_main", "photom_main"]
