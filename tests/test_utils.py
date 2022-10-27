import pytest
from stacked_seds import utils
from pathlib import Path
from typing import Dict, Any


def test_load_config_success(tmp_path: Path) -> None:
    """
    Tests that the config loader successfully reads a valid YAML file.
    """
    # Create a temporary config file
    config_content: str = """
data_directory: "test/data"
stacking_params:
  stamp_size: 101
"""
    config_path: Path = tmp_path / "test_config.yml"
    config_path.write_text(config_content)

    # Load the config
    config: Dict[str, Any] = utils.load_config(str(config_path))

    # Assertions
    assert config["data_directory"] == "test/data"
    assert config["stacking_params"]["stamp_size"] == 101


def test_load_config_file_not_found() -> None:
    """
    Tests that the config loader handles a missing file gracefully by exiting.
    """
    with pytest.raises(SystemExit) as e:
        utils.load_config("non_existent_file.yml")

    # Check that the exit code is 1, indicating an error
    assert e.type == SystemExit
    assert e.value.code == 1


def test_load_config_bad_yaml(tmp_path: Path) -> None:
    """
    Tests that the config loader handles a poorly formatted YAML file.
    """
    # Create an invalid YAML file (e.g., with a tab character)
    bad_config_content: str = "key:\t- invalid_yaml"
    config_path: Path = tmp_path / "bad_config.yml"
    config_path.write_text(bad_config_content)

    with pytest.raises(SystemExit) as e:
        utils.load_config(str(config_path))

    assert e.type == SystemExit
    assert e.value.code == 1
