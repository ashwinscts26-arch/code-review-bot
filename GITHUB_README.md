# Code Review Bot 🚀

AI-powered code analysis tool that detects bugs, vulnerabilities, and quality issues across 9 programming languages.

**Upload. Analyze. Improve.**

---

## Features ✨

- 🔍 **Code Analysis** - Static analysis, security scanning, quality metrics
- 🤖 **AI-Powered** - Claude AI integration for intelligent code review
- 📊 **Quality Scoring** - Get 0-100 quality score with breakdown
- 🚨 **Security** - Detect 8+ vulnerability types (SQL injection, XSS, etc.)
- 📄 **Exports** - PDF, JSON, CSV reports
- 🔗 **Share** - Generate shareable links with expiration
- 📈 **Analytics** - Track history and trends
- 📱 **Responsive** - Works on desktop, tablet, mobile

---

## Quick Start 🚀

### Prerequisites
- Python 3.8+
- Node.js 16+ LTS

### 1-Click Launch

**Windows:**
```bash
Double-click: RUN_ME.bat
```

**Mac:**
```bash
Double-click: RUN_ME.command
```

**Linux:**
```bash
bash RUN_ME.sh
```

Then wait 2-3 minutes and your browser opens automatically!

---

## Technology Stack

**Backend:**
- Flask + SQLAlchemy
- Python AST analysis
- Claude AI API integration
- ReportLab for PDF export

**Frontend:**
- React 18 + TypeScript
- Vite bundler
- Recharts visualizations
- Lucide React icons

**Database:**
- SQLite (development)
- PostgreSQL ready (production)

---

## Supported Languages

Python, JavaScript, TypeScript, Java, C++, C#, Go, Ruby, PHP

---

## How It Works

1. **Upload or paste** code
2. **Analysis runs** (1-5 seconds)
3. **See results** with:
   - Quality score (0-100)
   - Detected bugs
   - Security vulnerabilities
   - Code quality issues
   - AI suggestions
4. **Export or share** the review

---

## Screenshots

- Dashboard with metrics
- Code analysis results
- Issue explorer
- Analytics dashboard
- Review history

---

## Project Structure

```
code-review-bot/
├── backend/              # Flask REST API
│   ├── app.py           # Main application
│   ├── models.py        # Database schema
│   ├── analyzer/        # Analysis engine
│   └── exports/         # PDF/JSON/CSV export
│
├── frontend/            # React application
│   ├── src/App.tsx     # Main component
│   ├── package.json    # Dependencies
│   └── index.html      # Entry point
│
├── RUN_ME.bat/sh/command  # 1-click launcher
└── README.md            # This file
```

---

## API Documentation

### Analyze Code
```bash
POST /api/analyze
Content-Type: application/json

{
  "code": "your code here",
  "filename": "example.py",
  "language": "Python"
}
```

### Get Review
```bash
GET /api/review/<review_id>
```

### Get History
```bash
GET /api/history?page=1&per_page=10
```

### Export PDF
```bash
GET /api/export/<review_id>/pdf
```

See [README.md](README.md) for complete API docs.

---

## Configuration

### Optional: Claude AI Integration

To enable AI-powered reviews:

```bash
export ANTHROPIC_API_KEY="sk-your-key-here"
```

Get your key from: https://console.anthropic.com

Without it, analysis uses rule-based review (still works perfectly).

---

## Deployment

### Docker
```bash
docker build -t code-review-bot .
docker run -p 5000:5000 -p 3000:3000 code-review-bot
```

### Manual
```bash
# Backend
cd backend
pip install -r requirements.txt
python app.py

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

---

## Testing

Test with this vulnerable code:
```python
password = "secret123"
query = "SELECT * FROM users WHERE id = " + user_id
os.system("cat " + filename)
```

---

## Performance

- Analysis: <5 seconds
- PDF Export: <2 seconds  
- API Response: <500ms
- First Load: 2-3 minutes
- Subsequent: 30-60 seconds

---

## Security

- ✅ No hardcoded secrets
- ✅ API keys not exposed
- ✅ Input validation
- ✅ SQL injection prevention (ORM)
- ✅ CORS configured
- ✅ Share links with expiration

---

## Troubleshooting

### Python not found
- Install from https://python.org
- Windows: Check "Add Python to PATH"
- Restart computer after install

### Node not found
- Install from https://nodejs.org
- Get LTS version
- Windows: Restart after install

### Port already in use
- Close other apps using ports 3000/5000
- Wait 30 seconds and try again

### Browser didn't open
- Manually go to http://localhost:3000

See [QUICK_FIX.md](QUICK_FIX.md) for more troubleshooting.

---

## Documentation

- **README.md** - Feature documentation
- **SETUP.md** - Detailed setup guide
- **1_CLICK_SETUP.txt** - Simple quick start
- **IMPLEMENTATION_SUMMARY.md** - Architecture details

---

## Perfect For

✅ College portfolios  
✅ Technical interviews  
✅ Learning code quality  
✅ Demonstrating full-stack development  
✅ Portfolio projects  

---

## Future Features

- [ ] GitHub/GitLab integration
- [ ] CI/CD pipeline integration
- [ ] Team collaboration
- [ ] Custom rule configuration
- [ ] Advanced analytics
- [ ] WebSocket real-time updates
- [ ] Docker support
- [ ] PostgreSQL support

---

## Contributing

Feel free to fork, improve, and share!

---

## License

MIT License - See LICENSE file

---

## Author

Built by Ashwin Kumar B C (@ashwinscts26-arch)

---

## Support

Having issues? Check the troubleshooting section or read the documentation files included.

---

**Built with Python, Flask, React, and Claude AI** 🚀

Give it a star if you find it useful! ⭐

