provider "azurerm" {
  tenant_id       = var.tenant_id
  subscription_id = var.subscription_id
  client_id       = var.client_id
  client_secret   = var.client_secret
  public_key_file = var.public_key_file
  features {}
}
terraform {
  backend "azurerm" {
    resource_group_name  = "tfstate"
    storage_account_name = "tfstate22060"
    container_name       = "tfstate"
    key                  = "terraform.tfstate"
  }
}
module "resource_group" {
  source         = "../../modules/resource_group"
  resource_group = var.resource_group
  location       = var.location
}
module "network" {
  source               = "../../modules/network"
  location             = var.location
  virtual_network_name = var.virtual_network_name
  application_type     = var.application_type
  resource_type        = "network"
  resource_group       = module.resource_group.resource_group_name
}

module "nsg-test" {
  source                  = "../../modules/networksecuritygroup"
  location                = var.location
  application_type        = var.application_type
  resource_type           = "security-group"
  resource_group          = module.resource_group.resource_group_name
  subnet_id               = module.network.subnet_id
  subnet_address_prefixes = module.network.subnet_address_prefixes
}
module "appservice" {
  source           = "../../modules/appservice"
  location         = var.location
  application_type = var.application_type
  resource_type    = "AppService"
  resource_group   = module.resource_group.resource_group_name
}
module "publicip" {
  source           = "../../modules/publicip"
  location         = var.location
  application_type = var.application_type
  resource_type    = "publicip"
  resource_group   = module.resource_group.resource_group_name
}
module "vm" {
  source               = "../../modules/vm"
  application_type     = var.application_type
  resource_type        = "vm"
  location             = var.location
  resource_group       = module.resource_group.resource_group_name
  public_ip_address_id = module.publicip.public_ip_address_id
  subnet_id            = module.network.subnet_id
  public_key_file      = var.public_key_file
}
