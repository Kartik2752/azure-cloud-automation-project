#!/bin/bash

RESOURCE_GROUP="AutoProjectRG"
VM_NAME="ProductionUbuntuVM"
SNAPSHOT_NAME="vmSnapshot-$(date +%Y%m%d%H%M%S)"

echo "Starting VM Backup..."

# Get OS Disk Name
DISK_NAME=$(az vm show \
    --resource-group $RESOURCE_GROUP \
    --name $VM_NAME \
    --query "storageProfile.osDisk.name" \
    --output tsv)

echo "OS Disk: $DISK_NAME"

# Get Disk ID
DISK_ID=$(az disk show \
    --resource-group $RESOURCE_GROUP \
    --name $DISK_NAME \
    --query "id" \
    --output tsv)

# Create Snapshot
az snapshot create \
    --resource-group $RESOURCE_GROUP \
    --source $DISK_ID \
    --name $SNAPSHOT_NAME

echo "Backup Snapshot Created Successfully"