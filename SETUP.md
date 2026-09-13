# Code Review Bot - Complete Setup Guide

## System Requirements

- **Python**: 3.8 or higher
- **Node.js**: 16 or higher
- **npm**: 8 or higher
- **Git**: (optional, for version control)
- **Disk Space**: ~500MB

## Quick Start (5 minutes)

### Option 1: Automated Setup (Linux/macOS)

```bash
cd code-review-bot
chmod +x quickstart.sh
./quickstart.sh
```

Then follow the instructions printed at the end.

### Option 2: Manual Setup (All Platforms)

## Step 1: Backend Setup

### 1.1 Navigate to backend directory
```bash
cd code-review-bot/backend
```

### 1.2 Create Python virtual environment
```bash
# Linux/macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 1.3 Verify virtual environment is active
You should see `(venv)` in your terminal prompt.

### 1.4 Install dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This installs:
- Flask 2.3.3
- Flask-CORS
- Flask-SQLAlchemy
- SQLAlchemy
- python-dotenv
- Werkzeug
- Anthropic SDK (for Claude integration)
- ReportLab (for PDF export)

### 1.5 Verify installation
```bash
python -c "import flask; import sqlalchemy; print('✓ Dependencies installed')"
```

### 1.6 Run backend
```bash
python app.py
```

Expected output:
```
* Serving Flask app 'app'
* Debug mode: on
* Running on http://127.0.0.1:5000
```

**Backend is now running on port 5000**

## Step 2: Frontend Setup

### 2.1 Open new terminal and navigate to frontend
```bash
cd code-review-bot/frontend
```

### 2.2 Install Node dependencies
```bash
npm install
```

This installs:
- React 18.2
- React DOM
- Recharts (for charts)
- Lucide React (for icons)
- Vite (build tool)
- TypeScript
- Tailwind CSS (via CDN in index.html)

### 2.3 Verify installation
```bash
npm --version
node --version
```

### 2.4 Run frontend development server
```bash
npm run dev
```

Expected output:
```
  VITE v4.x.x  ready in xxx ms

  ➜  Local:   http://localhost:3000/
  ➜  press h to show help
```

**Frontend is now running on port 3000**

## Step 3: Access the Application

1. Open your browser
2. Go to http://localhost:3000
3. You should see the Code Review Bot dashboard

## Testing the Application

### Test 1: Analyze Sample Code

1. Click "Start Code Review" or "New Review"
2. Choose one of these test cases:

**Python Example with Issues:**
```python
password = "secret123"
query = "SELECT * FROM users WHERE id = " + user_id
os.system("cat " + filename)
```

3. Click "Analyze Code"
4. Wait for analysis to complete
5. Review the results dashboard

### Test 2: Check Review History

1. Click "History" in the navigation
2. You should see your completed reviews
3. Click a review to see details

### Test 3: Export Review

1. In review detail page, click "PDF"
2. A PDF file should download
3. Open it to verify formatting

### Test 4: View Analytics

1. Click "Analytics"
2. Charts should display statistics
3. Try different filters if available

## Environment Variables

### Optional: Claude API Integration

To enable AI-powered reviews:

```bash
# Create .env file in backend directory
echo 'ANTHROPIC_API_KEY=sk-your-api-key' > backend/.env
```

Get your API key from https://console.anthropic.com

If not set, analysis will use fallback rule-based review.

### Database Configuration

Default: SQLite file in backend directory

To customize:
```bash
export DATABASE_URL="sqlite:///code_review.db"
```

## Troubleshooting

### Issue: "Command not found: python3"

**Solution**: 
- Ensure Python 3 is installed
- Try `python` instead of `python3`
- Add Python to PATH

### Issue: "virtual environment not activated"

**Solution**: Run activation command again
```bash
# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### Issue: "pip: command not found"

**Solution**: 
```bash
python -m pip install -r requirements.txt
```

### Issue: "npm: command not found"

**Solution**: 
- Install Node.js from https://nodejs.org
- Restart terminal

### Issue: "Port 5000 already in use"

**Solution**: Change Flask port in `backend/app.py`:
```python
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)  # Use 5001 instead
```

Then update frontend proxy in `frontend/vite.config.ts`:
```typescript
proxy: {
  '/api': {
    target: 'http://localhost:5001',  # Update port here
    changeOrigin: true,
  },
},
```

### Issue: "Port 3000 already in use"

**Solution**: Change Vite port in `frontend/vite.config.ts`:
```typescript
server: {
  port: 3001,  // Use different port
  // ...
}
```

### Issue: "CORS error in browser console"

**Solution**: Ensure backend is running:
```bash
curl http://localhost:5000/api/health
```

Should return:
```json
{"status":"ok","timestamp":"..."}
```

### Issue: Database not initializing

**Solution**: 
1. Delete old database file:
   ```bash
   rm backend/code_review.db
   ```
2. Restart backend - it will create new database automatically

### Issue: Analysis fails

**Solution**: 
1. Check backend terminal for error messages
2. Verify code is under 50KB
3. Try simple code example first
4. Check Python syntax is valid

## Running in Production

### Using Gunicorn

```bash
cd backend
pip install gunicorn
gunicorn --bind 0.0.0.0:5000 app:app
```

### Using PM2 (Node Process Manager)

```bash
npm install -g pm2

# Terminal 1
cd backend
pm2 start "python app.py" --name "code-review-bot-backend"

# Terminal 2
cd frontend
npm run build
pm2 start "npm run preview" --name "code-review-bot-frontend"
```

## Building Frontend for Deployment

```bash
cd frontend
npm run build
```

Creates optimized build in `frontend/dist/`

Serve with any static server:
```bash
npx serve -s dist -p 3000
```

## Database Backup

```bash
# Backup SQLite database
cp backend/code_review.db backend/code_review.db.backup

# Restore from backup
cp backend/code_review.db.backup backend/code_review.db
```

## Full System Shutdown

```bash
# Press Ctrl+C in both terminal windows
# Or in process managers:
pm2 delete all
```

## Next Steps

1. **Explore Features**
   - Try different programming languages
   - Test export functionality
   - Create and share reviews

2. **Integrate Claude API**
   - Get API key from Anthropic
   - Set ANTHROPIC_API_KEY environment variable
   - Analyze code with AI review enabled

3. **Customize**
   - Modify analysis rules in `backend/analyzer/`
   - Adjust scoring in `backend/analyzer/quality_scorer.py`
   - Customize UI in `frontend/src/App.tsx`

4. **Deploy**
   - Use Docker for containerization
   - Deploy backend to cloud (Heroku, AWS, GCP)
   - Deploy frontend to CDN (Vercel, Netlify)
   - Use production database (PostgreSQL)

## Support Resources

- **Backend Issues**: Check `backend/app.py` debug output
- **Frontend Issues**: Check browser console (F12)
- **Analysis Issues**: See `backend/analyzer/` modules
- **Database Issues**: Check SQLite file permissions

## System Information

To gather system info for troubleshooting:

```bash
python --version
node --version
npm --version
pip list | grep -E "Flask|SQLAlchemy|anthropic"
```

---

**Code Review Bot is now ready to use!**

Questions or issues? Check the main README.md for more documentation.
