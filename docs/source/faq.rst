Frequently Asked Questions
==========================

Installation Issues
-------------------

**Q: I'm getting import errors when trying to use stacked_seds**

A: Make sure you've installed all dependencies and the package itself:

.. code-block:: bash

   pip install -r requirements.txt
   pip install -e .

**Q: The package won't install on my system**

A: Check that you're using Python 3.8 or newer:

.. code-block:: bash

   python --version

Stacking Problems
-----------------

**Q: I'm getting very few valid stamps**

A: This usually means your region file coordinates don't match your image. Check that:

- Region file uses the same coordinate system as your FITS header
- Galaxy positions are within the image boundaries
- Region file format is correct (DS9 format expected)

**Q: My stacked images look wrong**

A: Common issues include:

- Incorrect stamp size (try 51 or 101 pixels)
- Wrong trim fraction (start with 0.1)
- Misaligned input images

Photometry Issues
-----------------

**Q: The background fit is failing**

A: Adjust your ``bkg_fit_range`` parameter:

- Make sure the range doesn't include the galaxy center
- Use pixels far enough from the center but within the stamp
- Example: ``[6, -5]`` uses pixels 6 to 5-from-end

**Q: Galaxy centers are off in my stacked images**

A: Fine-tune the ``galaxy_centers`` parameter in your config:

- Examine your ``*_NEW.fits`` files to find the true center
- Update coordinates in the photometry section
- Centers should be in (x, y) pixel coordinates

Configuration Questions
-----------------------

**Q: What stamp size should I use?**

A: Recommended sizes:

- 51 pixels: For compact galaxies or crowded fields
- 101 pixels: For extended galaxies
- Always use odd numbers for proper centering

**Q: What trim fraction is best?**

A: Start with 0.1 (10% trimming):

- Increase to 0.2-0.3 for very noisy data
- Decrease to 0.05 for high-quality data
- Never use 0.0 unless your data is perfect

Performance Questions
---------------------

**Q: The stacking is very slow**

A: Performance depends on:

- Number of galaxies in your region file
- Size of your stamps
- Size of your input images

Try reducing stamp size or processing fewer galaxies for testing.

**Q: I'm running out of memory**

A: Large datasets can be memory-intensive:

- Process one filter at a time
- Reduce stamp size
- Split your galaxy list into smaller batches

Output Questions
----------------

**Q: What's in the output FITS files?**

A: ``*_NEW.fits`` files contain:

- Primary HDU: Original header with stacking metadata
- SCI extension: Stacked image data
- ERR extension: Uncertainty map

**Q: How do I interpret the radial profile plots?**

A: The plots show:

- X-axis: Radius in arcseconds
- Y-axis: Surface brightness (flux per square arcsec)
- Error bars: Standard error of the mean
- Dashed line: Background fit

Data Format Questions
---------------------

**Q: What region file format is supported?**

A: DS9 region files in FK5 coordinates:

.. code-block:: text

   fk5
   point(237.123456,34.567890)
   point(237.234567,34.678901)

**Q: What should my zeropoints file look like?**

A: Simple text format:

.. code-block:: text

   image1.fits 25.0
   image2.fits 24.8
   image3.fits 25.2

Troubleshooting
---------------

**Q: How do I debug issues?**

A: Check these in order:

1. Run the example to verify installation
2. Check your configuration file syntax
3. Verify your input file paths
4. Examine the console output for error messages
5. Check that your region file has the correct format

**Q: The example works but my data doesn't**

A: Common differences:

- Different FITS header keywords
- Different coordinate systems
- Different image sizes or pixel scales

**Q: Who can I contact for help?**

A:

- File an issue on GitHub for bugs
- Use GitHub Discussions for questions
- Email ryan.trainor@fandm.edu for direct help
