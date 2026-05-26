param(
    [string]$Action
)

# ==========================================
# CONFIGURATION
# ==========================================

$ResourceGroup = "AutoProjectRG"
$VMName = "ProductionUbuntuVM"

Write-Host "======================================="
Write-Host "AZURE VM MANAGEMENT AUTOMATION"
Write-Host "======================================="

# ==========================================
# START VM
# ==========================================

if ($Action -eq "start") {

    Write-Host "Starting VM..."

    az vm start `
        --resource-group $ResourceGroup `
        --name $VMName

    Write-Host "VM Started Successfully"
}

# ==========================================
# STOP VM
# ==========================================

elseif ($Action -eq "stop") {

    Write-Host "Stopping VM..."

    az vm deallocate `
        --resource-group $ResourceGroup `
        --name $VMName

    Write-Host "VM Stopped Successfully"
}

# ==========================================
# RESTART VM
# ==========================================

elseif ($Action -eq "restart") {

    Write-Host "Restarting VM..."

    az vm restart `
        --resource-group $ResourceGroup `
        --name $VMName

    Write-Host "VM Restarted Successfully"
}

# ==========================================
# VM STATUS
# ==========================================

elseif ($Action -eq "status") {

    Write-Host "Fetching VM Status..."

    az vm get-instance-view `
        --resource-group $ResourceGroup `
        --name $VMName `
        --query "instanceView.statuses[].displayStatus" `
        --output table
}

# ==========================================
# INVALID INPUT
# ==========================================

else {

    Write-Host ""
    Write-Host "Invalid Action"
    Write-Host ""
    Write-Host "Usage:"
    Write-Host ".\vm_management.ps1 start"
    Write-Host ".\vm_management.ps1 stop"
    Write-Host ".\vm_management.ps1 restart"
    Write-Host ".\vm_management.ps1 status"
}