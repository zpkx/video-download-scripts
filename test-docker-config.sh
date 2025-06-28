#!/bin/bash

# Test script to verify Docker configuration works with config folder

echo "🧪 Testing Docker Configuration with Config Folder Support"
echo "=========================================================="

# Test 1: Check if docker-run.sh is executable
echo
echo "Test 1: Checking docker-run.sh executable..."
if [ -x "./docker-run.sh" ]; then
    echo "✅ docker-run.sh is executable"
else
    echo "❌ docker-run.sh is not executable"
    chmod +x docker-run.sh
    echo "✅ Made docker-run.sh executable"
fi

# Test 2: Check config folder structure
echo
echo "Test 2: Checking config folder structure..."
if [ -d "./config" ]; then
    echo "✅ config/ folder exists"
    echo "   Contents:"
    ls -la config/ | sed 's/^/     /'
else
    echo "❌ config/ folder does not exist"
    exit 1
fi

# Test 3: Check for required config files
echo
echo "Test 3: Checking required config files..."
files=("config/urls.yaml" "config/config.yaml" "config/cookies.txt")
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file exists"
    else
        echo "❌ $file missing"
    fi
done

# Test 4: Test docker-run.sh help command
echo
echo "Test 4: Testing docker-run.sh help command..."
if ./docker-run.sh help >/dev/null 2>&1; then
    echo "✅ docker-run.sh help command works"
else
    echo "❌ docker-run.sh help command failed"
fi

# Test 5: Validate docker-compose configuration
echo
echo "Test 5: Validating docker-compose configuration..."
if command -v docker-compose >/dev/null 2>&1; then
    if docker-compose config >/dev/null 2>&1; then
        echo "✅ docker-compose.yml is valid"
    else
        echo "❌ docker-compose.yml has errors"
    fi
else
    echo "⚠️  docker-compose not available, skipping validation"
fi

# Test 6: Check volume mount paths in docker-compose
echo
echo "Test 6: Checking volume mount configuration..."
if grep -q "./config:/app/config" docker-compose.yml; then
    echo "✅ Config folder volume mount configured correctly"
else
    echo "❌ Config folder volume mount not found in docker-compose.yml"
fi

if grep -q "./downloads:/downloads" docker-compose.yml; then
    echo "✅ Downloads folder volume mount configured correctly"
else
    echo "❌ Downloads folder volume mount not found in docker-compose.yml"
fi

# Test 7: Check Dockerfile includes config folder
echo
echo "Test 7: Checking Dockerfile configuration..."
if grep -q "COPY config/ ./config/" Dockerfile; then
    echo "✅ Dockerfile copies config folder"
else
    echo "❌ Dockerfile does not copy config folder"
fi

echo
echo "🎉 Docker configuration test completed!"
echo
echo "Next steps:"
echo "1. Run: ./docker-run.sh build"
echo "2. Add your URLs to config/urls.yaml"
echo "3. Run: ./docker-run.sh download"
