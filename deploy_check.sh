#!/bin/bash

echo "🔍 College Fee System - Deployment Check Script"
echo "=============================================="

# Check if required files exist
echo "📁 Checking required files..."
required_files=("render.yaml" "requirements.txt" "package.json" "manage.py" "college_fee_system/settings.py")

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file exists"
    else
        echo "❌ $file is missing"
        exit 1
    fi
done

# Check Python dependencies
echo ""
echo "🐍 Checking Python dependencies..."
if command -v python3 &> /dev/null; then
    echo "✅ Python3 is installed"
    python3 --version
else
    echo "❌ Python3 is not installed"
    exit 1
fi

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "✅ Virtual environment exists"
    source venv/bin/activate
    echo "✅ Virtual environment activated"
else
    echo "⚠️  Virtual environment not found. Creating one..."
    python3 -m venv venv
    source venv/bin/activate
    echo "✅ Virtual environment created and activated"
fi

# Install Python dependencies
echo ""
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Check Node.js dependencies
echo ""
echo "📦 Checking Node.js dependencies..."
if command -v node &> /dev/null; then
    echo "✅ Node.js is installed"
    node --version
else
    echo "❌ Node.js is not installed"
    exit 1
fi

if command -v npm &> /dev/null; then
    echo "✅ npm is installed"
    npm --version
else
    echo "❌ npm is not installed"
    exit 1
fi

# Install Node.js dependencies
echo ""
echo "📦 Installing Node.js dependencies..."
npm install

# Build React app
echo ""
echo "🏗️  Building React app..."
npm run build

if [ -d "dist" ]; then
    echo "✅ React app built successfully"
else
    echo "❌ React app build failed"
    exit 1
fi

# Check Django setup
echo ""
echo "🔧 Checking Django setup..."
python manage.py check

# Collect static files
echo ""
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Check database migrations
echo ""
echo "🗄️  Checking database migrations..."
python manage.py showmigrations

echo ""
echo "🎉 Deployment check completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Commit your changes to git"
echo "2. Push to GitHub"
echo "3. Deploy to Render using the deployment guide"
echo ""
echo "📖 See DEPLOYMENT_GUIDE.md for detailed instructions"
