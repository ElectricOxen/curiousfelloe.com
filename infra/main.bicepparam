using './main.bicep'

// ── Site Identity ───────────────────────────────────────────────────────────

param appName = 'curiousfelloe'
param domainName = 'curiousfelloe.com'
param databaseName = 'curiousfelloe-db'
param defaultFromEmail = 'hello@curiousfelloe.com'
param notifyEmail = 'hello@curiousfelloe.com'
param githubRepo = 'ElectricOxen/curiousfelloe.com'

// ── Key Vault Secret Names ──────────────────────────────────────────────────

param dbPassSecretName = 'CF-DBPASS'
param djangoKeySecretName = 'CF-DJANGO-SECRET-KEY'

// ── Shared Platform ─────────────────────────────────────────────────────────

param dbAdminLogin = 'qlfewfpbrw'

// ── Secrets (set env vars before deploying) ─────────────────────────────────
// PowerShell: $env:CF_DJANGO_SECRET_KEY = '...'; $env:DBPASS = '...'
// Bash:       export CF_DJANGO_SECRET_KEY='...' DBPASS='...'

param djangoSecretKey = readEnvironmentVariable('CF_DJANGO_SECRET_KEY')
param dbAdminPassword = readEnvironmentVariable('DBPASS')
