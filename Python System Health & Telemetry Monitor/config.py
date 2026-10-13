# Configuration Management
"""Manages loading, saving, and modifying 
user-defined warning and critical thresholds."""

# Imports
import json,os

CONFIG_FILE = "config.json"

DEFAULT_SETTINGS = {
    "warning_threshold": 80.0,
    "critical_threshold": 90.0,
    "check_interval_seconds": 2
}


def generate_settings():
    """Generates and initializes default configuration settings.

    Creates initial configuration files or default setting structures 
    required for system monitoring parameters (such as check intervals 
    and warning/critical thresholds) if they do not already exist."""

    if os.path.exists(CONFIG_FILE):
        print(f"Loading existing setting file from {CONFIG_FILE}")

        try:
            with open(CONFIG_FILE, 'r') as file:
                data = json.load(file)
                return data

        except json.JSONDecodeError:
            print("Error parsing JSON file, Falling back to default values")
            return DEFAULT_SETTINGS
        
    else:
        print(f"{CONFIG_FILE} not Found, creating new file with default values")

        try:
            with open(CONFIG_FILE, 'w') as file:
                json.dump(DEFAULT_SETTINGS, file, indent=4)
                return DEFAULT_SETTINGS
            
        except IOError as e:
            print(f"Failed to create config file: {e}. Running on runtime defaults.")
            return DEFAULT_SETTINGS