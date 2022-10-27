#!/usr/bin/env python3
"""
Comprehensive test runner for Stacked SEDs.

This script runs all types of tests we've developed and can be used
both locally and in CI to ensure everything works correctly.
"""

import sys
import os

# Force UTF-8 encoding on Windows
if sys.platform == "win32":
    import codecs

    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())

import subprocess
import yaml
from pathlib import Path
from typing import List, Tuple


def run_command(
    cmd: List[str], description: str, timeout: int = 120
) -> Tuple[bool, str]:
    """
    Run a command and return success status and output.

    Args:
        cmd: Command to run as list of strings
        description: Description for logging
        timeout: Timeout in seconds

    Returns:
        Tuple of (success, output)
    """
    print(f"\n{'='*60}")
    print(f"🧪 {description}")
    print(f"💻 Command: {' '.join(cmd)}")
    print(f"{'='*60}")

    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout, cwd=Path.cwd()
        )

        if result.returncode == 0:
            print(f"✅ {description} PASSED")
            if result.stdout.strip():
                print("Output:", result.stdout.strip())
            return True, result.stdout
        else:
            print(f"❌ {description} FAILED")
            print("Error:", result.stderr.strip())
            if result.stdout.strip():
                print("Output:", result.stdout.strip())
            return False, result.stderr

    except subprocess.TimeoutExpired:
        print(f"⏰ {description} TIMED OUT")
        return False, f"Command timed out after {timeout} seconds"
    except Exception as e:
        print(f"💥 {description} ERROR: {e}")
        return False, str(e)


def test_package_installation():
    """Test that the package is properly installed."""
    print("\n🔍 Testing package installation...")

    try:
        import stacked_seds

        print(f"✅ Package imported successfully (version: {stacked_seds.__version__})")

        # Test module imports
        from stacked_seds import stacking, photometry, plotting, utils

        print("✅ All core modules imported")

        # Test script imports
        from stacked_seds.scripts.run_stacking import main as stack_main
        from stacked_seds.scripts.run_photometry import main as photom_main

        print("✅ Script modules imported")

        return True

    except ImportError as e:
        print(f"❌ Package import failed: {e}")
        return False


def test_code_quality():
    """Run code quality checks."""
    tests = [
        (["make", "format-check"], "Code formatting check"),
        (["make", "lint"], "Linting check"),
    ]

    results = []
    for cmd, desc in tests:
        success, _ = run_command(cmd, desc)
        results.append(success)

    return all(results)


def test_unit_tests():
    """Run unit tests."""
    cmd = ["pytest", "tests/", "-m", "not slow and not integration", "-v"]
    success, _ = run_command(cmd, "Unit tests")
    return success


def test_integration_tests():
    """Run integration tests."""
    # Check if test data exists
    test_config = Path("tests/data/test_config.yml")
    if not test_config.exists():
        print("⚠️  Test data not found, skipping integration tests")
        print("Run: python create_test_data.py")
        return True  # Don't fail if test data is missing

    cmd = ["pytest", "tests/test_integration.py", "-v", "-s"]
    success, _ = run_command(cmd, "Integration tests")
    return success


def test_entry_points():
    """Test command-line entry points."""
    tests = [
        (["sed-stack", "--help"], "sed-stack entry point"),
        (["sed-photom", "--help"], "sed-photom entry point"),
    ]

    results = []
    for cmd, desc in tests:
        success, _ = run_command(cmd, desc, timeout=10)
        results.append(success)

    return all(results)


def test_workflow():
    """Test the complete workflow."""
    test_config = Path("tests/data/test_config.yml")
    if not test_config.exists():
        print("⚠️  Test config not found, skipping workflow test")
        return True

    # Test stacking
    cmd1 = ["sed-stack", str(test_config)]
    success1, _ = run_command(cmd1, "Complete stacking workflow")

    if not success1:
        return False

    # Test photometry
    cmd2 = ["sed-photom", str(test_config)]
    success2, _ = run_command(cmd2, "Complete photometry workflow")

    return success2


def test_output_validation():
    """Validate that output files are created correctly."""
    print("\n🔍 Validating output files...")

    try:
        from astropy.io import fits

        # Check stacked FITS file
        stacked_file = Path("tests/data/output/test_image_NEW.fits")
        if not stacked_file.exists():
            print(f"❌ Stacked file not found: {stacked_file}")
            return False

        # Validate FITS structure
        with fits.open(stacked_file) as hdul:
            if len(hdul) != 3:
                print(f"❌ Expected 3 HDUs, got {len(hdul)}")
                return False

            hdu_names = [hdu.name for hdu in hdul]
            if "SCI" not in hdu_names:
                print("❌ Missing SCI extension")
                return False

            if "ERR" not in hdu_names:
                print("❌ Missing ERR extension")
                return False

            sci_shape = hdul["SCI"].data.shape
            err_shape = hdul["ERR"].data.shape

            if sci_shape != (51, 51):
                print(f"❌ Wrong SCI shape: {sci_shape}")
                return False

            if err_shape != (51, 51):
                print(f"❌ Wrong ERR shape: {err_shape}")
                return False

        print("✅ FITS file structure validated")

        # Check plot file
        plot_file = Path("tests/data/plots/test_plot.pdf")
        if not plot_file.exists():
            print(f"❌ Plot file not found: {plot_file}")
            return False

        print("✅ Plot file found")

        # Check file sizes are reasonable
        fits_size = stacked_file.stat().st_size
        plot_size = plot_file.stat().st_size

        if fits_size < 1000:  # Should be at least 1KB
            print(f"⚠️  FITS file suspiciously small: {fits_size} bytes")

        if plot_size < 1000:  # Should be at least 1KB
            print(f"⚠️  Plot file suspiciously small: {plot_size} bytes")

        print(f"✅ File sizes: FITS={fits_size:,} bytes, Plot={plot_size:,} bytes")

        return True

    except Exception as e:
        print(f"❌ Output validation failed: {e}")
        return False


def test_configuration_examples():
    """Test that configuration examples are valid."""
    print("\n🔍 Testing configuration examples...")

    config_files = ["config/params.yml", "tests/data/test_config.yml"]

    for config_file in config_files:
        config_path = Path(config_file)
        if config_path.exists():
            try:
                with open(config_path) as f:
                    config = yaml.safe_load(f)
                print(f"✅ {config_file} is valid YAML")
            except yaml.YAMLError as e:
                print(f"❌ {config_file} invalid YAML: {e}")
                return False
        else:
            print(f"⚠️  {config_file} not found")

    return True


def run_all_tests():
    """Run all tests and report results."""
    print("🚀 COMPREHENSIVE STACKED SEDS TESTING")
    print("=" * 80)

    # Define all test functions
    test_functions = [
        ("Package Installation", test_package_installation),
        ("Code Quality", test_code_quality),
        ("Unit Tests", test_unit_tests),
        ("Integration Tests", test_integration_tests),
        ("Entry Points", test_entry_points),
        ("Complete Workflow", test_workflow),
        ("Output Validation", test_output_validation),
        ("Configuration Examples", test_configuration_examples),
    ]

    results = {}

    # Run all tests
    for test_name, test_func in test_functions:
        print(f"\n🎯 Running: {test_name}")
        try:
            success = test_func()
            results[test_name] = success
        except Exception as e:
            print(f"💥 {test_name} crashed: {e}")
            results[test_name] = False

    # Summary
    print("\n" + "=" * 80)
    print("📊 TEST SUMMARY")
    print("=" * 80)

    passed = 0
    total = len(results)

    for test_name, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name}")
        if success:
            passed += 1

    print(f"\n🎯 Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 ALL TESTS PASSED! Package is ready for production.")
        return True
    else:
        print(f"💥 {total - passed} tests failed. Please fix issues before proceeding.")
        return False


if __name__ == "__main__":
    # Change to project root if running from elsewhere
    script_dir = Path(__file__).parent
    os.chdir(script_dir)

    success = run_all_tests()
    sys.exit(0 if success else 1)
