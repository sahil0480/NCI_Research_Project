# terraform.tfvars
subscription_id   = "your-subscription-id"
client_id         = "your-client-id"
client_secret     = "your-client-secret"
tenant_id         = "your-tenant-id"
aks_cluster_name  = "nci-aks-cluster"
acr_name          = "nciregistryacr"
resource_group_name = "nci-azure-rg"
location            = "northeurope"
prefix              = "nciaks"
node_count          = 2
vm_size             = "Standard_B2s"