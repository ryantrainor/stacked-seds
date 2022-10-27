Installation
============

Requirements
------------

* Python >= 3.8
* NumPy >= 1.20.0
* SciPy >= 1.7.0
* Matplotlib >= 3.5.0
* Astropy >= 5.0.0
* PyYAML >= 6.0
* Photutils >= 1.5.0

Install from PyPI
-----------------

.. code-block:: bash

   pip install stacked-seds

Install from Source
-------------------

.. code-block:: bash

   git clone https://github.com/ryantrainor/stacked-seds.git
   cd stacked-seds
   pip install -e .

Development Installation
------------------------

.. code-block:: bash

   git clone https://github.com/ryantrainor/stacked-seds.git
   cd stacked-seds
   pip install -e ".[dev]"

   # Run tests
   make test

   # Format code
   make format

   # Run all checks
   make check
