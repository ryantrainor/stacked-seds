Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_,
and this project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

[Unreleased]
------------

Added
~~~~~
- Professional documentation structure
- ReadTheDocs integration
- Comprehensive tutorial and FAQ
- Contributing guidelines

[1.0.0] - 2025-01-XX
---------------------

Added
~~~~~
- Initial release of Stacked SEDs package
- Galaxy image stacking with trimmed mean statistics
- Radial photometry with background subtraction
- Error propagation using Median Absolute Deviation
- Command-line tools: ``sed-stack`` and ``sed-photom``
- Publication-ready plotting functionality
- Comprehensive test suite with pytest
- Example workflow with dummy data
- YAML-based configuration system
- Support for DS9 region files
- Multi-filter batch processing
- Automated CI/CD pipeline
- Documentation with Sphinx

Core Modules
~~~~~~~~~~~~
- ``stacking.py``: Image stacking and stamp creation
- ``photometry.py``: Radial profile analysis
- ``plotting.py``: Publication-ready plot generation
- ``utils.py``: Configuration and utility functions

Features
~~~~~~~~
- Robust outlier rejection during stacking
- Automatic coordinate transformation from WCS
- Configurable stamp sizes and trimming parameters
- Background fitting with polynomial models
- Error bars based on robust statistics
- Multi-panel comparison plots
- Extensible configuration system
