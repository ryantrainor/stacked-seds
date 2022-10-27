#!/usr/bin/env python3
"""
Script to create minimal test data for integration tests.

Run this script to generate test FITS files and configuration
that can be used to test the actual workflow.
"""

import os
import numpy as np
from pathlib import Path
from astropy.io import fits
from astropy.wcs import WCS


def create_test_data():
    """Create minimal test data for integration tests."""

    # Create test data directory
    test_data_dir = Path("tests/data")
    test_data_dir.mkdir(parents=True, exist_ok=True)

    print(f"Creating test data in {test_data_dir}")

    # Create FITS header with WCS
    header = fits.Header()
    header["SIMPLE"] = True
    header["BITPIX"] = -32
    header["NAXIS"] = 2
    header["NAXIS1"] = 200
    header["NAXIS2"] = 200
    header["CRPIX1"] = 100.0
    header["CRPIX2"] = 100.0
    header["CRVAL1"] = 237.2
    header["CRVAL2"] = 34.4
    header["CD1_1"] = -0.00027
    header["CD1_2"] = 0.0
    header["CD2_1"] = 0.0
    header["CD2_2"] = 0.00027
    header["CTYPE1"] = "RA---TAN"
    header["CTYPE2"] = "DEC--TAN"
    header["OBJECT"] = "TEST_FIELD"
    header["FILTER"] = "TEST"

    # Create realistic image data
    np.random.seed(42)  # For reproducible test data
    image_data = np.random.normal(10, 2, (200, 200))  # Sky background

    # Add some realistic sources at known positions
    source_positions = [(50, 50), (100, 150), (150, 75), (75, 125)]

    for x, y in source_positions:
        # Create a realistic 2D Gaussian source
        yy, xx = np.ogrid[:200, :200]
        source = 500 * np.exp(-((xx - x) ** 2 + (yy - y) ** 2) / (2 * 3**2))
        image_data += source

    # Add some cosmic rays
    cosmic_ray_positions = [(25, 25), (175, 175), (30, 170)]
    for x, y in cosmic_ray_positions:
        image_data[y - 1 : y + 2, x - 1 : x + 2] += 1000  # Sharp cosmic ray

    # Save test FITS file
    fits_file = test_data_dir / "test_image.fits"
    fits.writeto(fits_file, image_data, header, overwrite=True)
    print(f"✅ Created {fits_file}")

    # Create region file with source coordinates
    w = WCS(header)
    world_coords = w.wcs_pix2world(source_positions, 1)  # 1-based pixel coordinates

    region_file = test_data_dir / "test_regions.reg"
    with open(region_file, "w") as f:
        f.write("fk5\n")
        for ra, dec in world_coords:
            # Use decimal degrees format directly (not sexagesimal)
            f.write(f"point({ra:.8f},{dec:.8f})\n")
    print(f"✅ Created {region_file} with {len(world_coords)} sources")

    # Debug: Print the coordinates for verification
    print("\nDebug info:")
    print(f"Pixel coordinates (1-based): {source_positions}")
    print(f"World coordinates (decimal degrees):")
    for i, (ra, dec) in enumerate(world_coords):
        print(f"  Source {i+1}: RA={ra:.8f}, Dec={dec:.8f}")

    # Test coordinate conversion back
    test_pixels = w.wcs_world2pix(world_coords, 1)
    print(f"Round-trip pixel coordinates: {test_pixels}")
    print(f"Original pixel coordinates: {source_positions}")
    max_error = np.max(np.abs(np.array(test_pixels) - np.array(source_positions)))
    print(f"Coordinate conversion error: {max_error:.6f} pixels")

    if max_error > 0.01:
        print("⚠️  Warning: Large coordinate conversion error!")

    # Create zeropoints file
    zp_file = test_data_dir / "test_zeropoints.txt"
    with open(zp_file, "w") as f:
        f.write("test_image.fits 25.0\n")
    print(f"✅ Created {zp_file}")

    # Create test configuration file
    config_file = test_data_dir / "test_config.yml"
    config_content = f"""# Test configuration for integration tests
data_directory: "{test_data_dir}/"
output_directory: "{test_data_dir}/output/"
plot_directory: "{test_data_dir}/plots/"
region_file: "test_regions.reg"
zeropoints_file: "test_zeropoints.txt"

stacking_params:
  files_to_stack:
    - "test_image.fits"
  stamp_size: 51
  trim_fraction: 0.1

photometry_params:
  background_reduction: true
  galaxy_centers:
    test_image_NEW.fits: [25.0, 25.0]
  bkg_fit_range: [10, -5]
  plot_title: "Test Radial Profiles"
  output_plot_filename: "test_plot.pdf"
"""

    with open(config_file, "w") as f:
        f.write(config_content)
    print(f"✅ Created {config_file}")

    # Create output directories
    output_dir = test_data_dir / "output"
    plots_dir = test_data_dir / "plots"
    output_dir.mkdir(exist_ok=True)
    plots_dir.mkdir(exist_ok=True)
    print(f"✅ Created output directories")

    print(f"\n🎉 Test data creation complete!")
    print(f"📁 Files created in: {test_data_dir}")
    print(f"📊 Image size: 200x200 pixels")
    print(f"🌟 Sources: {len(source_positions)} realistic galaxies")
    print(f"⚡ Cosmic rays: {len(cosmic_ray_positions)} for testing robustness")

    print(f"\nTo run integration tests:")
    print(f"  pytest tests/test_integration.py -v")
    print(f"  pytest tests/test_integration.py -m 'not slow' -v  # Skip slow tests")
    print(f"  pytest tests/test_integration.py -v -s  # With output")

    return test_data_dir


if __name__ == "__main__":
    create_test_data()
