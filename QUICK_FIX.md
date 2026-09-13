# ⚡ QUICK FIX - Path Issue Resolved

## The Problem You Encountered

```
ERROR: Could not open requirements.txt: [Errno 2] No such file or directory: 'requirements.txt'
```

**What happened:**
- The script ran from the wrong directory
- It tried to find `requirements.txt` in the current folder instead of `backend/` folder
- This caused the installation to fail

---

## ✅ The Solution

I've created **FIXED versions** of the startup scripts:

### **For Windows:** Use `START_FIXED.bat`
```bash
Double-click: START_FIXED.bat
```

### **For Mac/Linux:** Use `START_FIXED.sh`
```bash
cd code-review-bot
chmod +x START_FIXED.sh
./START_FIXED.sh
```

---

## What Changed

The fixed scripts now:
1. ✅ Properly detect the script directory
2. ✅ Change to `backend/` before looking for `requirements.txt`
3. ✅ Change to `frontend/` before looking for `package.json`
4. ✅ Show clear error messages if files are missing
5. ✅ Verify dependencies are installed before starting

---

## Try Again Now

1. **Delete the old script files** (optional)
2. **Use `START_FIXED.bat` (Windows)** or **`START_FIXED.sh` (Mac/Linux)**
3. **Wait 2-3 minutes** for installation
4. **Browser opens automatically** ✨

---

## If You Still Get Errors

### Error: "Cannot find venv"
```bash
# Windows
cd code-review-bot\backend
python -m venv venv

# Mac/Linux
cd code-review-bot/backend
python3 -m venv venv
```

### Error: "Cannot find requirements.txt"
Make sure you have the complete folder structure:
```
code-review-bot/
├── START_FIXED.sh (or START_FIXED.bat)
├── backend/
│   ├── requirements.txt ← This file must exist
│   ├── app.py
│   └── ...
└── frontend/
    ├── package.json ← This file must exist
    ├── src/App.tsx
    └── ...
```

### Error: "Cannot find package.json"
```bash
cd code-review-bot/frontend
npm install
```

---

## 🚀 MANUAL SETUP (If Script Doesn't Work)

### Step 1: Backend Setup
```bash
cd code-review-bot/backend
python -m venv venv                    # Windows: venv\Scripts\activate
source venv/bin/activate              # Mac/Linux
pip install -r requirements.txt
python app.py
```

The backend should start on **http://localhost:5000**

### Step 2: Frontend Setup (New Terminal)
```bash
cd code-review-bot/frontend
npm install
npm run dev
```

The frontend should start on **http://localhost:3000**

### Step 3: Open Browser
Go to **http://localhost:3000**

---

## ✨ That's It!

The fixed scripts should work now. If you still have issues:

1. Make sure Python 3.8+ is installed and in PATH
2. Make sure Node.js 16+ LTS is installed
3. Make sure you have the complete project folder
4. Try the manual setup above

---

## 📋 Checklist

Before running:
- [ ] Python 3.8+ installed (`python --version`)
- [ ] Node.js 16+ installed (`node --version`)
- [ ] Complete project folder downloaded
- [ ] Using `START_FIXED.bat` or `START_FIXED.sh`
- [ ] Running from project root directory

After running:
- [ ] Backend shows "Running on http://127.0.0.1:5000"
- [ ] Frontend shows "Local: http://localhost:3000"
- [ ] Browser opens automatically
- [ ] Dashboard page loads

---

**Try the fixed script now!** 🚀

If it works, you can delete the old `START.sh` and `START.bat` files.

