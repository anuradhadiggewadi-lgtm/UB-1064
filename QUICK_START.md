# ⚡ Quick Start Guide

## Get Running in 3 Minutes!

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Start the Server
**Windows:**
```bash
start.bat
```
or
```bash
python app.py
```

**Mac/Linux:**
```bash
chmod +x start.sh
./start.sh
```
or
```bash
python3 app.py
```

### Step 3: Open Your Browser
Visit: **http://localhost:5000**

### Step 4: Login
- Email: `demo@example.com`
- Password: `demo123`

### Step 5: Test It!
1. Click "Simulate Data" (auto-fills inputs)
2. Click "Predict Stress Level"
3. View your results! 🎉

---

## That's It! 🚀

You now have a fully functional stress prediction system running on your machine.

## Need More Details?

- **README.md** - Full documentation
- **SETUP.md** - Detailed setup guide  
- **PROJECT_SUMMARY.md** - Technical overview

## Troubleshooting?

### "Port already in use"
Kill the process using port 5000 or change the port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### "Module not found"
Make sure you installed dependencies:
```bash
pip install -r requirements.txt
```

### "Python not found"
Make sure Python is installed and in your PATH:
```bash
python --version  # Should show Python 3.8+
```

---

**Ready to predict stress levels! 🧘‍♀️**

