# Quick Setup Guide

## Prerequisites
- Python 3.8 or higher
- pip package manager

## Installation Steps

### 1. Open Terminal/Command Prompt
Navigate to the project directory:
```bash
cd zenstressy
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
python app.py
```

You should see output like:
```
Model initialized and trained successfully
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://0.0.0.0:5000
```

### 4. Access the Application
Open your web browser and navigate to:
```
http://localhost:5000
```

## Demo Login Credentials
- **Email**: demo@example.com
- **Password**: demo123

## Testing the Application

### Step 1: Login
1. From the home page, click "Get Started"
2. Enter the demo credentials
3. Click "Sign In"

### Step 2: Enter Wearable Data
On the dashboard, you can either:
- **Option A**: Manually enter your data in the input fields
- **Option B**: Click "Simulate Data" to auto-fill with realistic sample data

### Step 3: Predict Stress Level
1. Click "Predict Stress Level"
2. View your stress level prediction
3. Review personalized recommendations

## Sample Data for Testing

Try these different scenarios:

### Low Stress (Good Health)
- Heart Rate: 65 bpm
- Sleep Hours: 8.5
- Steps Count: 10000
- Resting HR: 58 bpm
- Sleep Quality: 8

### Medium Stress
- Heart Rate: 85 bpm
- Sleep Hours: 6.5
- Steps Count: 5000
- Resting HR: 68 bpm
- Sleep Quality: 6

### High Stress
- Heart Rate: 110 bpm
- Sleep Hours: 5.0
- Steps Count: 3000
- Resting HR: 75 bpm
- Sleep Quality: 4

## Troubleshooting

### Port Already in Use
If you get an error about port 5000 being in use:
1. Close any other Flask applications
2. Or modify `app.py` to use a different port:
   ```python
   app.run(debug=True, host='0.0.0.0', port=5001)
   ```

### Import Errors
If you get import errors:
```bash
pip install --upgrade -r requirements.txt
```

### Model Not Loading
The model trains automatically on first run. Wait for the "Model initialized and trained successfully" message.

## Next Steps

- Integrate with real wearable device APIs (Fitbit, Apple Watch, etc.)
- Add database for storing historical data
- Implement user registration
- Add data visualization charts
- Create mobile app version

## Support

If you encounter any issues, check the console output for error messages and ensure all dependencies are properly installed.

