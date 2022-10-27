#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main script to run the galaxy stacking pipeline.
"""

import sys
import os

# Force UTF-8 encoding on Windows
if sys.platform == "win32":
    import codecs

    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())

import argparse
from astropy.io import fits
from astropy import wcs
from stacked_seds.stacking import (
    get_galaxy_pixel_coords,
    create_stamps,
    stack_images,
    save_stacked_fits,
)
from stacked_seds.utils import load_config
from typing import Dict, List


def main() -> None:
    """
    Main script to run the galaxy stacking pipeline.
    """
    parser = argparse.ArgumentParser(
        description="Stack galaxy images based on a configuration file."
    )
    parser.add_argument(
        "config_path", type=str, help="Path to the configuration YAML file."
    )
    args = parser.parse_args()

    config = load_config(args.config_path)

    os.makedirs(config["output_directory"], exist_ok=True)

    zeropoints: Dict[str, float] = {}
    zp_path: str = os.path.join(config["data_directory"], config["zeropoints_file"])
    with open(zp_path, "r") as reader:
        for line in reader.readlines():
            parts: List[str] = line.split()
            if len(parts) >= 2:
                zeropoints[parts[0]] = float(parts[1])

    for filename in config["stacking_params"]["files_to_stack"]:
        print(f"--- Processing {filename} ---")
        image_path: str = os.path.join(config["data_directory"], filename)
        region_path: str = os.path.join(config["data_directory"], config["region_file"])

        pixel_coords = get_galaxy_pixel_coords(image_path, region_path)

        with fits.open(image_path) as hdul:
            image_data = hdul[0].data
            wcs_obj = wcs.WCS(hdul[0].header)
            original_header = hdul[0].header

        stamps = create_stamps(
            image_data,
            wcs_obj,
            pixel_coords,
            stamp_size=config["stacking_params"]["stamp_size"],
        )
        print(f"Created {len(stamps)} valid stamps.")

        stacked_image, error_map = stack_images(
            stamps, trim_fraction=config["stacking_params"]["trim_fraction"]
        )

        output_filename = os.path.join(
            config["output_directory"], filename.replace(".fits", "_NEW.fits")
        )
        zeropoint: float = zeropoints.get(filename, 0.0)

        save_stacked_fits(
            output_filename, stacked_image, error_map, original_header, zeropoint
        )
    print("\n✅ Stacking workflow complete!")


if __name__ == "__main__":
    main()
