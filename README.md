# Stacked SEDs

[![CI/CD Pipeline](https://github.com/ryantrainor/stacked-seds/workflows/CI/CD%20Pipeline/badge.svg)](https://github.com/oabraham1/stacked-seds/actions)
[![Documentation](https://img.shields.io/badge/docs-github%20pages-blue)](https://stacked-seds.readthedocs.io/)
[![PyPI version](https://badge.fury.io/py/stacked-seds.svg)](https://badge.fury.io/py/stacked-seds)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python package for stacking faint galaxy images from multiple broadband filters and preparing them for Spectral Energy Distribution (SED) analysis.

## Key Features

- **Galaxy Image Stacking**: Robust stacking of hundreds of faint galaxy cutouts using trimmed mean statistics
- **Error Propagation**: Automatic calculation of uncertainty maps using Median Absolute Deviation (MAD)
- **Radial Photometry**: Azimuthally averaged surface brightness profiles with background subtraction
- **Publication-Ready Plots**: Automated generation of multi-filter comparison plots
- **Command-Line Tools**: Simple `sed-stack` and `sed-photom` commands for easy workflow execution

## Quick Start

### Installation

```bash
pip install stacked-seds
```

### Basic Usage

```bash
# 1. Create configuration file
cp config/params.yml my_config.yml

# 2. Edit my_config.yml with your data paths

# 3. Run stacking workflow
sed-stack my_config.yml
sed-photom my_config.yml
```

### Example

```python
from stacked_seds import stacking, photometry

# Load and stack galaxy images
pixel_coords = stacking.get_galaxy_pixel_coords("image.fits", "galaxies.reg")
stamps = stacking.create_stamps(image_data, wcs_obj, pixel_coords)
stacked_image, error_map = stacking.stack_images(stamps)

# Perform radial photometry
radii, profile, errors = photometry.get_radial_profile(stacked_image, center)
```

## Documentation

- **Full Documentation**: [https://ryantrainor.github.io/stacked-seds/](https://ryantrainor.github.io/stacked-seds/)
- **API Reference**: [API Documentation](https://ryantrainor.github.io/stacked-seds/api.html)
- **Tutorial**: [Getting Started Guide](https://stacked-seds.readthedocs.io/en/latest/tutorial.html)
- **Examples**: See the [examples/](examples/) directory

## Requirements

- Python ≥ 3.8
- NumPy ≥ 1.20.0
- SciPy ≥ 1.7.0
- Astropy ≥ 5.0.0
- Matplotlib ≥ 3.5.0
- PhotoUtils ≥ 1.5.0

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

```bash
git clone https://github.com/ryantrainor/stacked-seds.git
cd stacked-seds
pip install -e ".[dev]"
make test
```

## Citation

If you use this software in your research, please cite:

```bibtex
@software{stacked_seds,
  title={Stacked SEDs: Galaxy Image Stacking and Photometry},
  author={Abraham, O. and Chapman, C. and Garcia, E. and Trainor, R.},
  year={2025},
  url={https://github.com/ryantrainor/stacked-seds},
  doi={10.5281/zenodo.XXXXXX}
}
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- **Issues**: [GitHub Issues](https://github.com/ryantrainor/stacked-seds/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ryantrainor/stacked-seds/discussions)
- **Email**: ryan.trainor@fandm.edu

## Acknowledgments

This project was developed at Franklin & Marshall College. We thank the astronomy community for their valuable feedback and contributions.
