#!/bin/bash
# Azure App Service startup script.
#
# Oryx with CompressDestinationDir=true decompresses output.tar.zst
# to /tmp/<hash>/, sets CWD there, and activates the venv BEFORE
# running this script. Do NOT override CWD with --chdir.

echo "startup.sh: pwd=$(pwd)"
echo "startup.sh: python=$(which python)"
echo "startup.sh: manage.py=$(test -f manage.py && echo found || echo MISSING)"

# Ensure pip picks up the correct framework version (Oryx may cache stale wheels).
pip install --force-reinstall --no-deps "$(grep 'eo-site-framework' requirements.txt)" 2>/dev/null || true

# ── Dependency smoke check ─────────────────────────────────────────────
# Fail fast if critical packages are missing (catches stale wheel cache,
# broken extras resolution, or pip install failures).
python -c "
import eo_site_framework
print(f'startup.sh: eo-site-framework={eo_site_framework.__version__}')
import storages
print('startup.sh: django-storages OK')
" || { echo "startup.sh: FATAL — missing critical packages. Aborting."; exit 1; }

# One-time: rename tables from old 'landing' app to framework sub-apps (v1.2.6 domain-app-split).
# Idempotent — safe to leave in place after first successful run.
python manage.py migrate_domain_split --old-app landing || echo "startup.sh: migrate_domain_split failed (continuing startup)"

python manage.py migrate

# Keep local schema index populated for admin Snowball/Schema pickers.
# Backward-compatible: only run when framework version provides the command.
if python manage.py help | grep -q "sync_schema_index"; then
    echo "startup.sh: syncing approved schema index"
    python manage.py sync_schema_index --approved-only || echo "startup.sh: sync_schema_index failed (continuing startup)"
else
    echo "startup.sh: sync_schema_index command not available in current framework build"
fi

gunicorn --workers 2 --threads 4 --timeout 60 \
    --access-logfile '-' --error-logfile '-' \
    --bind=0.0.0.0:8000 \
    curiousfelloe.wsgi
