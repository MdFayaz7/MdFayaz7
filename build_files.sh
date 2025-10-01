#!/bin/bash

# Ensure pip is available and up to date
python -m pip install --upgrade pip

# Install Python dependencies
python -m pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput