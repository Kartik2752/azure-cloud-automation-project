from azure.identity import AzureCliCredential
from azure.mgmt.storage import StorageManagementClient
import os
import logging

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

log_path = os.path.join(BASE_DIR, 'logs', 'storage.log')

logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

try:
    subscription_id = "a8bd7b1b-b9aa-4283-aec4-2040b847d926"

    credential = AzureCliCredential()

    storage_client = StorageManagementClient(
        credential,
        subscription_id
    )

    poller = storage_client.storage_accounts.begin_create(
        "AutoProjectRG",
        "autoprojectstorage123",
        {
            "location": "centralindia",
            "sku": {"name": "Standard_LRS"},
            "kind": "StorageV2"
        }
    )

    result = poller.result()

    logging.info("Storage account created successfully")

    print("Storage account created")

except Exception as e:
    logging.error(f"Error: {e}")
    print("Error occurred")