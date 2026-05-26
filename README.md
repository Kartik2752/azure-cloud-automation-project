# Automated Azure Resource Provisioning and Management System

## Project Overview

This project demonstrates cloud automation using Microsoft Azure, Python, Bash, and PowerShell scripting. The system automates Azure infrastructure provisioning, virtual machine management, monitoring, backup, cleanup, and scheduled automation tasks.

The project follows DevOps and SRE practices by implementing:
- Infrastructure automation
- Resource monitoring
- Logging
- Error handling
- Scheduled operations
- Cost optimization
- Automated cleanup

---

# Technologies Used

- Microsoft Azure
- Azure CLI
- Python 3.12
- PowerShell
- Bash Scripting
- Windows Task Scheduler
- Azure SDK for Python
- Git & GitHub

---

# Project Features

## Infrastructure Provisioning
- Resource Group creation
- Virtual Network creation
- Subnet creation
- Public IP creation
- Network Security Group creation
- Ubuntu Virtual Machine provisioning
- Storage Account creation

## VM Lifecycle Automation
- Start VM
- Stop VM
- Restart VM
- Monitor VM status

## Monitoring & Logging
- Resource monitoring
- VM status tracking
- CPU usage monitoring
- Scheduler status tracking
- Log generation

## Backup & Cleanup Automation
- VM snapshot backup
- Unused resource cleanup
- Orphaned resource detection

## Scheduling Automation
- Automatic VM shutdown using Windows Task Scheduler
- Automated task execution logging

---

# Project Structure

```text
Automated Azure Resource Provisioning and Management System/
│
├── docs/
│
├── logs/
│   ├── scheduler.log
|   ├── storage.log
│   ├── vm_operations.log
│   ├── resources.log
│   ├── resource_monitoring.log
│   └── resource_cleanup.log
│
├── outputs/
│   ├── cleanup_resource_output.txt
│   ├── create_resources_output.txt
│   ├── create_storage_output.txt
│   ├── monitor_resources_output.txt
│   ├── restart_vm_output.txt
│   ├── scheduler_runner_output.txt
│   ├── start_vm_output.txt
│   └── stop_vm_output.txt
│ 
│
├── scripts/
│
│   ├── bash/
│   │   ├── backup.sh
│   │   |── cleanup.sh
│   │   └── create_resource.sh
│   │
│   ├── powershell/
│   │   └── vm_management.ps1
│   │
│   └── python/
│       ├── create_resources.py
│       ├── create_storage.py
│       ├── start_vm.py
│       ├── stop_vm.py
│       ├── restart_vm.py
│       ├── monitor_resource.py
│       ├── cleanup_resource.py
│       └── scheduler_runner.py
│
├── requirements.txt
└── README.md



---

# Step-by-Step Project Execution Guide

This section explains how to execute and understand every file in the project.

---

# Step 1 — Clone or Open Project

Open terminal inside project directory:

```bash
cd "Automated Azure Resource Provisioning and Management System"
```

---

# Step 2 — Create Virtual Environment

```bash
python -m venv venv
```

---

# Step 3 — Activate Virtual Environment

## Windows PowerShell

```powershell
venv\Scripts\Activate.ps1
```

Activated environment:

```text
(venv)
```

---

# Step 4 — Install Required Packages

```bash
pip install -r requirements.txt
```

---

# Step 5 — Login to Azure

```bash
az login
```

Verify account:

```bash
az account show
```

---

# Step 6 — Create Azure Infrastructure

## File

```text
scripts/python/create_resources.py
```

## Purpose

Creates:
- Resource Group
- Virtual Network
- Subnet
- NSG
- Public IP
- Network Interface
- Ubuntu Virtual Machine

## Run

```bash
python scripts/python/create_resources.py
```

## Output

```text
outputs/create_resources_output.txt
```

## Logs

```text
logs/vm_creation.log
```

---

# Step 7 — Create Storage Account

## File

```text
scripts/python/create_storage.py
```

## Purpose

Creates Azure Storage Account.

## Run

```bash
python scripts/python/create_storage.py
```

## Output

```text
outputs/create_storage_output.txt
```

## Logs

```text
logs/storage_creation.log
```

---

# Step 8 — Start Virtual Machine

## File

```text
scripts/python/start_vm.py
```

## Purpose

Starts Azure VM.

## Run

```bash
python scripts/python/start_vm.py
```

## Output

```text
outputs/start_vm_output.txt
```

---

# Step 9 — Stop Virtual Machine

## File

```text
scripts/python/stop_vm.py
```

## Purpose

Stops and deallocates Azure VM.

## Run

```bash
python scripts/python/stop_vm.py
```

## Output

```text
outputs/stop_vm_output.txt
```

---

# Step 10 — Restart Virtual Machine

## File

```text
scripts/python/restart_vm.py
```

## Purpose

Restarts Azure VM.

## Run

```bash
python scripts/python/restart_vm.py
```

## Output

```text
outputs/restart_vm_output.txt
```

---

# Step 11 — Monitor Virtual Machine

## File

```text
scripts/python/monitor_vm.py
```

## Purpose

Displays:
- VM state
- VM size
- CPU metrics
- Instance status

## Run

```bash
python scripts/python/monitor_vm.py
```

## Output

```text
outputs/monitor_vm_output.txt
```

## Logs

```text
logs/monitoring.log
```

---

# Step 12 — Dynamic Resource Monitoring

## File

```text
scripts/python/dynamic_resource_monitor.py
```

## Purpose

Monitors all resources dynamically inside Resource Group.

Supports:
- VM
- Public IP
- VNet
- NSG
- Storage Account
- NIC
- Disk

## Run

```bash
python scripts/python/dynamic_resource_monitor.py
```

## Output

```text
outputs/dynamic_resource_monitor_output.txt
```

---

# Step 13 — Backup Automation

## File

```text
scripts/bash/backup.sh
```

## Purpose

Creates VM snapshots for backup and recovery.

## Run

```bash
bash scripts/bash/backup.sh
```

## Output

```text
outputs/backup_output.txt
```

---

# Step 14 — Cleanup Automation

## File

```text
scripts/bash/cleanup.sh
```

## Purpose

Automatically removes:
- Old snapshots
- Unattached disks
- Unused public IPs
- Orphaned NICs
- Deallocated VMs

Helps reduce Azure cloud cost.

## Run

```bash
bash scripts/bash/cleanup.sh
```

## Output

```text
outputs/cleanup_output.txt
```

## Logs

```text
logs/cleanup.log
```

---

# Step 15 — PowerShell VM Management

## File

```text
scripts/powershell/vm_management.ps1
```

## Purpose

Performs:
- VM Start
- VM Stop
- VM Restart
- VM Status Check

## Run

### Start VM

```powershell
.\scripts\powershell\vm_management.ps1 start
```

### Stop VM

```powershell
.\scripts\powershell\vm_management.ps1 stop
```

### Restart VM

```powershell
.\scripts\powershell\vm_management.ps1 restart
```

### VM Status

```powershell
.\scripts\powershell\vm_management.ps1 status
```

## Output

```text
outputs/vm_management_output.txt
```

---

# Step 16 — Resource Cleanup Automation

## File

```text
scripts/python/resource_cleanup.py
```

## Purpose

Supports:
- Specific resource deletion
- Entire Resource Group deletion

## Run

```bash
python scripts/python/resource_cleanup.py
```

## Output

```text
outputs/resource_cleanup_output.txt
```

---

# Step 17 — Scheduler Automation

## File

```text
scripts/python/scheduler_runner.py
```

## Purpose

Automates:
- Scheduled VM shutdown
- Scheduler status tracking
- Runtime logging

## Run

```bash
python scripts/python/scheduler_runner.py
```

## Output

```text
outputs/scheduler_runner_output.txt
```

## Scheduler Status File

```text
outputs/scheduler_status.txt
```

## Logs

```text
logs/scheduler.log
```

---

# Step 18 — Windows Task Scheduler Setup

## Purpose

Automatically stops Azure VM daily at 10 PM.

## Steps

1. Open Task Scheduler
2. Click "Create Basic Task"
3. Name:
   ```text
   Azure VM Auto Shutdown
   ```
4. Trigger:
   ```text
   Daily
   ```
5. Time:
   ```text
   10:00 PM
   ```
6. Action:
   ```text
   Start a Program
   ```
7. Program:
   ```text
   cmd.exe
   ```
8. Arguments:
   ```text
   /c "venv\Scripts\python.exe scripts\python\scheduler_runner.py"
   ```

---

# Step 19 — View Outputs

All terminal outputs are automatically stored inside:

```text
outputs/
```

---

# Step 20 — View Logs

All logs are automatically stored inside:

```text
logs/
```

---

# Step 21 — Verify Azure Resources

## Azure Portal

Check:
- Resource Group
- VM
- VNet
- Public IP
- NSG
- Storage Account

## Azure CLI

```bash
az resource list --resource-group AutoProjectRG --output table
```

---

# Step 22 — Deactivate Virtual Environment

```bash
deactivate
```

---