# Telemetry Logging & Statistics
"""Handles saving historical telemetry data to 
files and calculating statistical summaries (min, max, average)."""

# Imports
import csv, datetime,os
from monitor import system_diagnostic, validate_threshold


def record_keeper(cpu,ram,disk):
    """Appends timestamped telemetry data and health status to the CSV log.

    Checks if the telemetry log file exists; if not, creates it and writes 
    the header row. Appends a new timestamped row containing CPU, RAM, 
    and Disk usage percentages alongside their evaluated status."""

    raw_timestamp = datetime.datetime.now()
    partial_timestamp = raw_timestamp.strftime("%Y-%m-%d %H:%M:%S")
    timestamp = partial_timestamp

    file_name = 'telemetry_log.csv'
    header = ["Timestamp", "CPU %", "RAM %", "Disk %", "Status"]
    status = validate_threshold(cpu,ram,disk)
    row_data = [timestamp, cpu["Usage %"], ram["Usage %"],disk["Usage %"],status]

    if not os.path.exists(file_name):
        with open(file_name,'w', newline="", encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(header) 
            writer.writerow(row_data)

    else:
        with open(file_name, 'a', newline="", encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(row_data)


def data_cruncher(file_name):
    """Processes historical telemetry logs to compute statistical summaries.

    Reads the specified CSV log file, parses usage records, and calculates 
    the minimum, maximum, and average usage percentages for CPU, RAM, and Disk."""

    if not os.path.exists(file_name):
        return f"File name: {file_name} Not Found"
    
    try:

        with open(file_name,'r', newline="", encoding='utf-8') as file:
            reader = csv.reader(file)
            skip_header = next(reader)

            count = 0

            cpu_values = []
            ram_values = []
            disk_values = []

            for data_row in reader:

                if len(data_row) >= 4:
                    cpu_values.append(float(data_row[1]))
                    ram_values.append(float(data_row[2]))
                    disk_values.append(float(data_row[3]))
                    count += 1

            if count > 0:
                metrics = {

                    "cpu": {"max": max(cpu_values),
                            "min": min(cpu_values),
                            "avg": sum(cpu_values) / count
                    },
                    "ram": {"max": max(ram_values),
                            "min": min(ram_values),
                            "avg": sum(ram_values) / count
                    },
                    "disk": {"max": max(disk_values),
                            "min": min(disk_values),
                            "avg": sum(disk_values) / count
                    }

                }
                
            if count == 0:
                return f"The File is empty"

            return metrics

    except:
        print("No historical data recorded yet")