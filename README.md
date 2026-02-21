# 🧘 ZenStressy - Stress Prediction System

A comprehensive stress prediction and wellness monitoring system that uses real-time wearable device data to predict stress levels and provide personalized recommendations.

## Features

- **Stunning Animated Homepage**: Interactive animations, floating shapes, and modern gradients
- **Real-time Monitoring**: Track heart rate, sleep cycle, and step count from wearable devices
- **AI-Powered Predictions**: Machine learning algorithms predict stress levels accurately
- **Personalized Recommendations**: Get tailored tips based on your stress level
- **Beautiful UI**: Modern, responsive design with intuitive user experience
- **Flexible Authentication**: Use any email and password to sign in
- **Comprehensive Dashboard**: View predictions and recommendations in real-time

## Tech Stack

- **Backend**: Flask (Python)
- **Machine Learning**: Scikit-learn (Random Forest Classifier)
- **Frontend**: HTML, CSS, JavaScript
- **Data Processing**: NumPy, Pandas

## Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd zenstressy
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. **Start the Flask server**
   ```bash
   python app.py
   ```
   The server will display access URLs including your network IP!

2. **Open your browser**
   - **On same device**: Navigate to `http://localhost:5000`
   - **On other devices**: Use the IP address shown (e.g., `http://192.168.1.100:5000`)
   - Make sure devices are on the **same Wi-Fi network**

3. **Configure Firewall** (for network access)
   - Run `allow_firewall.bat` as Administrator
   - OR manually allow Python through Windows Firewall
   - See `NETWORK_ACCESS.md` for details

4. **Login**
   - **Note**: You can use any email and password to sign in!
   - **Example**: yourname@email.com with any password

## Usage

### Home Page
- Beautiful landing page with feature overview
- Click "Get Started" to proceed to login

### Login Page
- Enter your email and password
- Demo credentials are provided for testing

### Dashboard
1. **Enter Wearable Data**:
   - Heart Rate (beats per minute)
   - Sleep Hours
   - Steps Count
   - Resting Heart Rate
   - Sleep Quality (1-10 scale)

2. **Predict Stress Level**:
   - Click "Predict Stress Level" to analyze your data
   - View prediction results with confidence scores
   - Get personalized recommendations

3. **Simulate Data** (Optional):
   - Click "Simulate Data" to auto-fill with realistic sample data

## Stress Levels

- **Low**: Congratulations! You're maintaining a healthy balance
- **Medium**: Moderate stress detected - some adjustments recommended
- **High**: High stress detected - immediate intervention recommended

## Recommendations

The system provides personalized recommendations based on your stress level:

- **Low Stress**: Positive reinforcement and maintenance tips
- **Medium Stress**: Moderate interventions and lifestyle adjustments
- **High Stress**: Immediate stress-reduction techniques and support

## Model Details

The stress prediction model uses a Random Forest Classifier trained on:
- Heart rate variations
- Sleep duration and quality
- Physical activity (steps)
- Resting heart rate
- Multiple physiological indicators

The model is trained on synthetic data that captures realistic patterns of stress indicators.

## Project Structure

```
zenstressy/
├── app.py                 # Flask backend
├── requirements.txt       # Python dependencies
├── templates/            # HTML templates
│   ├── home.html
│   ├── login.html
│   └── dashboard.html
├── static/
│   ├── css/
│   │   └── style.css     # Styling
│   └── js/
│       ├── login.js      # Login logic
│       └── dashboard.js  # Dashboard logic
└── README.md
```

## Future Enhancements

- Integration with real wearable devices (Fitbit, Apple Watch, etc.)
- Historical data tracking and trends
- Advanced analytics and insights
- User profile management
- Database integration for data persistence
- Mobile app development
- Integration with meditation and wellness apps

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Contact

For questions or support, please open an issue on GitHub.

---

**Made with ❤️ for better mental health and wellness**

