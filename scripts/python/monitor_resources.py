from azure.identity import AzureCliCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.monitor import MonitorManagementClient
from datetime import datetime, timedelta

import logging
import sys
import os
import time

# ==============================
# PROJECT PATH CONFIGURATION
# ==============================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

output_dir = os.path.join(BASE_DIR, "outputs")

# ==========================================
# OUTPUT DIRECTORY
# ==========================================

os.makedirs(output_dir, exist_ok=True)

# ==========================================
# OUTPUT FILE
# ==========================================

script_name = os.path.splitext(
    os.path.basename(__file__)
)[0]

output_file = os.path.join(
    output_dir,
    f"{script_name}_output.txt"
)

# ==========================================
# TEE OUTPUT CLASS
# ==========================================

class Tee:

    def __init__(self, *files):
        self.files = files

    def write(self, obj):
        for file in self.files:
            file.write(obj)
            file.flush()

    def flush(self):
        for file in self.files:
            file.flush()



# ==========================================
# OUTPUT STREAM
# ==========================================

output_stream = open(
    output_file,
    "w",
    encoding="utf-8"
)

# ==========================================
# DUPLICATE OUTPUT
# ==========================================

sys.stdout = Tee(sys.stdout, output_stream)

sys.stderr = Tee(sys.stderr, output_stream)

# Logs folder
log_dir = os.path.join(BASE_DIR, 'logs')
os.makedirs(log_dir, exist_ok=True)

# Monitoring log file
log_file = os.path.join(log_dir, 'advanced_monitoring.log')

# ==============================
# LOGGING CONFIGURATION
# ==============================

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)

# ==========================================
# START EXECUTION TIMER
# ==========================================

execution_start = datetime.now()
start_time = time.time()

print(
    f"Execution Started At: "
    f"{execution_start.strftime('%Y-%m-%d %H:%M:%S')}"
)

print("=" * 50)

# ==============================
# AZURE CONFIGURATION
# ==============================

subscription_id = "a8bd7b1b-b9aa-4283-aec4-2040b847d926"

resource_group = "AutoProjectRG"
vm_name = "ProductionUbuntuVM"

# ==============================
# MAIN MONITORING LOGIC
# ==============================

try:

    logging.info("Monitoring script started")

    credential = AzureCliCredential()

    compute_client = ComputeManagementClient(
        credential,
        subscription_id
    )

    monitor_client = MonitorManagementClient(
        credential,
        subscription_id
    )

    # ==============================
    # GET VM DETAILS
    # ==============================

    vm = compute_client.virtual_machines.get(
        resource_group,
        vm_name
    )

    print("\nVM INFORMATION")
    print("=" * 50)

    print(f"VM Name : {vm.name}")
    print(f"Location : {vm.location}")
    print(f"VM Size : {vm.hardware_profile.vm_size}")

    logging.info(f"VM Name: {vm.name}")
    logging.info(f"VM Location: {vm.location}")
    logging.info(f"VM Size: {vm.hardware_profile.vm_size}")

    # ==============================
    # VM STATUS
    # ==============================

    instance_view = compute_client.virtual_machines.instance_view(
        resource_group,
        vm_name
    )

    print("\nVM STATUS")
    print("=" * 50)

    for status in instance_view.statuses:

        print(status.display_status)

        logging.info(f"VM Status: {status.display_status}")

    # ==============================
    # METRIC COLLECTION TIME
    # ==============================

    # Metric collection time

    metric_end_time = datetime.utcnow()

    metric_start_time = (
        metric_end_time - timedelta(hours=1)
    )

    resource_id = vm.id

    # ==============================
    # CPU METRICS
    # ==============================

    metrics_data = monitor_client.metrics.list(
        resource_id,
        timespan=f"{metric_start_time}/{metric_end_time}",
        interval='PT1M',
        metricnames='Percentage CPU',
        aggregation='Average'
    )

    print("\nCPU METRICS")
    print("=" * 50)

    cpu_values = []

    for item in metrics_data.value:

        for timeserie in item.timeseries:

            for data in timeserie.data:

                if data.average is not None:

                    cpu_usage = round(data.average, 2)

                    cpu_values.append(cpu_usage)

                    print(f"CPU Usage: {cpu_usage}%")

                    logging.info(f"CPU Usage: {cpu_usage}%")

    # ==============================
    # CPU ALERT CHECK
    # ==============================

    if cpu_values:

        avg_cpu = round(sum(cpu_values) / len(cpu_values), 2)

        print(f"\nAverage CPU Usage: {avg_cpu}%")

        logging.info(f"Average CPU Usage: {avg_cpu}%")

        if avg_cpu > 80:

            warning_message = (
                f"HIGH CPU ALERT! "
                f"Average CPU Usage is {avg_cpu}%"
            )

            print(warning_message)

            logging.warning(warning_message)

    else:

        logging.warning("No CPU metrics available")

    # ==============================
    # MONITORING COMPLETED
    # ==============================

    logging.info("Monitoring completed successfully")

    print("\nMonitoring Completed Successfully")

# ==============================
# EXCEPTION HANDLING
# ==============================

except Exception as e:

    error_message = f"Monitoring failed: {e}"

    logging.error(error_message)

    print(f"\nERROR: {error_message}")

# ==========================================
# EXECUTION TIME
# ==========================================

end_time = time.time()

execution_time = round(
    end_time - start_time,
    2
)

execution_end = datetime.now()

print("\n" + "=" * 50)

print(
    f"Execution Completed At: "
    f"{execution_end.strftime('%Y-%m-%d %H:%M:%S')}"
)

print(
    f"Execution Time: "
    f"{execution_time} seconds"
)

print("=" * 50)

# output_stream.close()