# CLI Menu & Control Loop
"""The application entry point that runs the 
main interactive CLI menu and coordinates the program loop."""

# Imports
import time,os,sys
from logger import record_keeper, data_cruncher
from config import DEFAULT_SETTINGS
from monitor import system_diagnostic, validate_threshold


def telemetry_dashboard():
    """Displays the main menu options, accepts user input, 
    and routes the user to either the live monitor, the analytics report, or exits the application."""

    print("Welcome to the System Health & Telemetry Monitor")

    while True:

        print("\n--- Telemetry Dashboard ---")
        print("[1] Launch Telemetry Nexus (Live Monitoring)")
        print("[2] Access Telemetry Archives (Historical Analytics)")
        print("[3] Exit System")

        choice = input("Select an option (1-3): ")

        if choice == "1":
            telemetry_nexus()

        elif choice == "2":
            telemetry_archives()

        elif choice == "3":
            print("Exiting Program.")
            break

        else:
            print("Invalid Choice. Enter a number from 1 to 3.")


def telemetry_nexus():
    """Manages the active monitoring loop, fetches live stats using diagnostics, calls record_keeper() to log them, 
    and prints the real-time dashboard view to the console at configured time intervals."""

    refresh_interval = DEFAULT_SETTINGS.get("check_interval_seconds")

    print("\n--- Telemetry Nexus (Status/Stats) ---")

    print("Press Ctrl+C To Stop Program")

    try: 
        
        while True:

            current_stats = system_diagnostic()

            cpu = current_stats["cpu"]
            ram = current_stats["ram"]
            disk = current_stats["disk"]

            status = validate_threshold(cpu,ram,disk)

            record_keeper(cpu,ram,disk)

            print(f"CPU: {cpu['Usage']}%, {status}")
            print(f"RAM: {ram['Usage']}%, {status}")
            print(f"DISK: {disk['Usage']}%, {status}")

            time.sleep(refresh_interval)            

    except KeyboardInterrupt:
        print("\nMonitoring Interrupted By User")


def telemetry_archives():
    """Calls data_cruncher(), checks whether it returned a warning message (like a missing or empty file) or statistics dictionary, 
    and formats the output into a clean, readable report for the user."""

    file_name = 'telemetry_log.csv'

    result = data_cruncher(file_name)

    if isinstance(result, str):

        print(f"\n[!] Notice: {result}")
        print("Launch Telemetry Nexus First")
        return

    elif isinstance(result,dict):

        print("\n--- Telemetry Archives ---")

        for name,stats in result.items():

            max_metrics = stats['max']
            min_metrics = stats['min']
            avg_metrics = stats['avg']

            print(f"{name:<15} | {max_metrics:>10.2f} | {min_metrics:>10.2f} | {avg_metrics:>10.2f}")

    else:
        print("Error: Unexpected data format returned from result ")