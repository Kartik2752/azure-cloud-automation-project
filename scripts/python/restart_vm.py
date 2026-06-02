from azure.identity import AzureCliCredential
from azure.mgmt.compute import ComputeManagementClient
import logging
import os
import sys
import time
from datetime import datetime

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

output_dir = os.path.join(BASE_DIR, "outputs")


# OUTPUT DIRECTORY


os.makedirs(output_dir, exist_ok=True)


# OUTPUT FILE


script_name = os.path.splitext(
    os.path.basename(__file__)
)[0]

output_file = os.path.join(
    output_dir,
    f"{script_name}_output.txt"
)


# TEE OUTPUT CLASS


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




# OUTPUT STREAM


output_stream = open(
    output_file,
    "w",
    encoding="utf-8"
)


# DUPLICATE OUTPUT


sys.stdout = Tee(sys.stdout, output_stream)

sys.stderr = Tee(sys.stderr, output_stream)

log_path = os.path.join(BASE_DIR, 'logs', 'vm_operations.log')

logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)


# START EXECUTION TIMER


execution_start = datetime.now()
start_time = time.time()

print(
    f"Execution Started At: "
    f"{execution_start.strftime('%Y-%m-%d %H:%M:%S')}"
)

print("=" * 50)

try:
    subscription_id = "a8bd7b1b-b9aa-4283-aec4-2040b847d926"

    credential = AzureCliCredential()

    compute_client = ComputeManagementClient(
        credential,
        subscription_id
    )

    print("Restarting VM...")

    compute_client.virtual_machines.begin_restart(
        "AutoProjectRG",
        "ProductionUbuntuVM"
    ).wait()

    print("VM Restarted Successfully")

    logging.info("VM restarted successfully")

except Exception as e:
    logging.error(f"Error restarting VM: {e}")
    print(f"Error: {e}")
    

# EXECUTION TIME


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