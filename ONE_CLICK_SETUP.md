# 🚀 One-Click Setup & Launch

## ⚡ FASTEST WAY TO START

### For Linux/macOS Users

1. **First Time Only - Install Dependencies**
   ```bash
   cd code-review-bot
   chmod +x START.sh
   ./START.sh
   ```

2. **Every Time After - Just Click**
   Double-click `START.sh` or run:
   ```bash
   ./START.sh
   ```

### For Windows Users

1. **First Time Only - Install Dependencies**
   - Extract the project folder
   - Double-click `START.bat`
   - Wait for installation to complete

2. **Every Time After - Just Click**
   - Double-click `START.bat`
   - Browser opens automatically

---

## 📋 What The Script Does

When you click `START.sh` (Mac/Linux) or `START.bat` (Windows), it automatically:

1. ✅ Checks Python is installed
2. ✅ Checks Node.js is installed  
3. ✅ Creates Python virtual environment (first time)
4. ✅ Installs Python dependencies (first time)
5. ✅ Installs Node packages (first time)
6. ✅ Starts Flask backend (port 5000)
7. ✅ Waits for backend to be ready
8. ✅ Starts npm frontend (port 3000)
9. ✅ Waits for frontend to be ready
10. ✅ **Opens browser automatically**
11. ✅ Shows you the application ready to use

**Everything happens in the background - you just see a single terminal with status updates!**

---

## 🖥️ System Requirements (One-Time Setup)

### Windows
1. Download and install Python 3.8+
   - https://www.python.org/downloads/
   - ✅ Check "Add Python to PATH" during install

2. Download and install Node.js 16+
   - https://nodejs.org/
   - Use the LTS version

3. That's it! Just run `START.bat`

### macOS
1. Install Python 3 (usually pre-installed)
   ```bash
   python3 --version
   ```

2. Install Node.js
   ```bash
   brew install node
   ```

3. Run the script
   ```bash
   ./START.sh
   ```

### Linux
1. Install Python 3
   ```bash
   sudo apt-get install python3 python3-venv
   ```

2. Install Node.js
   ```bash
   sudo apt-get install nodejs npm
   ```

3. Run the script
   ```bash
   ./START.sh
   ```

---

## ✅ Verification After First Run

After the first launch, you should see:

```
================================
✓ Application Started!
================================

Frontend: http://localhost:3000
Backend:  http://localhost:5000

Press Ctrl+C to stop the application
```

**And your browser automatically opens to http://localhost:3000**

---

## 🎯 Using The Application

1. **Dashboard** loads automatically
2. Click "Start Code Review"
3. Paste some Python code:
   ```python
   password = "secret123"
   query = "SELECT * FROM users WHERE id = " + user_id
   ```
4. Click "Analyze Code"
5. See results instantly!

---

## 🛑 Stopping The Application

### On Mac/Linux
Press `Ctrl+C` in the terminal

### On Windows
- Backend window: Close the window
- Frontend window: Press `Ctrl+C`

---

## 🔧 Troubleshooting

### "Python not found"
- **Windows**: Reinstall Python and check "Add Python to PATH"
- **Mac/Linux**: Run `python3 --version` to verify installation

### "Node.js not found"
- Install from https://nodejs.org/
- Make sure to use a recent LTS version (16+)

### "Port 5000 already in use"
The backend couldn't start. Try:
1. Close other applications using port 5000
2. Wait 30 seconds and try again
3. Or manually change the port in `backend/app.py`

### "Port 3000 already in use"
The frontend couldn't start. Try:
1. Close other applications using port 3000
2. Wait 30 seconds and try again
3. Or change port in `frontend/vite.config.ts`

### Browser didn't open
It's fine - manually go to **http://localhost:3000**

---

## 💡 Pro Tips

### Create a Desktop Shortcut (Windows)
1. Right-click `START.bat`
2. Select "Create shortcut"
3. Move shortcut to Desktop
4. Double-click from Desktop to launch

### Create an App Launcher (Mac)
1. Open Automator
2. Select "Application"
3. Add action: "Run Shell Script"
4. Paste: `/path/to/code-review-bot/START.sh`
5. Save as application on Desktop

### Run in Background (Advanced)
**Linux/Mac:**
```bash
./START.sh &
```

**Windows PowerShell:**
```powershell
Start-Process "START.bat" -WindowStyle Minimized
```

---

## 📊 First Launch Timing

- **First Time**: 2-3 minutes (downloads & installs everything)
- **After That**: 30-60 seconds (quick startup)

---

## ✨ That's It!

You now have a **one-click launcher** that:
- Installs everything automatically
- Starts both servers
- Opens the browser
- Shows status updates

No more terminal commands. Just click and go! 🚀

---

**Questions?** Check the main README.md or SETUP.md for detailed documentation.
