# Railway Deployment Guide

This guide will walk you through deploying your backend and frontend to Railway.

## Prerequisites

1. A GitHub account
2. A Railway account (sign up at https://railway.app)
3. Your code pushed to a GitHub repository

---

## Step 1: Prepare Your Repository

1. **Push your code to GitHub** (if not already done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

---

## Step 2: Deploy Backend to Railway

### 2.1 Create a New Project

1. Go to [Railway Dashboard](https://railway.app/dashboard)
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose your repository
5. Railway will detect it's a Python project

### 2.2 Add MySQL Database

1. In your Railway project, click **"+ New"**
2. Select **"Database"** → **"Add MySQL"**
3. Railway will automatically create a MySQL database
4. Note: Railway will automatically set environment variables for the MySQL connection

### 2.3 Configure Environment Variables

1. Click on your **backend service** in Railway
2. Go to the **"Variables"** tab
3. Add the following environment variables:

   **Required Variables:**
   ```
   SECRET_KEY=<generate-a-random-secret-key>
   MYSQL_HOST=${{MySQL.MYSQLHOST}}
   MYSQL_PORT=${{MySQL.MYSQLPORT}}
   MYSQL_USER=${{MySQL.MYSQLUSER}}
   MYSQL_PASSWORD=${{MySQL.MYSQLPASSWORD}}
   MYSQL_DATABASE=${{MySQL.MYSQLDATABASE}}
   ```

   **Optional Variables:**
   ```
   FLASK_DEBUG=0
   MYSQL_POOL_SIZE=5
   MYSQL_POOL_NAME=app_pool
   ```

   **Note:** The `${{MySQL.*}}` syntax references Railway's MySQL service variables automatically.

### 2.4 Set Root Directory (if needed)

1. In your backend service settings, go to **"Settings"** tab
2. If your backend code is in a `backend/` folder, set:
   - **Root Directory:** `backend`

### 2.5 Deploy

1. Railway will automatically detect the `Procfile` and start deploying
2. Check the **"Deployments"** tab to see the build logs
3. Once deployed, Railway will provide a public URL (e.g., `https://your-app.railway.app`)

---

## Step 3: Deploy Frontend to Railway

### 3.1 Update Frontend API URLs

**IMPORTANT:** Before deploying, update all frontend JavaScript files to use your Railway backend URL.

1. **Get your backend URL** from Railway (e.g., `https://your-backend.railway.app`)

2. **Update the following files:**
   - `shop.js` - Line 1: Change `const API_URL = 'http://127.0.0.1:5000/api';`
   - `cart.js` - Line 1: Change `const API_URL = 'http://127.0.0.1:5000/api';`
   - `orders.js` - Line 1: Change `const API_URL = 'http://127.0.0.1:5000/api';`
   - `admin.js` - Line 1: Change `const API_URL = 'http://127.0.0.1:5000/api';`
   - `register.js` - Line 55: Change `'http://127.0.0.1:5000/api/register'`

3. **Replace with your Railway backend URL:**
   ```javascript
   const API_URL = 'https://your-backend.railway.app/api';
   ```

   **Example:**
   ```javascript
   // In shop.js, cart.js, orders.js, admin.js
   const API_URL = 'https://stationary-backend-production.up.railway.app/api';
   
   // In register.js (line 55)
   const res = await fetch('https://stationary-backend-production.up.railway.app/api/register', {
   ```

### 3.2 Deploy Frontend Using Static Server

A simple Flask server (`frontend-server.py`) is provided to serve your frontend files.

1. **In your Railway project, click "+ New"**
2. **Select "Deploy from GitHub repo"**
3. **Choose the same repository**
4. **Configure the service:**
   - **Root Directory:** Leave empty (or set to root if files are in root)
   - **Build Command:** (leave empty, Railway will auto-detect)
   - **Start Command:** `python frontend-server.py`

5. **Set Environment Variables (optional):**
   - `PORT` - Railway sets this automatically
   - You can add `API_URL` if you want to use it in the server

6. **Alternative: Use the Procfile**
   - Railway will automatically detect `frontend-Procfile` if you rename it to `Procfile` in the root
   - Or create a separate service with root directory set appropriately

### 3.3 Alternative: Deploy Frontend as Separate Service

If you want to keep frontend files in a subdirectory:

1. Create a new service in Railway
2. Set **Root Directory** to the directory containing your frontend files
3. Use `frontend-Procfile` and `frontend-requirements.txt`
4. Railway will serve your HTML/JS/CSS files

---

## Step 4: Configure CORS (if needed)

Your backend already has CORS enabled. If you need to restrict it to specific origins:

1. Update `backend/app/__init__.py`:
   ```python
   CORS(app, origins=["https://your-frontend.railway.app"])
   ```

---

## Step 5: Verify Frontend-Backend Connection

1. **Test the connection:**
   - Open your frontend URL in a browser
   - Open browser DevTools (F12) → Console tab
   - Check for any CORS or connection errors

2. **If you see CORS errors:**
   - The backend already has CORS enabled for all origins
   - If issues persist, check the backend logs in Railway

3. **Update CORS if needed:**
   - If you want to restrict CORS to specific origins, update `backend/app/__init__.py`:
   ```python
   CORS(app, origins=["https://your-frontend.railway.app"])
   ```

---

## Step 6: Database Initialization

The database tables will be automatically created when the app starts (via `init_db()` in `app/__init__.py`).

To seed initial data:
1. Use Railway's CLI or web console to run:
   ```bash
   python seed_products.py
   ```
   (You may need to set environment variables first)

---

## Step 7: Custom Domain (Optional)

1. In Railway, go to your service **"Settings"**
2. Click **"Generate Domain"** or add a custom domain
3. Update your frontend API URLs if you change the domain

---

## Troubleshooting

### Backend won't start
- Check the **Deployments** tab for error logs
- Verify all environment variables are set correctly
- Ensure `requirements.txt` includes all dependencies

### Database connection errors
- Verify MySQL service is running
- Check that MySQL environment variables are correctly referenced
- Ensure the database service is in the same Railway project

### CORS errors
- Verify CORS is enabled in backend
- Check that frontend URL matches CORS allowed origins
- Review browser console for specific CORS error messages

### Port binding errors
- Railway automatically sets the `PORT` environment variable
- The app is configured to use `PORT` or fallback to 5000
- Ensure the app binds to `0.0.0.0` (already configured)

---

## Environment Variables Reference

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `PORT` | Railway sets this automatically | 5000 | No |
| `SECRET_KEY` | Flask secret key | 'change-me' | **Yes** |
| `MYSQL_HOST` | MySQL host | 127.0.0.1 | **Yes** |
| `MYSQL_PORT` | MySQL port | 3306 | **Yes** |
| `MYSQL_USER` | MySQL username | root | **Yes** |
| `MYSQL_PASSWORD` | MySQL password | '' | **Yes** |
| `MYSQL_DATABASE` | MySQL database name | app_db | **Yes** |
| `FLASK_DEBUG` | Enable debug mode | 1 | No |
| `MYSQL_POOL_SIZE` | Connection pool size | 5 | No |

---

## Quick Start Checklist

- [ ] Code pushed to GitHub
- [ ] Railway account created
- [ ] Backend service deployed
- [ ] MySQL database added
- [ ] Environment variables configured
- [ ] Backend URL obtained
- [ ] Frontend deployed (or configured)
- [ ] Frontend API URLs updated in all JS files
- [ ] Frontend service deployed
- [ ] Database initialized
- [ ] Test the deployment

---

## Railway CLI (Optional)

You can also use Railway CLI for deployment:

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Link project
railway link

# Deploy
railway up
```

---

## Support

- Railway Docs: https://docs.railway.app
- Railway Discord: https://discord.gg/railway

