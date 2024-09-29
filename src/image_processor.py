# galaxy_stacker/
#   __init__.py
#   image_processor.py
#   utils.py
#   main.py

# galaxy_stacker/__init__.py
from .image_processor import ImageProcessor

# galaxy_stacker/image_processor.py
import os
from typing import List, Dict, Tuple
from astropy.io import fits
from astropy.nddata import Cutout2D
from astropy import wcs
from astropy.coordinates import SkyCoord
import astropy.units as u
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

class ImageProcessor:
    """
    A class for processing astronomical images and stacking galaxy measurements.

    This class provides methods for loading FITS images, extracting stamps around
    specified coordinates, and performing statistical analyses on the resulting data.

    Attributes:
    file_directory (str): Directory containing the input FITS files.
    region_file (str): Name of the region file containing galaxy coordinates.
    ignored_files (List[str]): List of filenames to be ignored during processing.
    files (List[str]): List of FITS files to be processed.
    num_galaxies (int): Number of galaxies to be processed.
    zero_points (Dict[str, float]): Dictionary of zero points for each file.
    """

    def __init__(self, file_directory: str, region_file: str):
        """
        Initialize the ImageProcessor with the given file directory and region file.

        Args:
            file_directory (str): Path to the directory containing FITS files.
            region_file (str): Name of the region file with galaxy coordinates.
        """
        self.file_directory = file_directory
        self.region_file = region_file
        self.ignored_files = ["q1549_H0.reg.Hsnorm.fits", "q1549_J0.reg.J3norm.fits", "q1549nb_tot_final.zp30.fits"]
        self.files = [
            "q1549_Hl.reg.fits", "q1549_Hs.reg.fits", "q1549_J.fits", "q1549_J1.reg.fits",
            "q1549_J2.reg.fits", "q1549_J3.reg.fits", "q1549_K.fits", "q1549G.zp30.reg.fits", "q1549Rse.fits"
        ]
        self.num_galaxies = 201  # 206 - 5, number of lines in the region file
        self.zero_points = self.load_zero_points()

    def load_zero_points(self) -> Dict[str, float]:
        """
        Load zero points from a text file.

        Returns: Dict[str, float]: A dictionary mapping filenames to their zero points.
        """
        zero_points = {}
        with open(os.path.join(self.file_directory, "zeropoints.txt"), "r") as reader:
            for line in reader:
                file_name, value = line.strip().split()
                zero_points[file_name] = float(value)
        return zero_points

    def process_images(self) -> None:
        """
        Process all images in the file list.

        This method loads each image, extracts stamps, calculates statistics,
        and saves the results.
        """
        for file in self.files:
            image_data, header = self.load_image(file)
            coord_array = self.get_coordinates()
            pixel_coord_array = self.world_to_pixel(header, coord_array)
            full_stamps = self.create_stamps(image_data, pixel_coord_array)

            averaged_image = self.calculate_averaged_image(full_stamps)
            mad_data = self.calculate_mad(full_stamps)

            self.save_processed_image(file, averaged_image, mad_data, header)
            self.plot_averaged_image(file, averaged_image)

    def load_image(self, file: str) -> Tuple[np.ndarray, fits.Header]:
        """
        Load a FITS image file.

        Args:
            file (str): Name of the FITS file to load.

        Returns:
            Tuple[np.ndarray, fits.Header]: The image data and header.
        """
        with fits.open(os.path.join(self.file_directory, file)) as hdulist:
            return hdulist[0].data, hdulist[0].header

    def get_coordinates(self) -> List[List[float]]:
        """
        Extract coordinates from the region file.

        Returns:
            List[List[float]]: List of [RA, Dec] coordinates.
        """
        coord_array = []
        with open(os.path.join(self.file_directory, self.region_file)) as reg_file:
            for line in reg_file:
                if "point" in line:
                    ra, dec = line[6:18], line[19:31]
                    c = SkyCoord(ra, dec, unit=(u.hourangle, u.degree), frame='fk5')
                    coord_array.append([c.ra.degree, c.dec.degree])
        return coord_array

    def world_to_pixel(self, header: fits.Header, coord_array: List[List[float]]) -> np.ndarray:
        """
        Convert world coordinates to pixel coordinates.

        Args:
            header (fits.Header): FITS header containing WCS information.
            coord_array (List[List[float]]): List of [RA, Dec] coordinates.

        Returns:
            np.ndarray: Array of pixel coordinates.
        """
        w = wcs.WCS(header)
        return w.wcs_world2pix(coord_array, 1)

    def create_stamps(self, image_data: np.ndarray, pixel_coord_array: np.ndarray) -> List[np.ndarray]:
        """
        Create image stamps centered on given pixel coordinates.

        Args:
            image_data (np.ndarray): Full image data.
            pixel_coord_array (np.ndarray): Array of pixel coordinates.

        Returns:
            List[np.ndarray]: List of image stamps.
        """
        full_stamps = []
        for pixel in pixel_coord_array:
            stamp = Cutout2D(image_data, pixel, (51, 51)).data
            if stamp.shape == (51, 51):
                full_stamps.append(stamp)
        return full_stamps

    def calculate_averaged_image(self, full_stamps: List[np.ndarray]) -> np.ndarray:
        """
        Calculate the trimmed mean of the image stamps.

        Args:
            full_stamps (List[np.ndarray]): List of image stamps.

        Returns:
            np.ndarray: Averaged image.
        """
        return stats.trim_mean(full_stamps, 0.1, axis=0)

    def calculate_mad(self, full_stamps: List[np.ndarray]) -> np.ndarray:
        """
        Calculate the Median Absolute Deviation (MAD) of the image stamps.

        Args:
            full_stamps (List[np.ndarray]): List of image stamps.

        Returns:
            np.ndarray: MAD image.
        """
        return 1.5 * stats.median_absolute_deviation(full_stamps, axis=0) / np.sqrt(self.num_galaxies - 1)

    def save_processed_image(self, file: str, averaged_image: np.ndarray, mad_data: np.ndarray, header: fits.Header) -> None:
        """
        Save the processed image data to a new FITS file.

        Args:
            file (str): Original filename.
            averaged_image (np.ndarray): Averaged image data.
            mad_data (np.ndarray): MAD image data.
            header (fits.Header): FITS header from the original file.
        """
        image_hdu = fits.ImageHDU(averaged_image)
        mad_hdu = fits.ImageHDU(mad_data)
        header['ZEROPT'] = self.zero_points[file]
        primary_hdu = fits.PrimaryHDU(header=header)
        hdul = fits.HDUList([primary_hdu, image_hdu, mad_hdu])
        output_file = os.path.join(self.file_directory, "..", "New_Files", f"{os.path.splitext(file)[0]}_NEW.fits")
        hdul.writeto(output_file, overwrite=True)

    def plot_averaged_image(self, file: str, averaged_image: np.ndarray) -> None:
        """
        Plot and save the averaged image.

        Args:
            file (str): Original filename.
            averaged_image (np.ndarray): Averaged image data.
        """
        plt.clf()
        plt.imshow(averaged_image, origin='lower')
        plt.colorbar()
        plt.title(f"{os.path.splitext(file)[0]} with trimmed mean")
        output_file = os.path.join(self.file_directory, "..", "Stacked_PDFs", f"{os.path.splitext(file)[0]}.pdf")
        plt.savefig(output_file)

# galaxy_stacker/utils.py
import os

def clean_output_directories(directories: List[str]) -> None:
    """
    Remove all files from specified directories.

    Args:
        directories (List[str]): List of directory paths to clean.
    """
    for directory in directories:
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")

# galaxy_stacker/main.py
from galaxy_stacker import ImageProcessor
from galaxy_stacker.utils import clean_output_directories

def main() -> None:
    """
    Main function to run the galaxy stacking process.
    """
    file_directory = "/Users/cwmchapman/Documents/Franklin and Marshall/Trainor Research/SED_Project/Original_Files/"
    region_file = "q1549_nbcands.reg"

    # Clean up existing files
    output_dirs = [
        "/Users/cwmchapman/Documents/Franklin and Marshall/Trainor Research/SED_Project/New_Files/",
        "/Users/cwmchapman/Documents/Franklin and Marshall/Trainor Research/SED_Project/Stacked_PDFs/"
    ]
    clean_output_directories(output_dirs)

    processor = ImageProcessor(file_directory, region_file)
    processor.process_images()

if __name__ == "__main__":
    main()
