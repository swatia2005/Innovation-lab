variable "resource_group_name" {
  type        = string
  description = "Azure Resource Group name"
}

variable "primary_location" {
  type        = string
  description = "Azure primary region"
  default     = "Central US"
}

variable "name_prefix" {
  type        = string
  description = "Prefix used to auto-generate resource names"
  default     = "hackathon"
}

variable "vm_count" {
  type        = number
  description = "Number of VMs to create"
  default     = 1
}

variable "storage_account_count" {
  type        = number
  description = "Number of storage accounts to create"
  default     = 1
}

variable "key_vault_count" {
  type        = number
  description = "Number of key vaults to create"
  default     = 1
}

variable "admin_username" {
  type        = string
  description = "Admin username for Linux VM"
  default     = "azureuser"
}

variable "ssh_public_key_path" {
  type        = string
  description = "Path to SSH public key"
  default     = "~/.ssh/id_rsa.pub"
}

variable "vm_size" {
  type        = string
  description = "Azure VM size"
  default     = "Standard_D2s_v3"
}
