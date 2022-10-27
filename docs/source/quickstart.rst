Quick Start Guide
=================

This guide shows how to run the full workflow on your own data.

1. Create Your Configuration File
----------------------------------

Copy the default configuration and customize it for your data:

.. code-block:: bash

   cp config/params.yml my_analysis_config.yml

Edit the configuration file to point to your FITS files, region files, and desired output directories.

2. Run the Workflow
-------------------

Execute the command-line tools in sequence:

Step 1: Stack the Images
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   sed-stack my_analysis_config.yml

This reads your raw FITS files and produces stacked ``*_NEW.fits`` images.

Step 2: Perform Photometry and Plotting
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   sed-photom my_analysis_config.yml

This analyzes the stacked images and generates a summary plot.

3. Run the Example
------------------

To verify your installation:

.. code-block:: bash

   cd examples
   python run_workflow_example.py

This creates dummy data and runs the full stacking workflow to test that everything works correctly.

Command Line Interface
----------------------

The package provides two main command-line tools:

``sed-stack``
~~~~~~~~~~~~~

Stacks galaxy images based on a configuration file.

.. code-block:: bash

   sed-stack [config_file.yml]

``sed-photom``
~~~~~~~~~~~~~~

Runs photometry and generates plots from stacked images.

.. code-block:: bash

   sed-photom [config_file.yml]
