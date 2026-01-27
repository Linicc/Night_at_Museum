#!/usr/bin/env python
"""Setup script to create Excel configuration template."""
import os
import sys

def setup():
    """Create Excel template if it doesn't exist."""
    config_dir = "config"
    config_file = os.path.join(config_dir, "museum_ca_config.xlsx")

    if os.path.exists(config_file):
        print(f"Config file already exists: {config_file}")
        return

    os.makedirs(config_dir, exist_ok=True)

    try:
        from io_manager.excel_parser import create_empty_config_template
        create_empty_config_template(config_file)
        print(f"Created Excel template: {config_file}")
        print("\nYou can now:")
        print(f"1. Edit {config_file} to configure your simulation:")
        print("   - Set walls (value: 2)")
        print("   - Set exits (value: 3)")
        print("   - Set entrances (value: 4)")
        print("   - Set exhibits (value: 5)")
        print(f"2. Run: python main_ca.py")
    except Exception as e:
        print(f"Error creating template: {e}")
        sys.exit(1)

if __name__ == "__main__":
    setup()
