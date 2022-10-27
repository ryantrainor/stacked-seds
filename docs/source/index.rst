Stacked SEDs Documentation
==========================

.. image:: https://github.com/ryantrainor/stacked-seds/workflows/CI/CD%20Pipeline/badge.svg
   :target: https://github.com/ryantrainor/stacked-seds/actions
   :alt: CI/CD Pipeline

.. image:: https://badge.fury.io/py/stacked-seds.svg
   :target: https://badge.fury.io/py/stacked-seds
   :alt: PyPI version

.. image:: https://img.shields.io/badge/python-3.8+-blue.svg
   :target: https://www.python.org/downloads/
   :alt: Python 3.8+

**Stacked SEDs** is a Python package for stacking faint galaxy images from multiple broadband filters and preparing them for Spectral Energy Distribution (SED) analysis.

Key Features
------------

* **Galaxy Image Stacking**: Robust stacking of hundreds of faint galaxy cutouts using trimmed mean statistics
* **Error Propagation**: Automatic calculation of uncertainty maps using Median Absolute Deviation (MAD)
* **Radial Photometry**: Azimuthally averaged surface brightness profiles with background subtraction
* **Publication-Ready Plots**: Automated generation of multi-filter comparison plots
* **Command-Line Tools**: Simple ``sed-stack`` and ``sed-photom`` commands for easy workflow execution

Quick Start
-----------

Installation
~~~~~~~~~~~~

.. code-block:: bash

   pip install stacked-seds

Basic Usage
~~~~~~~~~~~

.. code-block:: bash

   # 1. Create configuration file
   cp config/params.yml my_config.yml

   # 2. Edit my_config.yml with your data paths

   # 3. Run stacking workflow
   sed-stack my_config.yml
   sed-photom my_config.yml

Python API
~~~~~~~~~~

.. code-block:: python

   from stacked_seds import stacking, photometry

   # Load and stack galaxy images
   pixel_coords = stacking.get_galaxy_pixel_coords("image.fits", "galaxies.reg")
   stamps = stacking.create_stamps(image_data, wcs_obj, pixel_coords)
   stacked_image, error_map = stacking.stack_images(stamps)

   # Perform radial photometry
   radii, profile, errors = photometry.get_radial_profile(stacked_image, center)

User Guide
----------

.. toctree::
   :maxdepth: 2

   installation
   tutorial
   configuration
   examples
   faq

API Reference
-------------

.. toctree::
   :maxdepth: 2

   api/stacking
   api/photometry
   api/plotting
   api/utils

Development
-----------

.. toctree::
   :maxdepth: 1

   contributing
   changelog
   license

Community
---------

* **GitHub Repository**: https://github.com/ryantrainor/stacked-seds
* **Issue Tracker**: https://github.com/ryantrainor/stacked-seds/issues
* **Discussions**: https://github.com/ryantrainor/stacked-seds/discussions

Citation
--------

If you use this software in your research, please cite:

.. code-block:: bibtex

   @software{stacked_seds,
     title={Stacked SEDs: Galaxy Image Stacking and Photometry},
     author={Abraham, O. and Chapman, C. and Garcia, E. and Trainor, R.},
     year={2025},
     url={https://github.com/ryantrainor/stacked-seds},
     doi={10.5281/zenodo.XXXXXX}
   }

Indices and Tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
