# 🔧 Backend Server Restart Instructions

## Issue Fixed
Fixed database schema conflict in `order_items` table where `product_id` was `NOT NULL` but the foreign key constraint used `ON DELETE SET NULL`.

## How to Restart the Backend

### Option 1: Using PowerShell/Command Prompt
1. Open a **new terminal/command prompt**
2. Navigate to your project:
   ```powershell
   cd "C:\Users\ADMIN\Downloads\Project (3)\backend"
   ```
3. Run the server:
   ```powershell
   python run.py
   ```

### Option 2: If the server is still running
1. Press `Ctrl + C` in the terminal where the server is running
2. Wait for it to stop
3. Run again:
   ```powershell
   python run.py
   ```

### Option 3: Kill the old process first
```powershell
netstat -ano | findstr :5000
taskkill /F /PID <PID_NUMBER>
cd "C:\Users\ADMIN\Downloads\Project (3)\backend"
python run.py
```

## What Was Fixed
- Changed `product_id INT NOT NULL` to `product_id INT` (nullable)
- This allows the foreign key constraint `ON DELETE SET NULL` to work properly
- Now when a product is deleted, the order history is preserved with NULL product_id

## After Restarting
1. The server should start successfully
2. You'll see: `Backend started successfully — http://127.0.0.1:5000`
3. Your checkout functionality will work properly
4. All order operations will function correctly

## Test the Fix
1. Add products to cart
2. Click "Proceed to Checkout"
3. You should see the success popup! 🎉

