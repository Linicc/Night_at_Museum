#!/usr/bin/env python
"""Check if all CA system modules are properly installed and importable."""
import sys

def check_imports():
    """Check if all required modules can be imported."""
    modules_to_check = [
        ("numpy", "numpy"),
        ("matplotlib", "matplotlib"),
        ("pandas", "pandas"),
        ("openpyxl", "openpyxl"),
        ("core.ca.ca_grid", "CA Grid Module"),
        ("core.ca.ca_agent", "CA Agent Module"),
        ("core.ca.ca_environment", "CA Environment Module"),
        ("core.ca.ca_behaviors", "CA Behaviors Module"),
        ("core.ca.ca_engine", "CA Engine Module"),
        ("io_manager.excel_parser", "Excel Parser Module"),
        ("io_manager.excel_writer", "Excel Writer Module"),
        ("analysis.ca_logger", "CA Logger Module"),
        ("config.ca_settings", "CA Settings Module"),
    ]

    print("Checking CA System Dependencies...")
    print("=" * 50)

    all_ok = True
    for module_name, description in modules_to_check:
        try:
            __import__(module_name)
            print(f"✓ {description:30s} OK")
        except ImportError as e:
            print(f"✗ {description:30s} FAILED: {e}")
            all_ok = False

    print("=" * 50)

    if all_ok:
        print("\n✓ All modules ready! You can run:")
        print("  python test_ca_demo.py    # Quick demo")
        print("  python setup_ca.py         # Create Excel template")
        print("  python main_ca.py          # Full simulation")
        return 0
    else:
        print("\n✗ Some modules are missing. Install with:")
        print("  pip install -r requirements.txt")
        return 1


if __name__ == "__main__":
    sys.exit(check_imports())
