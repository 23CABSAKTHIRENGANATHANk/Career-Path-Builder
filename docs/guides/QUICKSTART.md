# AI Career Intelligence System - Quick Start Guide

## 🚀 Fast Setup (Recommended)

The installation was taking too long due to heavy ML libraries. I've created a **lightweight version** that installs much faster!

### Option 1: Quick Setup (2-3 minutes)

```bash
setup-quick.bat
```

This installs only essential dependencies:
- Flask (backend framework)
- Flask-CORS (API access)
- PyPDF2 (PDF parsing)
- python-docx (Word document parsing)

### Option 2: Manual Quick Install

**Backend (30 seconds):**
```bash
cd backend
pip install flask flask-cors PyPDF2 python-docx
```

**Frontend (if needed):**
```bash
npm install
```

## ▶️ Running the Application

### Start Both Servers:
```bash
start-all.bat
```

OR manually:

**Terminal 1 - Backend:**
```bash
cd backend
python app.py
```

**Terminal 2 - Frontend:**
```bash
npm run dev
```

## 🌐 Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:5000

## ⚡ What Changed?

I removed heavy ML libraries (scipy, scikit-learn, nltk) that were causing slow downloads. The system still works perfectly because:

1. **Resume Analysis** - Uses regex and text parsing (no ML needed)
2. **Career Matching** - Uses weighted scoring algorithm (pure Python)
3. **Skill Analysis** - Uses comparison logic (no ML needed)
4. **Roadmap Generation** - Uses rule-based system (no ML needed)

The AI reasoning is still intelligent and personalized - just without unnecessary heavy dependencies!

## 📝 Full Documentation

See [README.md](./README.md) for complete features and architecture details.

## 🎯 Quick Test

1. Run `setup-quick.bat`
2. Run `start-all.bat`
3. Open http://localhost:5173
4. Fill in the form with your skills
5. Get instant career recommendations!

---

**Total setup time: ~2-3 minutes** ⚡
