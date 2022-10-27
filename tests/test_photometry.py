import numpy as np
from stacked_seds import photometry
from astropy.io import fits


def test_get_pixel_scale(dummy_wcs_header: fits.Header) -> None:
    """
    Tests that the pixel scale is correctly calculated from the FITS header.
    """
    # Modify the header to use CD matrix (preferred)
    dummy_wcs_header["CD1_1"] = -0.0001
    dummy_wcs_header["CD1_2"] = 0.0

    scale = photometry.get_pixel_scale(dummy_wcs_header)

    # Expected scale is 0.0001 deg/pix * 3600 arcsec/deg = 0.36 arcsec/pix
    assert np.isclose(scale, 0.36)


def test_get_radial_profile() -> None:
    """
    Tests the radial profile calculation with a simple, predictable image.
    """
    # Create a 21x21 image with a bright 3x3 square at the center
    image_data = np.zeros((21, 21))
    image_data[9:12, 9:12] = 100.0
    center = (10.0, 10.0)

    radii, profile, error = photometry.get_radial_profile(image_data, center)

    # The first few bins should have high values
    assert profile[0] > 90
    assert profile[1] > 90
    # The outer bins should be zero
    assert np.isclose(profile[-1], 0.0)
    # The number of bins should be correct
    assert len(radii) == len(profile)


def test_fit_background() -> None:
    """
    Tests the background fitting function with a known quadratic profile.
    """
    # Create a fake radial profile that is purely background
    radii = np.arange(20)
    true_bkg = 5 + 0.1 * radii**2

    # Define a fit range that covers the whole profile for this test
    fit_range = [0, -1]

    fitted_bkg = photometry.fit_background(radii, true_bkg, fit_range)

    # The fitted model should be very close to the true background
    assert np.allclose(fitted_bkg, true_bkg, atol=1e-6)
