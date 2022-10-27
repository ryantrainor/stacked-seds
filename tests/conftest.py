import pytest
from astropy.io import fits


@pytest.fixture(scope="session")
def dummy_wcs_header() -> fits.Header:
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
    return header
