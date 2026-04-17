#!/bin/bash
# Azure App Service startup script.
#
# Oryx with CompressDestinationDir=true decompresses output.tar.zst
# to /tmp/<hash>/, sets CWD there, and activates the venv BEFORE
# running this script. Do NOT override CWD with --chdir.

echo "startup.sh: pwd=$(pwd)"
echo "startup.sh: python=$(which python)"
echo "startup.sh: manage.py=$(test -f manage.py && echo found || echo MISSING)"

python manage.py migrate

gunicorn --workers 2 --threads 4 --timeout 60 \
    --access-logfile '-' --error-logfile '-' \
    --bind=0.0.0.0:8000 \
    curiousfelloe.wsgi
