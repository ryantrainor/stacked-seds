import numpy as np
from stacked_seds import stacking
from astropy.io import fits
from astropy import wcs


def test_create_stamps(dummy_wcs_header: fits.Header) -> None:
    """
    Tests the stamp creation logic.
    - One coordinate should be valid.
    - One coordinate should be too close to the edge and be rejected.
    """
    image_data = np.zeros((200, 200))
    image_data[95:105, 95:105] = 100  # A 10x10 bright square at the center
    wcs_obj = wcs.WCS(dummy_wcs_header)

    # Define pixel coordinates: one valid, one at the edge
    pixel_coords = np.array([[100, 100], [5, 5]])

    stamps = stacking.create_stamps(image_data, wcs_obj, pixel_coords, stamp_size=51)

    assert stamps.shape[0] == 1, "Should only create one valid stamp"
    assert stamps[0].shape == (51, 51), "Stamp should have the correct dimensions"
    # Assert the center of the stamp is the brightest part
    assert np.sum(stamps[0][20:30, 20:30]) > np.sum(stamps[0][0:10, 0:10])


def test_stack_images() -> None:
    """
    Tests the stacking and error calculation logic with a predictable dataset.
    """
    # Create three simple 3x3 stamps
    stamp1 = np.ones((3, 3)) * 10
    stamp2 = np.ones((3, 3)) * 20
    stamp3 = np.ones((3, 3)) * 30

    # Add an outlier to the first stamp for trim_mean test
    stamp1[1, 1] = 1000

    stamps = np.array([stamp1, stamp2, stamp3])

    # Test with a smaller trim fraction that will handle the outlier appropriately
    # With trim_fraction=0.2, for 3 values: 0.2 * 3 = 0.6, so no values are trimmed
    # Let's use more stamps to demonstrate trimming better
    stamp4 = np.ones((3, 3)) * 15
    stamp5 = np.ones((3, 3)) * 25
    stamps_extended = np.array([stamp1, stamp2, stamp3, stamp4, stamp5])

    # With 5 stamps and trim_fraction=0.2:
    # For corner pixels: [10, 20, 30, 15, 25] -> sorted [10, 15, 20, 25, 30]
    # Trim 20% from each end (1 value each) -> [15, 20, 25] -> mean = 20
    # For center pixel: [1000, 20, 30, 15, 25] -> sorted [15, 20, 25, 30, 1000]
    # Trim 20% from each end -> [20, 25, 30] -> mean = 25
    stacked_with_trim, error_map = stacking.stack_images(
        stamps_extended, trim_fraction=0.2
    )

    assert stacked_with_trim.shape == (3, 3)
    assert error_map.shape == (3, 3)
    assert np.isclose(stacked_with_trim[0, 0], 20)  # Mean of [15, 20, 25]
    assert np.isclose(
        stacked_with_trim[1, 1], 25
    )  # Mean of [20, 25, 30] (outlier trimmed)

    # Test with no trimming for comparison
    stacked_no_trim, _ = stacking.stack_images(stamps, trim_fraction=0.0)
    assert stacked_no_trim[0, 0] == 20  # Mean of [10, 20, 30]
    assert stacked_no_trim[1, 1] == 350  # Mean of [1000, 20, 30] - outlier included
