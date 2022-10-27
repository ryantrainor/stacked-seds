import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from typing import Dict, Any


def plot_radial_profiles(results: Dict[str, Any], title: str, output_path: str) -> None:
    """
    Generates and saves a grid of radial profile plots.

    Args:
        results (Dict[str, Any]): A dictionary where keys are filenames and values
                                  are dictionaries of photometry results.
        title (str): The main title for the entire plot figure.
        output_path (str): The path to save the output PDF file.
    """
    n_plots = len(results)
    if n_plots == 0:
        print("No results to plot.")
        return

    n_cols = min(4, n_plots)
    n_rows = (n_plots + n_cols - 1) // n_cols  # Calculate required rows

    fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 4 * n_rows), squeeze=False)

    # Flatten the axes array for easy iteration
    ax_flat = axes.flatten()

    for i, (filename, data) in enumerate(results.items()):
        ax = ax_flat[i]

        # Unpack data
        radii_arcsec = data["radii_arcsec"]
        profile_sb = data["profile_sb"]
        error_sb = data["error_sb"]
        bkg_fit_sb = data["bkg_fit_sb"]

        # Plotting
        ax.plot(
            radii_arcsec,
            profile_sb,
            marker="o",
            markersize=2.5,
            linewidth=1,
            label="Data",
        )
        ax.errorbar(
            radii_arcsec,
            profile_sb,
            yerr=error_sb,
            fmt="none",
            ecolor="b",
            capsize=2,
            elinewidth=1,
            alpha=0.7,
        )
        ax.plot(
            radii_arcsec,
            bkg_fit_sb,
            color="red",
            linestyle="dashed",
            linewidth=1.5,
            label="Bkg Fit",
        )

        ax.set_title(filename.replace("_NEW.fits", "").replace(".reg", ""), size=12)
        ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
        ax.tick_params(axis="both", labelsize=10)

    # Set common labels and add legend to the first plot
    ax_flat[0].legend()
    for row in range(n_rows):
        axes[row, 0].set_ylabel("Surface Brightness (flux/arcsec²)")
    for col in range(n_cols):
        axes[n_rows - 1, col].set_xlabel("Radius (arcsec)")

    # Hide unused subplots
    for i in range(len(results), len(ax_flat)):
        ax_flat[i].set_visible(False)

    fig.suptitle(title, size=16)
    fig.tight_layout(rect=(0, 0.03, 1, 0.97))  # Adjust for suptitle and labels

    plt.savefig(output_path, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved summary plot to {output_path}")
