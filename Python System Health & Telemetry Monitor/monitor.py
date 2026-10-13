# Telemetry & System Metadata Engine
"""The core telemetry engine responsible for fetching 
live CPU, RAM, disk usage, uptime, and system metadata."""

# Imports
import psutil,platform, socket, datetime,time
from config import DEFAULT_SETTINGS


def system_diagnostic():
    """Fetches current system performance metrics.

    Retrieves real-time usage percentages for CPU, RAM, and Disk
    using system monitoring utilities."""
    
    root_path = "C:\\" if platform.system() == "Windows" else "/"

    memory = psutil.virtual_memory()
    disk_info = psutil.disk_usage(root_path)

    boot_time_timestamp = psutil.boot_time()
    boot_time = datetime.datetime.fromtimestamp(boot_time_timestamp)

    uptime_seconds = time.time() - boot_time_timestamp
    uptime = datetime.timedelta(seconds=int(uptime_seconds))
    metadata = {
        "OS": platform.system(),
        "OS Release": platform.release(),
        "OS Version": platform.version(),
        "Architecture": platform.machine(),
        "Hostname": platform.node(),
        "Uptime": str(uptime),
        "Boot Time": boot_time.strftime("%Y-%m-%d %H:%M:%S")
    }

    cpu = {
        "Physical Core": psutil.cpu_count(logical=False),
        "Total Cores": psutil.cpu_count(logical=True),

        "Usage %": psutil.cpu_percent(interval=2),
        "Usage per Core": psutil.cpu_percent(interval=0, percpu=True),
        "Frequency (MHz)": psutil.cpu_freq().current if psutil.cpu_freq() else "N/A"
    }

    ram = {
        "Total (GB)": round(memory.total / (1024**3), 2),
        "Available (GB)": round(memory.available / (1024**3), 2),
        "Used (GB)": round(memory.used / (1024**3), 2),
        "Usage %": memory.percent
    }

    disk = {
        "Total (GB)": round(disk_info.total / (1024**3), 2),
        "Used (GB)": round(disk_info.used / (1024**3), 2),
        "Free (GB)": round(disk_info.free / (1024**3), 2),
        "Usage %": disk_info.percent
    }

    validate_threshold()

    return {"Metadata": metadata, "CPU": cpu, "RAM": ram, "Disk": disk }


def validate_threshold(cpu,ram,disk):
    """Evaluates system component usage against configured thresholds.

    Compares live CPU, RAM, and Disk metrics against safety limits
    defined in configuration settings to determine overall health status."""

    if (cpu["Usage %"] >= DEFAULT_SETTINGS["critical_threshold"] or
        ram["Usage %"] >= DEFAULT_SETTINGS["critical_threshold"] or
        disk["Usage %"] >= DEFAULT_SETTINGS["critical_threshold"]):
        return "CRITICAL"
    
    elif (cpu["Usage %"] >= DEFAULT_SETTINGS["warning_threshold"] or
          ram["Usage %"] >= DEFAULT_SETTINGS["warning_threshold"] or
          disk["Usage %"] >= DEFAULT_SETTINGS["warning_threshold"]):
        return "WARNING"
    
    else:
        return "Normal"