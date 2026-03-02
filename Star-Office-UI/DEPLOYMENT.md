# 🚀 Deployment Guide - Star's Pixel Office

## Quick Start: Deploy on Vercel (Recommended)

### Prerequisites
- GitHub account (repository)
- Vercel account (free tier works)
- Git CLI installed locally

### Step 1: Prepare Your Repository

```bash
cd your-project-folder
git init
git add .
git commit -m "Initial commit: Star's Pixel Office"
git branch -M main
```

### Step 2: Push to GitHub

```bash
# Create a new repository on GitHub (without README)
git remote add origin https://github.com/YOUR_USERNAME/star-office-ui.git
git push -u origin main
```

### Step 3: Deploy to Vercel

**Option A: Using Vercel CLI**
```bash
npm i -g vercel
vercel
# Follow prompts to connect GitHub and deploy
```

**Option B: Using Vercel Dashboard**
1. Go to [vercel.com](https://vercel.com)
2. Click "New Project"
3. Import your GitHub repository
4. Vercel will auto-detect the `vercel.json` configuration
5. Click "Deploy"

### Step 4: Configure Environment

Your Vercel project will automatically:
- Detect Python backend via `vercel.json`
- Serve static frontend files
- Serve landing page

**Live URL:**
```
https://your-project-name.vercel.app
- / → Dashboard
- /landing → Landing Page
- /join → Join Form
- /invite → Invite Guide
```

---

## Local Development

### Run Backend
```bash
cd backend
pip install -r requirements.txt
python app.py
# Now accessible at http://localhost:18791
```

### Access Locally
- Landing Page: http://localhost:18791/landing
- Dashboard: http://localhost:18791/
- Join Form: http://localhost:18771/join

---

## File Structure for Deployment

```
star-office-ui/
├── landing.html          ← Landing page (new)
├── vercel.json          ← Vercel config (new)
├── README.md
├── LICENSE
├── frontend/
│   ├── index.html       ← Main dashboard
│   ├── join.html
│   ├── invite.html
│   ├── game.js
│   ├── layout.js
│   └── fonts/
├── backend/
│   ├── app.py           ← Flask application
│   └── requirements.txt
├── docs/
└── [other files]
```

---

## Alternative: Docker Deployment

If you prefer Docker:

### Create Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "backend/app.py"]
```

### Build & Run
```bash
docker build -t star-office .
docker run -p 18791:18791 star-office
```

### Deploy to Railway, Render, or Replit
Most platforms support Docker - just upload your repository.

---

## Manual Deployment (VPS/Server)

### Install Dependencies
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip nginx

cd /home/user/star-office-ui
pip3 install -r backend/requirements.txt
```

### Setup Nginx Reverse Proxy
Create `/etc/nginx/sites-available/star-office`:
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:18791;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /static {
        alias /home/user/star-office-ui/frontend;
    }
}
```

### Run Application
```bash
cd /home/user/star-office-ui/backend
nohup python3 app.py > app.log 2>&1 &
```

---

## Features Available After Deployment

✅ Landing page with modern design  
✅ Real-time dashboard with agents  
✅ Agent join/leave functionality  
✅ Status tracking (6 states)  
✅ Responsive mobile design  
✅ WebP image optimization  
✅ Secure join key authentication  

---

## Troubleshooting

### Issue: Static files not loading
**Solution:** Check `vercel.json` routes match your file paths

### Issue: Backend not responding
**Solution:** Verify Flask is running and Vercel Python build detected

### Issue: Landing page shows blank
**Solution:** Ensure `landing.html` is in root directory

---

## Environment Variables (Optional)

Create `.env` file:
```
FLASK_ENV=production
FLASK_DEBUG=False
PYTHONUNBUFFERED=1
```

---

## Support & Next Steps

1. **Customize domain:** Add custom domain in Vercel settings
2. **Setup monitoring:** Use Vercel Analytics dashboard
3. **Add CI/CD:** Auto-deploy on git push
4. **Scale agents:** Deploy multiple instances if needed

Happy deploying! 🚀⭐
