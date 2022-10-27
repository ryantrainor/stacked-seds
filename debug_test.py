#!/usr/bin/env python3
"""
Debug script to diagnose integration test failures.
"""

import numpy as np
from pathlib import Path
from astropy.io import fits
from astropy.wcs import WCS

from stacked_seds import stacking


def debug_coordinate_issue():
    """Debug why no stamps are being created."""

    # Check if test data exists
    test_data_dir = Path("tests/data")
    fits_file = test_data_dir / "test_image.fits"
    region_file = test_data_dir / "test_regions.reg"

    if not fits_file.exists():
        print(f"❌ FITS file not found: {fits_file}")
        print("Run: python create_test_data.py")
        return

    if not region_file.exists():
        print(f"❌ Region file not found: {region_file}")
        print("Run: python create_test_data.py")
        return

    print("✅ Test files exist")

    # Check FITS file
    print(f"\n--- Checking FITS file: {fits_file} ---")
    with fits.open(fits_file) as hdul:
        header = hdul[0].header
        image_data = hdul[0].data
        wcs_obj = WCS(header)

    print(f"Image shape: {image_data.shape}")
    print(f"Image data range: {image_data.min():.2f} to {image_data.max():.2f}")
    print(f"WCS valid: {wcs_obj.is_celestial}")

    # Check region file
    print(f"\n--- Checking region file: {region_file} ---")
    with open(region_file) as f:
        lines = f.readlines()

    print(f"Region file lines: {len(lines)}")
    for i, line in enumerate(lines):
        print(f"  Line {i}: {line.strip()}")

    # Test coordinate extraction
    print(f"\n--- Testing coordinate extraction ---")
    try:
        pixel_coords = stacking.get_galaxy_pixel_coords(
            str(fits_file), str(region_file)
        )
        print(f"✅ Coordinate extraction successful")
        print(f"Number of coordinates: {len(pixel_coords)}")
        print(f"Pixel coordinates:\n{pixel_coords}")

        # Check if coordinates are within image bounds
        for i, (x, y) in enumerate(pixel_coords):
            in_bounds = (0 <= x < image_data.shape[1]) and (
                0 <= y < image_data.shape[0]
            )
            print(f"  Source {i+1}: ({x:.2f}, {y:.2f}) - In bounds: {in_bounds}")

    except Exception as e:
        print(f"❌ Coordinate extraction failed: {e}")
        return

    # Test stamp creation with debug info
    print(f"\n--- Testing stamp creation ---")
    try:
        stamps = stacking.create_stamps(
            image_data, wcs_obj, pixel_coords, stamp_size=51
        )
        print(f"✅ Stamp creation successful")
        print(f"Number of stamps created: {stamps.shape[0]}")
        print(f"Stamp shape: {stamps.shape}")

        if stamps.shape[0] == 0:
            print("❌ No stamps created - investigating...")

            # Manual stamp creation for debugging
            stamp_size = 51
            half_size = stamp_size // 2

            for i, (x, y) in enumerate(pixel_coords):
                x_int, y_int = int(round(x)), int(round(y))
                x_min, x_max = x_int - half_size, x_int + half_size + 1
                y_min, y_max = y_int - half_size, y_int + half_size + 1

                print(f"  Source {i+1}: center=({x:.2f}, {y:.2f})")
                print(f"    Integer center: ({x_int}, {y_int})")
                print(f"    Stamp bounds: x=[{x_min}:{x_max}], y=[{y_min}:{y_max}]")
                print(
                    f"    Image bounds: x=[0:{image_data.shape[1]}], y=[0:{image_data.shape[0]}]"
                )

                # Check bounds
                if (
                    x_min >= 0
                    and x_max <= image_data.shape[1]
                    and y_min >= 0
                    and y_max <= image_data.shape[0]
                ):
                    print(f"    ✅ Source {i+1} should create valid stamp")
                else:
                    print(f"    ❌ Source {i+1} too close to edge")

    except Exception as e:
        print(f"❌ Stamp creation failed: {e}")
        import traceback

        traceback.print_exc()


def create_simple_test_data():
    """Create the simplest possible test data."""

    test_data_dir = Path("tests/data")
    test_data_dir.mkdir(parents=True, exist_ok=True)

    print("Creating minimal test data...")

    # Create very simple FITS file
    header = fits.Header()
    header["SIMPLE"] = True
    header["BITPIX"] = -32
    header["NAXIS"] = 2
    header["NAXIS1"] = 100
    header["NAXIS2"] = 100

    # Simple WCS - 1 arcsec per pixel
    header["CRPIX1"] = 50.5
    header["CRPIX2"] = 50.5
    header["CRVAL1"] = 0.0  # RA
    header["CRVAL2"] = 0.0  # Dec
    header["CDELT1"] = -1.0 / 3600.0  # -1 arcsec/pixel
    header["CDELT2"] = 1.0 / 3600.0  # +1 arcsec/pixel
    header["CTYPE1"] = "RA---TAN"
    header["CTYPE2"] = "DEC--TAN"

    # Simple image - background + one bright source at center
    image_data = np.ones((100, 100)) * 10.0  # Background
    image_data[45:55, 45:55] += 100.0  # Bright source at (50, 50)

    # Save FITS
    fits_file = test_data_dir / "simple_test.fits"
    fits.writeto(fits_file, image_data, header, overwrite=True)

    # Create simple region file - one source at image center
    w = WCS(header)
    world_coord = w.wcs_pix2world([[50, 50]], 1)[0]

    region_file = test_data_dir / "simple_test.reg"
    with open(region_file, "w") as f:
        f.write("fk5\n")
        f.write(f"point({world_coord[0]:.8f},{world_coord[1]:.8f})\n")

    print(f"✅ Created simple test data:")
    print(f"  FITS: {fits_file}")
    print(f"  Region: {region_file}")
    print(
        f"  Image center: pixel (50, 50) = world ({world_coord[0]:.8f}, {world_coord[1]:.8f})"
    )

    # Test it immediately
    print(f"\n--- Testing simple data ---")
    pixel_coords = stacking.get_galaxy_pixel_coords(str(fits_file), str(region_file))
    print(f"Extracted coordinates: {pixel_coords}")

    stamps = stacking.create_stamps(image_data, w, pixel_coords, stamp_size=51)
    print(f"Created {stamps.shape[0]} stamps of shape {stamps.shape}")

    if stamps.shape[0] > 0:
        print("✅ Simple test data works!")
        return True
    else:
        print("❌ Even simple test data failed")
        return False


if __name__ == "__main__":
    print("=== Debug Integration Test Issues ===\n")

    # First try with existing test data
    debug_coordinate_issue()

    print("\n" + "=" * 50)
    print("Creating and testing simple data...")
    create_simple_test_data()
