from azure.identity import AzureCliCredential

from azure.mgmt.resource import ResourceManagementClient

import logging
import sys
import os
import time
from datetime import datetime

# ==========================================
# LOGGING CONFIGURATION
# ==========================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

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
# START EXECUTION TIMER
# ==========================================

execution_start = datetime.now()
start_time = time.time()

print(
    f"Execution Started At: "
    f"{execution_start.strftime('%Y-%m-%d %H:%M:%S')}"
)

print("=" * 50)

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

log_dir = os.path.join(BASE_DIR, 'logs')
os.makedirs(log_dir, exist_ok=True)

log_file = os.path.join(log_dir, 'resource_cleanup.log')

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)

# ==========================================
# AZURE CONFIGURATION
# ==========================================

subscription_id = "a8bd7b1b-b9aa-4283-aec4-2040b847d926"

resource_group = "AutoProjectRG"

# ==========================================
# AUTHENTICATION
# ==========================================

credential = AzureCliCredential()

resource_client = ResourceManagementClient(
    credential,
    subscription_id
)

# ==========================================
# USER INPUT
# ==========================================

print("\nAZURE RESOURCE CLEANUP SYSTEM\n")

print("1. Delete Specific Resource")
print("2. Delete Entire Resource Group")

choice = input("\nEnter your choice (1 or 2): ")

# ==========================================
# DELETE SPECIFIC RESOURCE
# ==========================================

try:

    if choice == "1":

        resource_name = input(
            "\nEnter Resource Name: "
        )

        resource_type = input(
            "Enter Resource Type\n"
            "(Example: "
            "Microsoft.Compute/virtualMachines): "
        )

        api_version = input(
            "Enter API Version\n"
            "(Example: 2023-07-01): "
        )

        print(
            f"\nDeleting Resource: {resource_name}"
        )

        delete_operation = resource_client.resources.begin_delete(
            resource_group_name=resource_group,
            resource_provider_namespace=resource_type.split('/')[0],
            parent_resource_path="",
            resource_type=resource_type.split('/')[1],
            resource_name=resource_name,
            api_version=api_version
        )

        delete_operation.result()

        print(
            "Resource deleted successfully"
        )

        logging.info(
            f"Deleted Resource: {resource_name}"
        )

    # ==========================================
    # DELETE RESOURCE GROUP
    # ==========================================

    elif choice == "2":

        print(
            f"\nDeleting Resource Group: "
            f"{resource_group}"
        )

        delete_operation = (
            resource_client.resource_groups.begin_delete(
                resource_group
            )
        )

        delete_operation.result()

        print(
            "Resource Group and all resources "
            "deleted successfully"
        )

        logging.info(
            f"Deleted Resource Group: "
            f"{resource_group}"
        )

    else:

        print("Invalid Choice")

        logging.warning(
            "Invalid cleanup choice entered"
        )

except Exception as e:

    logging.error(f"Cleanup failed: {e}")

    print(f"\nError: {e}")
    
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

output_stream.close()