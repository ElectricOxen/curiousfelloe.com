# curiousfelloe.com

Website for [Curious Felloe Games](https://curiousfelloe.com) — Electric Oxen's indie game studio.

## Stack

- **Framework**: [eo-site-framework](https://github.com/ElectricOxen/eo-site-framework) v1.2.0
- **Backend**: Django 5.2, Python 3.12, PostgreSQL 16
- **Frontend**: Tailwind v4 + daisyUI v5, Alpine.js, HTMX
- **Hosting**: Azure App Service (Linux) + Azure PostgreSQL Flexible Server
- **CI/CD**: GitHub Actions (OIDC → Azure)

## Local Development

```powershell
# Activate conda environment
& "$env:USERPROFILE\miniconda3\shell\condabin\conda-hook.ps1"
conda activate django

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Seed content (first time)
python manage.py seed_mvp_content --profile studio

# Start dev server
python manage.py runserver 8002
```

## Framework Relationship

This site is a thin consumer of `eo-site-framework`. The framework provides abstract models, views, templates, and the admin portal. This repo owns:

- `landing/models.py` — Concrete model subclasses
- `landing/views.py` — Site-specific views
- `templates/` — Site-specific template overrides and brand customization
- `static/css/input.css` — Tailwind theme tokens and brand colors
- `curiousfelloe/settings.py` — `EO_FRAMEWORK` configuration dict

## Deployment

Pushes to the `production` branch trigger automatic deployment via GitHub Actions.
