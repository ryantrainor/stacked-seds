Tutorial
========

This tutorial will walk you through the complete workflow of using Stacked SEDs to process galaxy images.

Overview
--------

The Stacked SEDs workflow consists of two main steps:

1. **Image Stacking**: Combine multiple galaxy cutouts into a single high S/N image
2. **Radial Photometry**: Extract surface brightness profiles and generate plots

Prerequisites
-------------

Before starting, you should have:

* FITS images containing your target galaxies
* A DS9 region file marking galaxy positions
* A zeropoints file with magnitude calibrations

Step 1: Configuration
---------------------

Create a configuration file based on the template:

.. code-block:: bash

   cp config/params.yml my_analysis.yml

Edit the configuration file to match your data:

.. code-block:: yaml

   data_directory: "path/to/your/fits/files/"
   output_directory: "path/to/output/"
   plot_directory: "path/to/plots/"
   region_file: "your_galaxies.reg"
   zeropoints_file: "your_zeropoints.txt"

   stacking_params:
     files_to_stack:
       - "image1.fits"
       - "image2.fits"
       - "image3.fits"
     stamp_size: 51
     trim_fraction: 0.1

   photometry_params:
     background_reduction: true
     galaxy_centers:
       image1_NEW.fits: [25.0, 25.0]
       image2_NEW.fits: [25.0, 25.0]
       image3_NEW.fits: [25.0, 25.0]
     bkg_fit_range: [6, -5]
     plot_title: "My Galaxy Radial Profiles"
     output_plot_filename: "my_radial_plot.pdf"

Step 2: Run Image Stacking
---------------------------

Execute the stacking workflow:

.. code-block:: bash

   sed-stack my_analysis.yml

This will:

1. Read galaxy coordinates from your region file
2. Extract cutout stamps around each galaxy
3. Stack the stamps using a robust trimmed mean
4. Save the stacked images as ``*_NEW.fits`` files

Step 3: Run Photometry and Plotting
------------------------------------

Execute the photometry workflow:

.. code-block:: bash

   sed-photom my_analysis.yml

This will:

1. Calculate radial surface brightness profiles for each filter
2. Fit and subtract background levels
3. Generate a publication-ready plot comparing all filters

Understanding the Output
------------------------

After running both steps, you'll have:

**Stacked Images** (``*_NEW.fits``)
   Multi-extension FITS files containing:

   * Primary HDU: Original header with stacking metadata
   * SCI extension: Stacked image data
   * ERR extension: Uncertainty map

**Radial Profile Plot** (``*.pdf``)
   Publication-ready figure showing:

   * Surface brightness vs. radius for each filter
   * Error bars representing measurement uncertainties
   * Background fit overlays

Python API Usage
----------------

For more control, you can use the Python API directly:

.. code-block:: python

   import numpy as np
   from astropy.io import fits
   from astropy.wcs import WCS
   from stacked_seds import stacking, photometry, plotting

   # Load your FITS file
   with fits.open('image.fits') as hdul:
       image_data = hdul[0].data
       header = hdul[0].header
       wcs_obj = WCS(header)

   # Get galaxy coordinates from region file
   pixel_coords = stacking.get_galaxy_pixel_coords('image.fits', 'galaxies.reg')

   # Create stamps around each galaxy
   stamps = stacking.create_stamps(image_data, wcs_obj, pixel_coords, stamp_size=51)

   # Stack the images
   stacked_image, error_map = stacking.stack_images(stamps, trim_fraction=0.1)

   # Perform radial photometry
   center = (25, 25)  # Center of your stacked galaxy
   radii, profile, errors = photometry.get_radial_profile(stacked_image, center)

   # Get pixel scale for conversion to arcseconds
   pixel_scale = photometry.get_pixel_scale(header)
   radii_arcsec = radii * pixel_scale

Advanced Configuration
----------------------

**Adjusting Stack Parameters**

* ``stamp_size``: Size of cutouts in pixels (odd numbers recommended)
* ``trim_fraction``: Fraction of outliers to reject (0.1 = 10% from each end)

**Photometry Settings**

* ``background_reduction``: Whether to subtract fitted background
* ``bkg_fit_range``: Range of pixels to use for background fitting
* ``galaxy_centers``: Precise centers for each stacked image

**Common Issues**

* **Few valid stamps**: Check that your region file coordinates are correct
* **Poor background fit**: Adjust ``bkg_fit_range`` to avoid contaminated regions
* **Misaligned centers**: Fine-tune ``galaxy_centers`` by examining stacked images

Next Steps
----------

* Check the :doc:`examples` for more detailed workflows
* See the :doc:`api/stacking` for full function documentation
* Read the :doc:`faq` for troubleshooting common issues
