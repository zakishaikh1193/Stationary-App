# Quick Start: Railway Deployment

## Backend is Ready! ✅

Your backend has been configured for Railway deployment with:
- ✅ `requirements.txt` - All Python dependencies
- ✅ `Procfile` - Railway start command
- ✅ `railway.json` - Railway configuration
- ✅ Updated `run.py` - Uses Railway's PORT and binds to 0.0.0.0
- ✅ Environment variable support in `config.py`

## Quick Deployment Steps

### 1. Backend Deployment (5 minutes)

1. Push code to GitHub
2. Go to [Railway](https://railway.app) → New Project → Deploy from GitHub
3. Add MySQL database service
4. Set environment variables:
   ```
   SECRET_KEY=<random-string>
   MYSQL_HOST=${{MySQL.MYSQLHOST}}
   MYSQL_PORT=${{MySQL.MYSQLPORT}}
   MYSQL_USER=${{MySQL.MYSQLUSER}}
   MYSQL_PASSWORD=${{MySQL.MYSQLPASSWORD}}
   MYSQL_DATABASE=${{MySQL.MYSQLDATABASE}}
   ```
5. Set Root Directory to `backend` (if backend code is in backend/ folder)
6. Deploy! Get your backend URL

### 2. Frontend Deployment (5 minutes)

1. **Update API URLs** in these files:
   - `shop.js` (line 1)
   - `cart.js` (line 1)
   - `orders.js` (line 1)
   - `admin.js` (line 1)
   - `register.js` (line 55)
   
   Change: `http://127.0.0.1:5000/api` → `https://YOUR-BACKEND-URL.railway.app/api`

2. In Railway → New Service → Same repo
3. Start Command: `python frontend-server.py`
4. Deploy!

## Files Created

- `backend/requirements.txt` - Python dependencies
- `backend/Procfile` - Backend start command
- `backend/railway.json` - Railway config
- `frontend-server.py` - Frontend static server
- `frontend-requirements.txt` - Frontend dependencies
- `frontend-Procfile` - Frontend start command
- `.gitignore` - Git ignore rules
- `backend/RAILWAY_DEPLOYMENT.md` - Full detailed guide

## Need Help?

See `backend/RAILWAY_DEPLOYMENT.md` for detailed step-by-step instructions.

