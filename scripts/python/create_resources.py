from azure.identity import AzureCliCredential

from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute.models import (
    VirtualMachine,
    HardwareProfile,
    StorageProfile,
    ImageReference,
    OSDisk,
    ManagedDiskParameters,
    OSProfile,
    LinuxConfiguration,
    SshConfiguration,
    SshPublicKey,
    NetworkProfile,
    NetworkInterfaceReference
)

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

log_file = os.path.join(log_dir, 'resources.log')

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
location = "centralindia"

vm_name = "ProductionUbuntuVM"

vnet_name = "ProjectVNet"
subnet_name = "DefaultSubnet"

public_ip_name = "ProjectPublicIP"

nsg_name = "ProjectNSG"

nic_name = "ProductionUbuntuVMNic"

# ==========================================
# AUTHENTICATION
# ==========================================

credential = AzureCliCredential()

resource_client = ResourceManagementClient(
    credential,
    subscription_id
)

compute_client = ComputeManagementClient(
    credential,
    subscription_id
)

network_client = NetworkManagementClient(
    credential,
    subscription_id
)

try:

    logging.info("Infrastructure creation started")

    # ==========================================
    # CHECK / CREATE RESOURCE GROUP
    # ==========================================

    if resource_client.resource_groups.check_existence(
        resource_group
    ):

        logging.info(
            f"Resource Group already exists: {resource_group}"
        )

    else:

        resource_client.resource_groups.create_or_update(
            resource_group,
            {
                "location": location
            }
        )

        logging.info(
            f"Resource Group created: {resource_group}"
        )

    # ==========================================
    # VIRTUAL NETWORK
    # ==========================================

    vnet = network_client.virtual_networks.begin_create_or_update(
        resource_group,
        vnet_name,
        {
            "location": location,
            "address_space": {
                "address_prefixes": ["10.0.0.0/16"]
            }
        }
    ).result()

    logging.info("Virtual Network created")

    # ==========================================
    # SUBNET
    # ==========================================

    subnet = network_client.subnets.begin_create_or_update(
        resource_group,
        vnet_name,
        subnet_name,
        {
            "address_prefix": "10.0.0.0/24"
        }
    ).result()

    logging.info("Subnet created")

    # ==========================================
    # PUBLIC IP
    # ==========================================

    public_ip = network_client.public_ip_addresses.begin_create_or_update(
        resource_group,
        public_ip_name,
        {
            "location": location,
            "sku": {
                "name": "Standard"
            },
            "public_ip_allocation_method": "Static"
        }
    ).result()

    logging.info("Public IP created")

    # ==========================================
    # NETWORK SECURITY GROUP
    # ==========================================

    nsg = network_client.network_security_groups.begin_create_or_update(
        resource_group,
        nsg_name,
        {
            "location": location
        }
    ).result()

    logging.info("NSG created")

    # ==========================================
    # SSH RULE
    # ==========================================

    network_client.security_rules.begin_create_or_update(
        resource_group,
        nsg_name,
        "AllowSSH",
        {
            "protocol": "Tcp",
            "source_port_range": "*",
            "destination_port_range": "22",
            "source_address_prefix": "*",
            "destination_address_prefix": "*",
            "access": "Allow",
            "priority": 1000,
            "direction": "Inbound"
        }
    ).result()

    logging.info("SSH rule created")

    # ==========================================
    # HTTP RULE
    # ==========================================

    network_client.security_rules.begin_create_or_update(
        resource_group,
        nsg_name,
        "AllowHTTP",
        {
            "protocol": "Tcp",
            "source_port_range": "*",
            "destination_port_range": "80",
            "source_address_prefix": "*",
            "destination_address_prefix": "*",
            "access": "Allow",
            "priority": 1001,
            "direction": "Inbound"
        }
    ).result()

    logging.info("HTTP rule created")

    # ==========================================
    # HTTPS RULE
    # ==========================================

    network_client.security_rules.begin_create_or_update(
        resource_group,
        nsg_name,
        "AllowHTTPS",
        {
            "protocol": "Tcp",
            "source_port_range": "*",
            "destination_port_range": "443",
            "source_address_prefix": "*",
            "destination_address_prefix": "*",
            "access": "Allow",
            "priority": 1002,
            "direction": "Inbound"
        }
    ).result()

    logging.info("HTTPS rule created")

    # ==========================================
    # NETWORK INTERFACE
    # ==========================================

    nic = network_client.network_interfaces.begin_create_or_update(
        resource_group,
        nic_name,
        {
            "location": location,
            "ip_configurations": [{
                "name": "IPConfig",
                "subnet": {
                    "id": subnet.id
                },
                "public_ip_address": {
                    "id": public_ip.id
                }
            }],
            "network_security_group": {
                "id": nsg.id
            }
        }
    ).result()

    logging.info("NIC created")

    # ==========================================
    # VIRTUAL MACHINE
    # ==========================================

    vm_parameters = VirtualMachine(

        location=location,

        hardware_profile=HardwareProfile(
            vm_size="Standard_B2ats_v2"
        ),

        storage_profile=StorageProfile(

            image_reference=ImageReference(
                publisher="Canonical",
                offer="0001-com-ubuntu-server-jammy",
                sku="22_04-lts-gen2",
                version="latest"
            ),

            os_disk=OSDisk(
                create_option="FromImage",

                managed_disk=ManagedDiskParameters(
                    storage_account_type="Standard_LRS"
                )
            )
        ),

        os_profile=OSProfile(

            computer_name=vm_name,

            admin_username="azureuser",

            linux_configuration=LinuxConfiguration(

                disable_password_authentication=True,

                ssh=SshConfiguration(

                    public_keys=[

                        SshPublicKey(

                            path="/home/azureuser/.ssh/authorized_keys",

                            key_data=open(
                                os.path.expanduser(
                                    "~/.ssh/id_rsa.pub"
                                )
                            ).read()
                        )
                    ]
                )
            )
        ),

        network_profile=NetworkProfile(

            network_interfaces=[

                NetworkInterfaceReference(
                    id=nic.id,
                    primary=True
                )
            ]
        )
    )

    compute_client.virtual_machines.begin_create_or_update(
        resource_group,
        vm_name,
        vm_parameters
    ).result()

    logging.info("VM created successfully")

except Exception as e:

    logging.error(f"Error: {e}")

    print(f"Error: {e}")

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