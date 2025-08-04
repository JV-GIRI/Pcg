# 🫀 HEARTEST - AI PCG Analyzer

**Giri's AI PCG Analyzer** - Advanced Valvular Heart Disease Detection using Phonocardiography

![HEARTEST Logo](https://img.shields.io/badge/HEARTEST-AI%20PCG%20Analyzer-red?style=for-the-badge&logo=heart)
![Gemini AI](https://img.shields.io/badge/Powered%20by-Gemini%202.5%20Pro-blue?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-ff6b6b?style=for-the-badge)

## 🎯 Overview

HEARTEST is a cutting-edge medical diagnostics application that leverages Google's Gemini 2.5 Pro AI to analyze phonocardiography (PCG) signals for detecting valvular heart diseases. The application provides real-time analysis of heart sounds from 4 valve sites and generates comprehensive medical reports.

## ✨ Key Features

### 🤖 AI-Powered Diagnosis
- **Real Gemini 2.5 Pro Integration**: Advanced AI analysis of PCG signals
- **8 Disease Detection**: AS, AR, PS, PR, TS, TR, MS, MR
- **4 Valve Sites**: Aortic (AV), Pulmonary (PV), Tricuspid (TV), Mitral (MV)

### 🎨 Modern Animated UI
- **Lottie Animations**: Heartbeat, medical loading, AI brain animations
- **Gradient Backgrounds**: Medical-themed color schemes
- **Floating Elements**: Interactive valve selectors with glow effects
- **Audio Visualizer**: Real-time waveform animations
- **Smooth Transitions**: CSS animations for better UX

### 👤 Comprehensive Patient Management
- **Patient Demographics**: Name, age, gender, height, weight
- **Auto BMI Calculation**: Real-time BMI computation
- **Clinical Notes**: Detailed medical observations
- **Phone Integration**: WhatsApp sharing capabilities

### 📊 Advanced PCG Analysis
- **Audio Upload/Recording**: Support for .wav files and live recording
- **Signal Processing**: Noise reduction and waveform analysis
- **Spectral Analysis**: Frequency domain features extraction
- **Interactive Plots**: Plotly-powered visualizations

### 📄 Professional Reporting
- **PDF Generation**: Comprehensive medical reports
- **WhatsApp Sharing**: Instant report sharing via WhatsApp
- **Case History**: Complete patient diagnosis tracking
- **Download Options**: PDF download and print functionality

### 💾 Data Management
- **Supabase Integration**: Cloud database storage
- **Local Fallback**: Local JSON storage when offline
- **Case Tracking**: Historical diagnosis records
- **Data Security**: Secure patient information handling

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- Streamlit
- Google Gemini API Key (optional, will use simulation mode without)
- Supabase Account (optional, will use local storage without)

### 1. Clone the Repository
```bash
git clone <repository-url>
cd heartest-pcg-analyzer
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a `.env` file based on `.env.example`:
```bash
cp .env.example .env
```

Edit `.env` with your credentials:
```env
# Google Gemini AI Configuration
GOOGLE_API_KEY=your_google_gemini_api_key_here

# Supabase Configuration (Optional)
SUPABASE_URL=your_supabase_project_url_here
SUPABASE_KEY=your_supabase_anon_key_here

# App Configuration
APP_NAME=HEARTEST
APP_DESCRIPTION=Giri's AI PCG analyzer
```

### 4. Run the Application
```bash
streamlit run streamlit_app.py
```

## 📱 Usage Guide

### Step 1: Patient Information
1. Navigate to **"👤 Patient Info"** tab
2. Fill in patient demographics:
   - Full Name
   - Age
   - Gender
   - Height (cm)
   - Weight (kg)
   - Phone Number (for WhatsApp sharing)
   - Clinical Notes
3. BMI is automatically calculated
4. Click **"💾 Save Patient Information"**

### Step 2: PCG Analysis
1. Go to **"🔍 Diagnosis"** tab
2. Select valve site (AV, PV, TV, or MV)
3. Upload .wav file OR record audio live
4. Click **"🤖 Analyze with Gemini AI"**
5. View diagnosis results with confidence levels

### Step 3: Generate Reports
1. Click **"📄 Generate PDF Report"** for professional documentation
2. Use **"📱 Share via WhatsApp"** for instant sharing
3. Access **"📚 Case History"** for previous diagnoses

## 🧠 AI Analysis Features

### Supported Valve Diseases
| Code | Disease Name | Valve Site |
|------|-------------|------------|
| AS | Aortic Stenosis | Aortic Valve |
| AR | Aortic Regurgitation | Aortic Valve |
| PS | Pulmonary Stenosis | Pulmonary Valve |
| PR | Pulmonary Regurgitation | Pulmonary Valve |
| TS | Tricuspid Stenosis | Tricuspid Valve |
| TR | Tricuspid Regurgitation | Tricuspid Valve |
| MS | Mitral Stenosis | Mitral Valve |
| MR | Mitral Regurgitation | Mitral Valve |

### Analysis Output
- **Primary Diagnosis**: Main detected condition
- **Confidence Level**: AI confidence percentage (0-100%)
- **Severity Assessment**: Mild/Moderate/Severe classification
- **Clinical Findings**: Detailed observations
- **Recommendations**: Follow-up suggestions

## 🎨 Animation Features

### Interactive Elements
- **Heartbeat Header**: Animated heart logo
- **Loading Animations**: Medical-themed loading screens
- **Valve Selector**: Floating, color-coded valve buttons
- **Audio Visualizer**: Real-time waveform animation
- **Progress Bars**: Animated analysis progress
- **Success Notifications**: Celebration animations

### UI Enhancements
- **Gradient Backgrounds**: Medical blue-purple gradients
- **Glass Morphism**: Semi-transparent cards with blur effects
- **Hover Effects**: Interactive button animations
- **Slide Transitions**: Smooth page transitions
- **Pulse Effects**: Attention-grabbing animations

## 📊 Technical Architecture

```
HEARTEST/
├── streamlit_app.py          # Main application
├── config.py                 # Configuration settings
├── database.py               # Supabase integration
├── ai_analyzer.py            # Gemini AI integration
├── pdf_generator.py          # Report generation
├── whatsapp_integration.py   # WhatsApp sharing
├── animations.py             # UI animations
├── requirements.txt          # Dependencies
├── .env.example             # Environment template
└── README.md                # Documentation
```

## 🔧 Configuration Options

### Audio Processing
- **Sample Rate**: 44.1 kHz (configurable)
- **Supported Formats**: WAV
- **Duration Limits**: 2-30 seconds
- **Noise Reduction**: Butterworth filter

### AI Analysis
- **Model**: Gemini 2.5 Pro
- **Fallback**: Simulation mode when API unavailable
- **Features**: Spectral analysis, heart rate estimation
- **Output**: Structured medical diagnosis

### Database Options
- **Primary**: Supabase (cloud)
- **Fallback**: Local JSON files
- **Tables**: Patients, Cases
- **Relationships**: Patient → Multiple Cases

## 📱 WhatsApp Integration

### Features
- **Report Sharing**: Automatic message generation
- **Phone Validation**: Indian mobile number support
- **Custom Messages**: Medical report templates
- **Follow-up Reminders**: Appointment scheduling

### Message Template
```
🩺 HEARTEST Medical Report

👤 Patient: [Name]
📋 Diagnosis: [Result]
📄 Report: [Filename]

Generated by HEARTEST - Giri's AI PCG Analyzer
Advanced AI-powered phonocardiography analysis

⚠️ This report is for medical reference only.
```

## ⚠️ Important Disclaimers

### Medical Disclaimer
**This application is for educational and research purposes only. It should not be used as a substitute for professional medical diagnosis or treatment. Always consult with a qualified healthcare provider for proper medical evaluation and care.**

### AI Limitations
- The AI analysis is based on signal processing and pattern recognition
- Results should be validated by medical professionals
- False positives/negatives are possible
- Clinical correlation is essential

### Data Privacy
- Patient data is handled securely
- Local storage option available for privacy
- No data is shared without explicit user action
- HIPAA compliance considerations apply

## 🛠️ Development

### Adding New Animations
1. Edit `animations.py`
2. Add new Lottie animation URLs
3. Create animation methods
4. Integrate in main application

### Extending AI Analysis
1. Modify `ai_analyzer.py`
2. Update feature extraction
3. Enhance Gemini prompts
4. Add new disease classifications

### Custom Reports
1. Edit `pdf_generator.py`
2. Modify report templates
3. Add new sections
4. Update styling

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Gemini AI** for advanced language model capabilities
- **Streamlit** for the amazing web framework
- **Supabase** for database infrastructure
- **Lottie** for beautiful animations
- **Medical Community** for validation and feedback

## 📞 Support

For support, email [your-email] or create an issue in the repository.

---

<div align="center">

**🫀 Developed with ❤️ for advancing cardiac diagnostics**

![Powered by AI](https://img.shields.io/badge/Powered%20by-AI-brightgreen)
![Medical Grade](https://img.shields.io/badge/Medical%20Grade-Analysis-red)
![Real Time](https://img.shields.io/badge/Real%20Time-Processing-blue)

</div>