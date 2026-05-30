output "resource_group_name" {
  value = azurerm_resource_group.primary.name
}

output "vnet_name" {
  value = azurerm_virtual_network.primary_vnet.name
}

output "subnet_name" {
  value = azurerm_subnet.primary_subnet.name
}

output "vm_names" {
  value = azurerm_linux_virtual_machine.primary_vm[*].name
}

output "nic_names" {
  value = azurerm_network_interface.primary_nic[*].name
}

output "storage_account_names" {
  value = azurerm_storage_account.primary_storage[*].name
}

output "key_vault_names" {
  value = azurerm_key_vault.primary_kv[*].name
}
