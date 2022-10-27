Configuration
=============

Stacked SEDs uses YAML configuration files to control all aspects of the analysis workflow. This page provides complete examples and detailed explanations of all configuration options.

Quick Start Configuration
-------------------------

Here's a minimal configuration file to get started:

.. code-block:: yaml

   # Basic configuration for Stacked SEDs
   data_directory: "data/"
   output_directory: "output/"
   plot_directory: "plots/"
   region_file: "galaxies.reg"
   zeropoints_file: "zeropoints.txt"

   stacking_params:
     files_to_stack:
       - "image1.fits"
       - "image2.fits"
     stamp_size: 51
     trim_fraction: 0.1

   photometry_params:
     background_reduction: true
     galaxy_centers:
       image1_NEW.fits: [25.0, 25.0]
       image2_NEW.fits: [25.0, 25.0]
     bkg_fit_range: [6, -5]
     plot_title: "Radial Profiles"
     output_plot_filename: "radial_plot.pdf"

Complete Configuration Example
------------------------------

Here's a full configuration file with all available options and detailed comments:

.. code-block:: yaml

   # =================================================================
   # Stacked SEDs Configuration File
   # =================================================================

   # --- File Paths ---
   # All paths can be absolute or relative to where you run the commands

   data_directory: "data/raw/"              # Directory containing FITS files
   output_directory: "data/processed/"      # Where to save stacked images
   plot_directory: "plots/"                 # Where to save output plots
   region_file: "q1549_nbcands.reg"        # DS9 region file with galaxy coordinates
   zeropoints_file: "zeropoints.txt"       # Text file with magnitude zeropoints

   # --- Image Stacking Parameters ---
   stacking_params:

     # List of FITS files to process (must be in data_directory)
     files_to_stack:
       - "q1549_Hl.reg.fits"     # H-band long exposure
       - "q1549_Hs.reg.fits"     # H-band short exposure
       - "q1549_J1.reg.fits"     # J-band exposure 1
       - "q1549_J2.reg.fits"     # J-band exposure 2
       - "q1549_J3.reg.fits"     # J-band exposure 3
       - "q1549_K.fits"          # K-band exposure
       - "q1549G.zp30.reg.fits"  # G-band exposure
       - "q1549Rse.fits"         # R-band exposure

     # Size of cutout stamps in pixels (must be odd number)
     # Recommended: 51 for compact sources, 101 for extended sources
     stamp_size: 51

     # Fraction of outliers to trim from each end during stacking
     # 0.1 = remove 10% from each end (20% total outlier rejection)
     # Increase for noisier data, decrease for high-quality data
     trim_fraction: 0.1

   # --- Photometry and Plotting Parameters ---
   photometry_params:

     # Whether to subtract fitted background from radial profiles
     background_reduction: true

     # Precise center coordinates for each stacked image
     # Format: filename: [x_pixel, y_pixel]
     # These are the centers of the stacked galaxy in the output images
     galaxy_centers:
       q1549_Hl.reg_NEW.fits: [25.0, 23.7]      # Slightly off-center
       q1549_Hs.reg_NEW.fits: [26.0, 24.5]      # Adjust for each filter
       q1549_J1.reg_NEW.fits: [25.0, 25.0]      # Perfect center
       q1549_J2.reg_NEW.fits: [25.5, 24.5]      # Fine-tuned position
       q1549_J3.reg_NEW.fits: [25.5, 25.0]      # Fine-tuned position
       q1549_K_NEW.fits: [26.0, 25.0]           # Note: no .reg in filename
       q1549G.zp30.reg_NEW.fits: [24.0, 24.0]   # Systematic offset
       q1549Rse_NEW.fits: [25.0, 25.0]          # Perfect center

     # Range of pixels to use for background fitting
     # Format: [start_pixel, end_pixel]
     # Negative end_pixel counts from the edge
     # [6, -5] means use pixels 6 to 5-from-edge for background fit
     bkg_fit_range: [6, -5]

     # Plot customization
     plot_title: "Radial Profiles of Stacked Galaxies"
     output_plot_filename: "all_bands_radial_plot.pdf"

File Format Requirements
------------------------

Input File Formats
~~~~~~~~~~~~~~~~~~~

**FITS Images**
   Your input FITS files should contain:

   * Standard astronomical image data
   * Valid WCS (World Coordinate System) header keywords
   * Consistent coordinate system across all images

**Region File (DS9 format)**
   The region file should contain point sources in FK5 coordinates:

   .. code-block:: text

      fk5
      point(237.123456,34.567890)
      point(237.234567,34.678901)
      point(237.345678,34.789012)

**Zeropoints File**
   Simple text file with filename and zeropoint:

   .. code-block:: text

      q1549_Hl.reg.fits 25.0
      q1549_Hs.reg.fits 24.8
      q1549_J1.reg.fits 25.2
      q1549_K.fits 25.0

Configuration Sections
----------------------

File Paths Section
~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Parameter
     - Type
     - Description
   * - ``data_directory``
     - string
     - Directory containing input FITS files
   * - ``output_directory``
     - string
     - Directory for stacked output images
   * - ``plot_directory``
     - string
     - Directory for output plots
   * - ``region_file``
     - string
     - DS9 region file with galaxy coordinates
   * - ``zeropoints_file``
     - string
     - Text file with magnitude zeropoints

Stacking Parameters
~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Parameter
     - Type
     - Description
   * - ``files_to_stack``
     - list
     - List of FITS filenames to process
   * - ``stamp_size``
     - integer
     - Size of cutout stamps in pixels (must be odd)
   * - ``trim_fraction``
     - float
     - Fraction of outliers to reject (0.0-0.5)

Photometry Parameters
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Parameter
     - Type
     - Description
   * - ``background_reduction``
     - boolean
     - Whether to subtract fitted background
   * - ``galaxy_centers``
     - dict
     - Center coordinates for each stacked image
   * - ``bkg_fit_range``
     - list
     - Pixel range for background fitting [start, end]
   * - ``plot_title``
     - string
     - Title for the summary plot
   * - ``output_plot_filename``
     - string
     - Filename for the output plot

Best Practices
--------------

**Stamp Size Selection**
   * Use odd numbers (51, 101, 151) for proper centering
   * 51 pixels: Good for point sources and compact galaxies
   * 101 pixels: Better for extended sources
   * Larger stamps require more memory and processing time

**Trim Fraction Guidelines**
   * 0.05-0.1: High-quality data with few cosmic rays
   * 0.1-0.2: Typical ground-based data
   * 0.2-0.3: Noisy data or many cosmic rays
   * Never use 0.5 or higher (removes too much real signal)

**Galaxy Center Determination**
   * Start with [25.0, 25.0] for 51x51 stamps
   * Examine stacked images to find true centers
   * Fine-tune in 0.1-pixel increments
   * Consistent centering improves photometry accuracy

**Background Fitting**
   * Use pixels far from galaxy center but within stamp
   * Avoid contaminated regions (other sources, artifacts)
   * [6, -5] works well for 51x51 stamps
   * Adjust based on galaxy size and stamp size

Example Workflows
-----------------

**Single Filter Analysis**

.. code-block:: yaml

   data_directory: "my_data/"
   output_directory: "results/"
   plot_directory: "plots/"
   region_file: "sources.reg"
   zeropoints_file: "zp.txt"

   stacking_params:
     files_to_stack:
       - "field_r_band.fits"
     stamp_size: 51
     trim_fraction: 0.1

   photometry_params:
     background_reduction: true
     galaxy_centers:
       field_r_band_NEW.fits: [25.0, 25.0]
     bkg_fit_range: [8, -8]
     plot_title: "R-band Radial Profile"
     output_plot_filename: "r_band_profile.pdf"

**Multi-Filter Survey**

.. code-block:: yaml

   data_directory: "/path/to/survey/data/"
   output_directory: "/path/to/survey/stacked/"
   plot_directory: "/path/to/survey/plots/"
   region_file: "target_galaxies.reg"
   zeropoints_file: "survey_zeropoints.txt"

   stacking_params:
     files_to_stack:
       - "field_u.fits"
       - "field_g.fits"
       - "field_r.fits"
       - "field_i.fits"
       - "field_z.fits"
     stamp_size: 101  # Larger for extended sources
     trim_fraction: 0.15

   photometry_params:
     background_reduction: true
     galaxy_centers:
       field_u_NEW.fits: [50.0, 50.0]
       field_g_NEW.fits: [50.0, 50.0]
       field_r_NEW.fits: [50.0, 50.0]
       field_i_NEW.fits: [50.0, 50.0]
       field_z_NEW.fits: [50.0, 50.0]
     bkg_fit_range: [15, -15]
     plot_title: "UGRIZ Photometric Analysis"
     output_plot_filename: "ugriz_comparison.pdf"

Troubleshooting Configuration
-----------------------------

**Common YAML Syntax Errors**
   * Inconsistent indentation (use spaces, not tabs)
   * Missing colons after parameter names
   * Incorrect list formatting (use ``-`` for list items)
   * Mixing single and double quotes

**File Path Issues**
   * Use forward slashes (/) even on Windows
   * Check that all file paths exist and are accessible
   * Use absolute paths if relative paths cause problems

**Parameter Validation**
   * Stamp size must be odd and positive
   * Trim fraction must be between 0.0 and 0.5
   * Galaxy centers must be within stamp boundaries
   * Background fit range must make sense for your stamp size
