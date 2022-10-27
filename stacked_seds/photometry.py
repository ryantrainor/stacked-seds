import numpy as np
from scipy.optimize import curve_fit
from astropy.io import fits
from typing import Tuple, List


def get_radial_profile(
    data: np.ndarray, center: Tuple[float, float]
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Calculates the azimuthally averaged radial profile of an image.

    Args:
        data (np.ndarray): The 2D image data.
        center (tuple): The (x, y) coordinates of the center.

    Returns:
        tuple: A tuple containing:
            - np.ndarray: The radial distance of each bin in pixels.
            - np.ndarray: The mean flux value in each radial bin.
            - np.ndarray: The standard error of the mean flux in each bin.
    """
    y, x = np.indices(data.shape)
    r: np.ndarray = np.sqrt((x - center[0]) ** 2 + (y - center[1]) ** 2).astype(int)

    # Ensure nr has no zeros to avoid division errors
    nr: np.ndarray = np.bincount(r.ravel())
    if np.any(nr == 0):
        valid_bins = nr > 0
        nr = nr[valid_bins]
        tbin: np.ndarray = np.bincount(r.ravel(), data.ravel())[valid_bins]
        radii_full = np.arange(len(valid_bins))
        radii: np.ndarray = radii_full[valid_bins]
    else:
        tbin: np.ndarray = np.bincount(r.ravel(), data.ravel())
        radii: np.ndarray = np.arange(len(nr))

    radial_mean: np.ndarray = tbin / nr

    std_dev = np.array([np.std(data[r == i]) for i in radii])
    radial_std_error: np.ndarray = std_dev / np.sqrt(nr)

    return radii, radial_mean, radial_std_error


def fit_background(
    radii: np.ndarray, radial_profile: np.ndarray, fit_range: List[int]
) -> np.ndarray:
    """
    Fits a quadratic function to the background of a radial profile.

    Args:
        radii (np.ndarray): Array of radial distances.
        radial_profile (np.ndarray): Array of flux values at each radius.
        fit_range (list): A list [start, end] defining the pixel range for the fit.

    Returns:
        np.ndarray: The modeled background flux at each radius.
    """

    def background_model(x: np.ndarray, a: float, b: float) -> np.ndarray:
        """A simple quadratic model for sky background."""
        return a + b * x**2

    start, end = fit_range[0], fit_range[1]
    xdata: np.ndarray = radii[start:end]
    ydata: np.ndarray = radial_profile[start:end]

    try:
        params, _ = curve_fit(background_model, xdata, ydata)
        fit_y: np.ndarray = background_model(radii, *params)
    except RuntimeError:
        print("Warning: Background fit failed. Returning zero background.")
        fit_y = np.zeros_like(radii)

    return fit_y


def get_pixel_scale(header: fits.Header) -> float:
    """
    Calculates the pixel scale from a FITS header in arcsec/pixel.
    """
    try:
        # Assumes CD matrix, preferred FITS standard
        scale: float = np.sqrt(header["CD1_1"] ** 2 + header["CD1_2"] ** 2) * 3600
    except KeyError:
        # Fallback for older CDELT standard
        scale = abs(header["CDELT1"]) * 3600
    return scale
