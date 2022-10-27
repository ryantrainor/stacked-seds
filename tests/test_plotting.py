import numpy as np
from stacked_seds import plotting
from pathlib import Path
from typing import Dict, Any


def test_plot_radial_profiles(tmp_path: Path) -> None:
    """
    Tests that the plotting function runs without errors and creates an output file.
    It does not check the visual content of the plot.
    """
    # Create a dummy results dictionary, mimicking the output of the photometry script
    results: Dict[str, Any] = {
        "filter1_NEW.fits": {
            "radii_arcsec": np.arange(10),
            "profile_sb": np.linspace(100, 10, 10),
            "error_sb": np.ones(10) * 2,
            "bkg_fit_sb": np.ones(10) * 5,
        },
        "filter2_NEW.fits": {
            "radii_arcsec": np.arange(15),
            "profile_sb": np.linspace(200, 5, 15),
            "error_sb": np.ones(15) * 4,
            "bkg_fit_sb": np.ones(15) * 10,
        },
    }

    output_plot_path: Path = tmp_path / "test_plot.pdf"

    # Run the plotting function
    plotting.plot_radial_profiles(
        results, title="Test Plot", output_path=str(output_plot_path)
    )

    # The primary test is to ensure the output file was created
    assert output_plot_path.exists()
