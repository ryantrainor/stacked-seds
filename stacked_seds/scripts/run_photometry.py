#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main script to run photometry on stacked images and generate plots.
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
from stacked_seds.photometry import get_pixel_scale, get_radial_profile, fit_background
from stacked_seds.plotting import plot_radial_profiles
from stacked_seds.utils import load_config
from typing import Dict, Any


def main() -> None:
    """
    Main script to run photometry and plotting on stacked galaxy images.
    """
    parser = argparse.ArgumentParser(
        description="Run photometry and plotting on stacked galaxy images."
    )
    parser.add_argument(
        "config_path", type=str, help="Path to the configuration YAML file."
    )
    args = parser.parse_args()

    config = load_config(args.config_path)
    phot_params = config["photometry_params"]

    os.makedirs(config["plot_directory"], exist_ok=True)

    results: Dict[str, Any] = {}

    processed_files = sorted(
        [f for f in os.listdir(config["output_directory"]) if f.endswith("_NEW.fits")]
    )

    for filename in processed_files:
        print(f"--- Analyzing {filename} ---")
        file_path = os.path.join(config["output_directory"], filename)

        with fits.open(file_path) as hdul:
            data = hdul["SCI"].data
            header = hdul[0].header

        center = phot_params["galaxy_centers"].get(filename)
        if not center:
            print(f"Warning: No center found for {filename} in config. Skipping.")
            continue

        pixel_scale = get_pixel_scale(header)
        radii_pix, profile_flux, error_flux = get_radial_profile(data, center)

        profile_sb = profile_flux / pixel_scale**2
        error_sb = error_flux / pixel_scale**2

        bkg_fit_flux = fit_background(
            radii_pix, profile_flux, phot_params["bkg_fit_range"]
        )

        if phot_params["background_reduction"]:
            profile_sb -= bkg_fit_flux / pixel_scale**2

        results[filename] = {
            "radii_arcsec": radii_pix * pixel_scale,
            "profile_sb": profile_sb,
            "error_sb": error_sb,
            "bkg_fit_sb": bkg_fit_flux / pixel_scale**2,
        }

    output_plot_path = os.path.join(
        config["plot_directory"], phot_params["output_plot_filename"]
    )
    plot_radial_profiles(
        results, title=phot_params["plot_title"], output_path=output_plot_path
    )
    print("\n✅ Photometry and plotting workflow complete!")


if __name__ == "__main__":
    main()
