terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }

    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {
    resource_group {
      prevent_deletion_if_contains_resources = false
    }
  }
}

data "azurerm_client_config" "current" {}

resource "random_string" "suffix" {
  length  = 5
  upper   = false
  special = false
}

locals {
  region_code  = replace(lower(var.primary_location), " ", "")
  clean_prefix = substr(replace(lower(var.name_prefix), "-", ""), 0, 10)
}

resource "azurerm_resource_group" "primary" {
  name     = var.resource_group_name
  location = var.primary_location
}

resource "azurerm_virtual_network" "primary_vnet" {
  name                = "${local.clean_prefix}-${local.region_code}-vnet"
  location            = azurerm_resource_group.primary.location
  resource_group_name = azurerm_resource_group.primary.name
  address_space       = ["10.0.0.0/16"]
}

resource "azurerm_subnet" "primary_subnet" {
  name                 = "${local.clean_prefix}-${local.region_code}-subnet"
  resource_group_name  = azurerm_resource_group.primary.name
  virtual_network_name = azurerm_virtual_network.primary_vnet.name
  address_prefixes     = ["10.0.1.0/24"]
}

resource "azurerm_network_interface" "primary_nic" {
  count               = var.vm_count
  name                = "${local.clean_prefix}-vm${format("%02d", count.index + 1)}-nic"
  location            = azurerm_resource_group.primary.location
  resource_group_name = azurerm_resource_group.primary.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.primary_subnet.id
    private_ip_address_allocation = "Dynamic"
  }
}

resource "azurerm_linux_virtual_machine" "primary_vm" {
  count               = var.vm_count
  name                = "${local.clean_prefix}-vm${format("%02d", count.index + 1)}"
  resource_group_name = azurerm_resource_group.primary.name
  location            = azurerm_resource_group.primary.location

  size           = var.vm_size
  admin_username = var.admin_username

  network_interface_ids = [
    azurerm_network_interface.primary_nic[count.index].id
  ]

  admin_ssh_key {
    username   = var.admin_username
    public_key = file(pathexpand(var.ssh_public_key_path))
  }

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
    disk_size_gb         = 30
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-jammy"
    sku       = "22_04-lts"
    version   = "latest"
  }
}

resource "azurerm_storage_account" "primary_storage" {
  count                    = var.storage_account_count
  name                     = "${local.clean_prefix}st${format("%02d", count.index + 1)}${random_string.suffix.result}"
  resource_group_name      = azurerm_resource_group.primary.name
  location                 = azurerm_resource_group.primary.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_key_vault" "primary_kv" {
  count                      = var.key_vault_count
  name                       = "${local.clean_prefix}-kv${format("%02d", count.index + 1)}-${random_string.suffix.result}"
  location                   = azurerm_resource_group.primary.location
  resource_group_name        = azurerm_resource_group.primary.name
  tenant_id                  = data.azurerm_client_config.current.tenant_id
  sku_name                   = "standard"
  purge_protection_enabled   = false
  soft_delete_retention_days = 7
}
