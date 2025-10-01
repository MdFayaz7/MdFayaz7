#!/bin/bash
# Build script for Vercel deployment

# Make build_files.sh executable
chmod a+x build_files.sh

# Install Python dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput --clear

# Create directory for static files
mkdir -p staticfiles_build/static

# Copy all static files
cp -r static staticfiles_build/

# Copy all media files if they exist
if [ -d "media" ]; then
  mkdir -p staticfiles_build/media
  cp -r media staticfiles_build/
fi

echo "Build completed successfully!"