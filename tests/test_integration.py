"""
Integration tests using real FITS files.

These tests require actual FITS files to be present in tests/data/
and are marked as slow tests that can be skipped in CI.
"""

import pytest
import numpy as np
from pathlib import Path
from astropy.io import fits
from astropy.wcs import WCS

from stacked_seds import stacking, photometry, utils


# Skip these tests if test data is not available
TEST_DATA_DIR = Path(__file__).parent / "data"
FITS_FILE = TEST_DATA_DIR / "test_image.fits"
REGION_FILE = TEST_DATA_DIR / "test_regions.reg"
CONFIG_FILE = TEST_DATA_DIR / "test_config.yml"

pytestmark = pytest.mark.skipif(
    not FITS_FILE.exists() or not REGION_FILE.exists(),
    reason="Real test data not available",
)


@pytest.mark.slow
class TestRealDataIntegration:
    """Integration tests using real FITS files."""

    def test_full_stacking_workflow(self):
        """Test the complete stacking workflow with real data."""

        # Test coordinate extraction
        pixel_coords = stacking.get_galaxy_pixel_coords(
            str(FITS_FILE), str(REGION_FILE)
        )
        assert len(pixel_coords) > 0, "Should find galaxies in region file"

        # Test stamp creation
        with fits.open(FITS_FILE) as hdul:
            image_data = hdul[0].data
            wcs_obj = WCS(hdul[0].header)
            header = hdul[0].header

        stamps = stacking.create_stamps(
            image_data, wcs_obj, pixel_coords, stamp_size=51
        )
        assert stamps.shape[0] > 0, "Should create valid stamps"
        assert stamps.shape[1:] == (51, 51), "Stamps should be correct size"

        # Test stacking
        stacked_image, error_map = stacking.stack_images(stamps, trim_fraction=0.1)
        assert stacked_image.shape == (51, 51), "Stacked image wrong shape"
        assert error_map.shape == (51, 51), "Error map wrong shape"
        assert np.all(np.isfinite(stacked_image)), "Stacked image has invalid values"
        assert np.all(error_map >= 0), "Error map should be non-negative"

        # Test saving
        output_file = TEST_DATA_DIR / "test_output.fits"
        stacking.save_stacked_fits(
            str(output_file), stacked_image, error_map, header, 25.0
        )
        assert output_file.exists(), "Output file not created"

        # Verify saved file structure
        with fits.open(output_file) as hdul:
            assert len(hdul) == 3, "Should have 3 HDUs"
            assert "SCI" in [hdu.name for hdu in hdul], "Missing SCI extension"
            assert "ERR" in [hdu.name for hdu in hdul], "Missing ERR extension"
            assert hdul[0].header["ZEROPT"] == 25.0, "Zeropoint not saved"

        # Clean up
        output_file.unlink()

    def test_real_photometry_workflow(self):
        """Test photometry on real stacked data."""

        # Create a test stacked image first (reuse stacking test)
        pixel_coords = stacking.get_galaxy_pixel_coords(
            str(FITS_FILE), str(REGION_FILE)
        )

        with fits.open(FITS_FILE) as hdul:
            image_data = hdul[0].data
            wcs_obj = WCS(hdul[0].header)
            header = hdul[0].header

        stamps = stacking.create_stamps(
            image_data, wcs_obj, pixel_coords, stamp_size=51
        )
        stacked_image, error_map = stacking.stack_images(stamps)

        # Test photometry
        center = (25, 25)  # Center of 51x51 stamp
        radii, profile, errors = photometry.get_radial_profile(stacked_image, center)

        assert len(radii) > 10, "Should have multiple radial bins"
        assert len(profile) == len(radii), "Profile length mismatch"
        assert len(errors) == len(radii), "Error length mismatch"
        assert np.all(np.isfinite(profile)), "Profile has invalid values"
        assert np.all(errors >= 0), "Errors should be non-negative"

        # Test pixel scale calculation
        pixel_scale = photometry.get_pixel_scale(header)
        assert pixel_scale > 0, "Pixel scale should be positive"

        # Test background fitting
        bkg_fit = photometry.fit_background(radii, profile, [10, -5])
        assert len(bkg_fit) == len(radii), "Background fit length mismatch"

    @pytest.mark.skipif(not CONFIG_FILE.exists(), reason="Test config not available")
    def test_config_loading_real_files(self):
        """Test configuration loading with real file paths."""

        config = utils.load_config(str(CONFIG_FILE))

        # Verify config structure
        assert "data_directory" in config
        assert "stacking_params" in config
        assert "files_to_stack" in config["stacking_params"]

        # Verify file paths exist (if specified as absolute paths)
        data_dir = Path(config["data_directory"])
        if data_dir.is_absolute():
            assert data_dir.exists(), f"Data directory {data_dir} not found"
