#!/bin/bash

# Star's Pixel Office - Deploy Helper Script
# Usage: ./deploy.sh [vercel|docker|manual]

set -e

DEPLOY_TYPE=${1:-vercel}

echo "🚀 Star's Pixel Office - Deploy Helper"
echo "========================================"

case $DEPLOY_TYPE in
    vercel)
        echo "📦 Preparing for Vercel deployment..."
        
        if [ ! -f ".git/config" ]; then
            echo "❌ Git repository not initialized"
            echo "Run: git init && git add . && git commit -m 'Initial commit'"
            exit 1
        fi
        
        echo "✅ Git repository found"
        echo ""
        echo "Next steps:"
        echo "1. Push to GitHub:"
        echo "   git remote add origin https://github.com/YOUR_USERNAME/star-office-ui.git"
        echo "   git push -u origin main"
        echo ""
        echo "2. Go to https://vercel.com"
        echo "3. Click 'New Project' → Import GitHub repository"
        echo "4. Vercel will auto-detect vercel.json configuration"
        echo ""
        echo "Vercel CLI (alternative):"
        echo "   npm i -g vercel"
        echo "   vercel"
        ;;
        
    docker)
        echo "🐳 Building Docker image..."
        
        if [ ! -f "Dockerfile" ]; then
            echo "❌ Dockerfile not found"
            exit 1
        fi
        
        docker build -t star-office-ui .
        
        echo "✅ Docker image built successfully"
        echo ""
        echo "Run locally:"
        echo "  docker run -p 18791:18791 star-office-ui"
        echo ""
        echo "Push to Docker Hub:"
        echo "  docker tag star-office-ui YOUR_USERNAME/star-office-ui:latest"
        echo "  docker push YOUR_USERNAME/star-office-ui:latest"
        ;;
        
    local)
        echo "🖥️  Setting up local development..."
        
        if [ -d "backend" ]; then
            cd backend
            
            if [ ! -d "venv" ]; then
                python3 -m venv venv
                source venv/bin/activate
            else
                source venv/bin/activate
            fi
            
            pip install -r requirements.txt
            
            echo "✅ Dependencies installed"
            echo ""
            echo "Start the server:"
            echo "  cd backend && source venv/bin/activate && python app.py"
            echo ""
            echo "Access:"
            echo "  http://localhost:18791/landing   (Landing page)"
            echo "  http://localhost:18791/          (Dashboard)"
            echo "  http://localhost:18791/join      (Join form)"
        else
            echo "❌ Backend directory not found"
            exit 1
        fi
        ;;
        
    *)
        echo "Usage: ./deploy.sh [vercel|docker|local]"
        echo ""
        echo "Examples:"
        echo "  ./deploy.sh vercel    - Deploy to Vercel (recommended)"
        echo "  ./deploy.sh docker    - Build Docker image"
        echo "  ./deploy.sh local     - Setup local development"
        exit 1
        ;;
esac

echo "✅ Done!"
