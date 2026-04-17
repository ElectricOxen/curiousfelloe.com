// ============================================================================
// curiousfelloe.com — Site Infrastructure
//
// Deploys this site's resources against the shared Electric Oxen platform:
//   Web App, Database, App Settings, KV Secrets, RBAC, Custom Domain
//
// Prerequisites:
//   The shared platform (VNet, PG server, ASP, Key Vault) must already exist.
//   Deploy it first from eo-site-framework/infra/platform.bicep.
//
// Deploy:
//   az deployment group create -g electricoxen-io \
//     -f infra/main.bicep -p infra/main.bicepparam
//
// Preview:
//   az deployment group what-if -g electricoxen-io \
//     -f infra/main.bicep -p infra/main.bicepparam
// ============================================================================

targetScope = 'resourceGroup'

// ── Site Parameters ─────────────────────────────────────────────────────────

@description('Web app name (must be globally unique)')
param appName string

@description('Custom domain name')
param domainName string

@description('Database name on the shared PG server')
param databaseName string

@description('Default from-email for Django')
param defaultFromEmail string

@description('Notification email for Django')
param notifyEmail string

@description('KV secret name for the DB password')
param dbPassSecretName string

@description('KV secret name for the Django secret key')
param djangoKeySecretName string

@description('GitHub repo (owner/name) for OIDC and CI/CD setup')
param githubRepo string

// ── Shared Platform Resource Names ──────────────────────────────────────────

@description('Name of the existing App Service Plan')
param planName string = 'ASP-electricoxenio-b396'

@description('Name of the existing PostgreSQL Flexible Server')
param dbServerName string = 'electricoxen-server'

@description('Name of the existing Key Vault')
param kvName string = 'electricoxen-kv'

@description('Name of the existing VNet')
param vnetName string = 'electricoxenVnet'

@description('Name of the App Service subnet')
param appSubnetName string = 'electricoxenAppSubnet'

@description('PostgreSQL admin login')
param dbAdminLogin string

// ── Secrets ─────────────────────────────────────────────────────────────────

@secure()
@description('Django SECRET_KEY value')
param djangoSecretKey string

@secure()
@description('PostgreSQL admin password')
param dbAdminPassword string

// ── OIDC ────────────────────────────────────────────────────────────────────

@description('Object ID of the Entra app registration for GitHub OIDC')
param oidcAppObjectId string = 'da2934ed-4b9b-47bc-8cba-c573b91f6309'

// ── Existing Shared Resources ───────────────────────────────────────────────

resource plan 'Microsoft.Web/serverfarms@2023-12-01' existing = {
  name: planName
}

resource pgServer 'Microsoft.DBforPostgreSQL/flexibleServers@2022-12-01' existing = {
  name: dbServerName
}

resource vault 'Microsoft.KeyVault/vaults@2023-07-01' existing = {
  name: kvName
}

resource vnet 'Microsoft.Network/virtualNetworks@2023-11-01' existing = {
  name: vnetName
}

resource appSubnet 'Microsoft.Network/virtualNetworks/subnets@2023-11-01' existing = {
  parent: vnet
  name: appSubnetName
}

// ── Web App ─────────────────────────────────────────────────────────────────

resource webApp 'Microsoft.Web/sites@2023-12-01' = {
  name: appName
  location: resourceGroup().location
  kind: 'app,linux'
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    serverFarmId: plan.id
    httpsOnly: true
    virtualNetworkSubnetId: appSubnet.id
    siteConfig: {
      linuxFxVersion: 'PYTHON|3.11'
      appCommandLine: 'startup.sh'
      alwaysOn: false
      ftpsState: 'FtpsOnly'
      http20Enabled: false
      minTlsVersion: '1.2'
      numberOfWorkers: 1
    }
  }
}

// ── Database ────────────────────────────────────────────────────────────────

resource database 'Microsoft.DBforPostgreSQL/flexibleServers/databases@2022-12-01' = {
  parent: pgServer
  name: databaseName
  properties: {
    charset: 'UTF8'
    collation: 'en_US.utf8'
  }
}

// ── App Settings ────────────────────────────────────────────────────────────

var kvBaseUri = 'https://${kvName}${environment().suffixes.keyvaultDns}/secrets'

resource appSettings 'Microsoft.Web/sites/config@2023-12-01' = {
  name: 'appsettings'
  parent: webApp
  properties: {
    APP_NAME: appName
    DOMAIN_NAME: domainName
    DEV_DOMAIN_NAME: '.azurewebsites.net'
    DEBUG_MODE: 'False'
    LOCAL_MODE: 'False'
    DEFAULT_FROM_EMAIL: defaultFromEmail
    NOTIFY_EMAIL: notifyEmail
    EXTRA_ALLOWED_HOSTS: '${appName}.azurewebsites.net,${domainName},www.${domainName}'
    DBNAME: databaseName
    DBHOST: pgServer.properties.fullyQualifiedDomainName
    DBUSER: dbAdminLogin
    DBPORT: '5432'
    DJANGO_SECRET_KEY: '@Microsoft.KeyVault(SecretUri=${kvBaseUri}/${djangoKeySecretName}/)'
    DBPASS: '@Microsoft.KeyVault(SecretUri=${kvBaseUri}/${dbPassSecretName}/)'
    SCM_DO_BUILD_DURING_DEPLOYMENT: 'true'
    ENABLE_ORYX_BUILD: 'true'
    DISABLE_COLLECTSTATIC: 'true'
    WEBSITE_HTTPLOGGING_RETENTION_DAYS: '3'
  }
}

// ── Key Vault Secrets ───────────────────────────────────────────────────────

resource dbPassSecret 'Microsoft.KeyVault/vaults/secrets@2023-07-01' = {
  parent: vault
  name: dbPassSecretName
  properties: {
    value: dbAdminPassword
  }
}

resource djangoKeySecret 'Microsoft.KeyVault/vaults/secrets@2023-07-01' = {
  parent: vault
  name: djangoKeySecretName
  properties: {
    value: djangoSecretKey
  }
}

// ── RBAC: Web App → Key Vault Secrets User ──────────────────────────────────

resource kvRbac 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(vault.id, webApp.id, '4633458b-17de-408a-b874-0445c86b69e6')
  scope: vault
  properties: {
    roleDefinitionId: subscriptionResourceId(
      'Microsoft.Authorization/roleDefinitions',
      '4633458b-17de-408a-b874-0445c86b69e6'
    )
    principalId: webApp.identity.principalId
    principalType: 'ServicePrincipal'
  }
}

// ── Custom Domain + SSL ─────────────────────────────────────────────────────
// Domain binding and SSL certs are managed outside of Bicep (one-time CLI setup
// + CI/CD "Ensure SSL Certificate" step). Bicep's hostname binding resource
// resets sslState to Disabled on every deploy, destroying the cert binding.

// ── Outputs ─────────────────────────────────────────────────────────────────

output webAppUrl string = 'https://${webApp.properties.defaultHostName}'
output customDomainUrl string = 'https://${domainName}'

output dnsRecords object = {
  cname: { type: 'CNAME', host: 'www', value: webApp.properties.defaultHostName }
  txt: { type: 'TXT', host: 'asuid', value: webApp.properties.customDomainVerificationId }
  note: 'For apex domain (@), use A record or CNAME flattening to ${webApp.properties.defaultHostName}'
}

output oidcSetupCommands array = [
  'az ad app federated-credential create --id ${oidcAppObjectId} --parameters \'{"name":"${replace(githubRepo, '/', '-')}-env-production","issuer":"https://token.actions.githubusercontent.com","subject":"repo:${githubRepo}:environment:production","audiences":["api://AzureADTokenExchange"]}\''
  'az ad app federated-credential create --id ${oidcAppObjectId} --parameters \'{"name":"${replace(githubRepo, '/', '-')}-branch-production","issuer":"https://token.actions.githubusercontent.com","subject":"repo:${githubRepo}:ref:refs/heads/production","audiences":["api://AzureADTokenExchange"]}\''
  'az ad app federated-credential create --id ${oidcAppObjectId} --parameters \'{"name":"${replace(githubRepo, '/', '-')}-pull-request","issuer":"https://token.actions.githubusercontent.com","subject":"repo:${githubRepo}:pull_request","audiences":["api://AzureADTokenExchange"]}\''
]

output githubSetupCommands array = [
  'gh api repos/${githubRepo}/environments/production -X PUT'
  'gh secret set AZURE_CLIENT_ID -R ${githubRepo} --env production --body "$(az ad app show --id ${oidcAppObjectId} --query appId -o tsv)"'
  'gh secret set AZURE_TENANT_ID -R ${githubRepo} --env production --body "${subscription().tenantId}"'
  'gh secret set AZURE_SUBSCRIPTION_ID -R ${githubRepo} --env production --body "${subscription().subscriptionId}"'
]
