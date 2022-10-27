#!/usr/bin/env python3
"""
Test the complete command-line workflow with test data.
"""

import os
import subprocess
import sys
from pathlib import Path


def test_command_line_workflow():
    """Test the complete sed-stack and sed-photom workflow."""

    # Ensure we're in the right directory
    project_root = Path(__file__).parent
    os.chdir(project_root)

    # Check if test data exists
    test_config = Path("tests/data/test_config.yml")
    if not test_config.exists():
        print("❌ Test data not found. Run: python create_test_data.py")
        return False

    print("🧪 Testing complete command-line workflow...")
    print(f"📁 Working directory: {Path.cwd()}")
    print(f"⚙️  Config file: {test_config}")

    # Test sed-stack command
    print("\n--- Testing sed-stack ---")
    try:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "stacked_seds.scripts.run_stacking",
                str(test_config),
            ],
            capture_output=True,
            text=True,
            timeout=60,
        )

        if result.returncode == 0:
            print("✅ sed-stack completed successfully")
            print("Output:", result.stdout)
        else:
            print("❌ sed-stack failed")
            print("Error:", result.stderr)
            return False

    except subprocess.TimeoutExpired:
        print("❌ sed-stack timed out")
        return False
    except Exception as e:
        print(f"❌ sed-stack error: {e}")
        return False

    # Check if stacked file was created
    output_file = Path("tests/data/output/test_image_NEW.fits")
    if output_file.exists():
        print(f"✅ Stacked file created: {output_file}")
    else:
        print(f"❌ Stacked file not found: {output_file}")
        return False

    # Test sed-photom command
    print("\n--- Testing sed-photom ---")
    try:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "stacked_seds.scripts.run_photometry",
                str(test_config),
            ],
            capture_output=True,
            text=True,
            timeout=60,
        )

        if result.returncode == 0:
            print("✅ sed-photom completed successfully")
            print("Output:", result.stdout)
        else:
            print("❌ sed-photom failed")
            print("Error:", result.stderr)
            return False

    except subprocess.TimeoutExpired:
        print("❌ sed-photom timed out")
        return False
    except Exception as e:
        print(f"❌ sed-photom error: {e}")
        return False

    # Check if plot was created
    plot_file = Path("tests/data/plots/test_plot.pdf")
    if plot_file.exists():
        print(f"✅ Plot file created: {plot_file}")
    else:
        print(f"❌ Plot file not found: {plot_file}")
        return False

    print("\n🎉 Complete workflow test PASSED!")
    return True


def test_entry_points():
    """Test the installed entry points (if package is installed)."""

    print("\n🔌 Testing entry points...")

    # Test sed-stack entry point
    try:
        result = subprocess.run(
            ["sed-stack", "--help"], capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            print("✅ sed-stack entry point works")
        else:
            print("❌ sed-stack entry point failed")
            return False
    except FileNotFoundError:
        print("⚠️  sed-stack entry point not found (package not installed)")
        return False
    except Exception as e:
        print(f"❌ sed-stack entry point error: {e}")
        return False

    # Test sed-photom entry point
    try:
        result = subprocess.run(
            ["sed-photom", "--help"], capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            print("✅ sed-photom entry point works")
        else:
            print("❌ sed-photom entry point failed")
            return False
    except FileNotFoundError:
        print("⚠️  sed-photom entry point not found (package not installed)")
        return False
    except Exception as e:
        print(f"❌ sed-photom entry point error: {e}")
        return False

    print("✅ Entry points test PASSED!")
    return True


if __name__ == "__main__":
    print("=" * 60)
    print("🧪 STACKED SEDS WORKFLOW TESTING")
    print("=" * 60)

    # Test the workflow using module calls
    success1 = test_command_line_workflow()

    # Test entry points if installed
    success2 = test_entry_points()

    if success1:
        print("\n🎉 All workflow tests PASSED!")

        if success2:
            print("🎉 All entry point tests PASSED!")
        else:
            print(
                "⚠️  Entry points not working (install package with: pip install -e .)"
            )

    else:
        print("\n❌ Workflow tests FAILED!")
        sys.exit(1)
