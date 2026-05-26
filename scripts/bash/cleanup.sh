#!/bin/bash

# ==========================================
# CONFIGURATION
# ==========================================
deleted_snapshots=0
deleted_disks=0
deleted_ips=0
deleted_nics=0
deleted_vms=0

RESOURCE_GROUP="AutoProjectRG"

echo "======================================="
echo "AZURE RESOURCE CLEANUP AUTOMATION"
echo "======================================="

# ==========================================
# DELETE OLD SNAPSHOTS
# ==========================================

echo ""
echo "Checking Old Snapshots..."

SNAPSHOTS=$(az snapshot list \
    --resource-group $RESOURCE_GROUP \
    --query "[].name" \
    --output tsv)

for snapshot in $SNAPSHOTS
do
    echo "Deleting Snapshot: $snapshot"

    az snapshot delete \
        --resource-group $RESOURCE_GROUP \
        --name $snapshot

    deleted_snapshots=$((deleted_snapshots + 1))
done

# ==========================================
# DELETE UNATTACHED DISKS
# ==========================================

echo ""
echo "Checking Unattached Disks..."

DISKS=$(az disk list \
    --resource-group $RESOURCE_GROUP \
    --query "[?managedBy==null].name" \
    --output tsv)

for disk in $DISKS
do
    echo "Deleting Unattached Disk: $disk"

    az disk delete \
        --resource-group $RESOURCE_GROUP \
        --name $disk \
        --yes
        deleted_disks=$((deleted_disks + 1))
done

# ==========================================
# DELETE UNUSED PUBLIC IPS
# ==========================================

echo ""
echo "Checking Unused Public IPs..."

IPS=$(az network public-ip list \
    --resource-group $RESOURCE_GROUP \
    --query "[?ipConfiguration==null].name" \
    --output tsv)

for ip in $IPS
do
    echo "Deleting Unused Public IP: $ip"

    az network public-ip delete \
        --resource-group $RESOURCE_GROUP \
        --name $ip
        deleted_ips=$((deleted_ips + 1))
done

# ==========================================
# DELETE ORPHANED NETWORK INTERFACES
# ==========================================

echo ""
echo "Checking Orphaned NICs..."

NICS=$(az network nic list \
    --resource-group $RESOURCE_GROUP \
    --query "[?virtualMachine==null].name" \
    --output tsv)

for nic in $NICS
do
    echo "Deleting Orphaned NIC: $nic"

    az network nic delete \
        --resource-group $RESOURCE_GROUP \
        --name $nic
        deleted_nics=$((deleted_nics + 1))
done

# ==========================================
# OPTIONAL:
# DELETE DEALLOCATED VMs
# ==========================================

echo ""
echo "Checking Deallocated VMs..."

VMS=$(az vm list -d \
    --resource-group $RESOURCE_GROUP \
    --query "[?powerState=='VM deallocated'].name" \
    --output tsv)

for vm in $VMS
do
    echo "Deleting Deallocated VM: $vm"

    az vm delete \
        --resource-group $RESOURCE_GROUP \
        --name $vm \
        --yes
        deleted_vms=$((deleted_vms + 1))
done

echo ""
echo "======================================="
echo "CLEANUP COMPLETED SUCCESSFULLY"
echo "======================================="

echo ""
echo "============== CLEANUP SUMMARY =============="

echo "Snapshots Deleted      : $deleted_snapshots"
echo "Disks Deleted          : $deleted_disks"
echo "Public IPs Deleted     : $deleted_ips"
echo "NICs Deleted           : $deleted_nics"
echo "VMs Deleted            : $deleted_vms"

echo "============================================="