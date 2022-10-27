import numpy as np
from astropy.io import fits
from astropy.nddata import Cutout2D
from astropy import wcs
from astropy.coordinates import SkyCoord
import astropy.units as u
from scipy import stats
from typing import Tuple, List


def get_galaxy_pixel_coords(image_path: str, region_path: str) -> np.ndarray:
    """
    Reads a FITS image header and a region file to get galaxy pixel coordinates.

    Args:
        image_path (str): Path to the FITS image file.
        region_path (str): Path to the .reg file containing galaxy world coordinates.

    Returns:
        np.ndarray: An array of (x, y) pixel coordinates for each galaxy.
    """
    with fits.open(image_path) as hdul:
        w = wcs.WCS(hdul[0].header)

    with open(region_path) as f:
        lines: List[str] = f.readlines()

    world_coords: List[List[float]] = []
    for line in lines:
        line = line.strip()
        if "point" in line and not line.startswith("#"):
            # Parse point(ra,dec) format
            # Remove "point(" and ")" and split by comma
            coords_str = line.replace("point(", "").replace(")", "")
            parts = coords_str.split(",")

            if len(parts) >= 2:
                try:
                    # Try parsing as decimal degrees first
                    ra_str, dec_str = parts[0].strip(), parts[1].strip()

                    # Handle potential sexagesimal format
                    if ":" in ra_str or ":" in dec_str:
                        # Use SkyCoord for sexagesimal parsing
                        c: SkyCoord = SkyCoord(
                            ra_str, dec_str, unit=(u.hourangle, u.degree), frame="fk5"
                        )
                        world_coords.append([c.ra.degree, c.dec.degree])
                    else:
                        # Direct decimal degree parsing
                        ra = float(ra_str)
                        dec = float(dec_str)
                        world_coords.append([ra, dec])

                except (ValueError, TypeError) as e:
                    print(f"Warning: Could not parse coordinates from line: {line}")
                    print(f"Error: {e}")
                    continue

    if not world_coords:
        raise ValueError(f"No valid coordinates found in region file: {region_path}")

    # Convert to pixel coordinates
    pixel_coords = w.wcs_world2pix(world_coords, 1)  # 1-based indexing

    # Convert to 0-based indexing for Python
    pixel_coords = pixel_coords - 1

    return pixel_coords


def create_stamps(
    image_data: np.ndarray,
    wcs_obj: wcs.WCS,
    pixel_coords: np.ndarray,
    stamp_size: int = 51,
) -> np.ndarray:
    """
    Creates cutout stamps for each coordinate in the pixel coordinate array.

    Args:
        image_data (np.ndarray): The 2D FITS image data.
        wcs_obj (wcs.WCS): The World Coordinate System object from the FITS header.
        pixel_coords (np.ndarray): Array of (x, y) pixel coordinates.
        stamp_size (int): The edge length of the square stamp in pixels.

    Returns:
        np.ndarray: A 3D array of all valid (correctly sized) stamps.
    """
    valid_stamps: List[np.ndarray] = []
    for x, y in pixel_coords:
        position = (x, y)
        try:
            cutout = Cutout2D(
                image_data, position, (stamp_size, stamp_size), wcs=wcs_obj
            )
            if cutout.shape == (stamp_size, stamp_size):
                valid_stamps.append(cutout.data)
        except Exception:
            # Catches galaxies too close to the edge
            continue

    return np.array(valid_stamps)


def stack_images(
    stamps: np.ndarray, trim_fraction: float = 0.1
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Stacks a set of image stamps using a trimmed mean and calculates the error.

    Args:
        stamps (np.ndarray): A 3D array of stamps to stack.
        trim_fraction (float): The fractional part of data to trim from each end.

    Returns:
        tuple: A tuple containing:
            - np.ndarray: The final stacked 2D image.
            - np.ndarray: The 2D error map (standard error of the mean).
    """
    num_galaxies: int = stamps.shape[0]
    if num_galaxies == 0:
        raise ValueError("Cannot stack an empty array of stamps.")

    stacked_image: np.ndarray = stats.trim_mean(stamps, trim_fraction, axis=0)

    # Calculate error using Median Absolute Deviation (MAD) for robustness
    mad: np.ndarray = stats.median_abs_deviation(stamps, axis=0) * 1.4826
    std_error: np.ndarray = mad / np.sqrt(num_galaxies - 1)

    return stacked_image, std_error


def save_stacked_fits(
    filename: str,
    data: np.ndarray,
    error_map: np.ndarray,
    original_header: fits.Header,
    zeropoint: float,
) -> None:
    """
    Saves the stacked data and error map to a new FITS file.

    Args:
        filename (str): The output path for the new FITS file.
        data (np.ndarray): The 2D stacked image data.
        error_map (np.ndarray): The 2D standard error map.
        original_header (fits.Header): The header from the original image.
        zeropoint (float): The magnitude zeropoint for this band.
    """
    hdr: fits.Header = original_header.copy()
    hdr.set("ZEROPT", zeropoint, "Magnitude zeropoint")
    hdr.add_history("Image stacked from multiple galaxy stamps.")

    primary_hdu = fits.PrimaryHDU(header=hdr)
    image_hdu = fits.ImageHDU(data, name="SCI")
    error_hdu = fits.ImageHDU(error_map, name="ERR")

    hdul = fits.HDUList([primary_hdu, image_hdu, error_hdu])
    hdul.writeto(filename, overwrite=True)
    print(f"Saved stacked image to {filename}")
