#!/bin/bash

RESOURCE_GROUP="AutoProjectRG"
LOCATION="centralindia"

echo "Creating Resource Group..."

az group create \
    --name $RESOURCE_GROUP \
    --location $LOCATION

echo "Resource Group Created"