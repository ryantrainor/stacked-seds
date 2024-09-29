import logging
import astropy.units as units
import numpy as np
from astropy import stats
from astropy.nddata import Cutout2D
from astropy.coordinates import SkyCoord
from astropy.io import fits
from astropy import wcs


class ImageGenerator:
    cutout: Cutout2D
    coordinates: fits.HDUList
    averages: dict
    filename: str

    def __init__(self, filename: str) -> None:
        self.filename = filename

    def generate_coordinates(self, coordinates: list) -> None:
        try:
            array = []
            for line in coordinates:
                if "point" in line:
                    ra = line[6:18]
                    dec = line[19:31]
                    coordinate = SkyCoord(ra, dec, unit=(units.dimensionless_angles, units.degree), frame='fk5')
                    array.append([coordinate.ra.degree, coordinate.dec.degree])
            self.coordinates =  coordinates.wcs_world2pix(array, 1)
        except Exception as e:
            logging.error(e)

    def generate_cutout(self, image: str, position: tuple) -> None:
        try:
            fittings: fits.HDUList  = fits.open(image)
            coordinates: wcs.WCS = wcs.WCS(fittings[0].header)
            self.image =  Cutout2D(fittings[0].data, position, (51, 51), coordinates)
        except Exception as e:
            logging.error(e)

    def generate_plot(self, zeros: list) -> None:
        ## TODO: Fix this method to generate proper plot
        try:
            if self.cutout is None or self.coordinates is None or self.averages == {}:
                raise Exception("Error: Cutout, Coordinates, or Averages are not defined")
            else:
                for i in range(len(self.averages)):
                    first_image_hdu = fits.ImageHDU(self.averages[i])
                    second_image_hdu = fits.ImageHDU(zeros[i])
                    empty_primary = fits.PrimaryHDU()
                    fits.HDUList([empty_primary, first_image_hdu, second_image_hdu])
        except Exception as e:
            logging.error(e)

    def get_averages(self, averages: list[float], mad: list, images: list[list[int]], file_path: str, galaxies_count: int) -> None:
        ## TODO: Remove hardcoded filename and average
        try:
            for image in images:
                averages.append(np.mean(stats.sigma_clip(image, axis=0), axis=0))
                mad.append(1.5 * stats.median_absolute_deviation((image)/np.sqrt(galaxies_count-1), axis=0))
                file_name = file_path + "zeropoints.txt"
                reader = open(file_name)
                lines = reader.readlines()
                for line in lines:
                    line = line.split(' ')
                    self.averages[line[0]] = float(line[1])
        except Exception as e:
            logging.error(e)
