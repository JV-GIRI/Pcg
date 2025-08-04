import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# App Configuration
APP_NAME = "HEARTEST"
APP_DESCRIPTION = "Giri's AI PCG analyzer"
APP_VERSION = "1.0.0"

# API Keys
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Medical Configuration
VALVE_SITES = {
    "AV": "Aortic Valve",
    "PV": "Pulmonary Valve", 
    "TV": "Tricuspid Valve",
    "MV": "Mitral Valve"
}

VALVE_DISEASES = {
    "AS": "Aortic Stenosis",
    "AR": "Aortic Regurgitation",
    "PS": "Pulmonary Stenosis",
    "PR": "Pulmonary Regurgitation",
    "TS": "Tricuspid Stenosis",
    "TR": "Tricuspid Regurgitation",
    "MS": "Mitral Stenosis",
    "MR": "Mitral Regurgitation"
}

# Audio Processing Parameters
SAMPLE_RATE = 44100
AUDIO_FORMAT = "wav"
MAX_DURATION = 30  # seconds
MIN_DURATION = 2   # seconds

# File Storage
UPLOAD_FOLDER = "uploaded_audios"
REPORTS_FOLDER = "reports"
TEMP_FOLDER = "temp"

# Gemini AI Prompts
GEMINI_PCG_ANALYSIS_PROMPT = """
You are an expert cardiologist AI analyzing phonocardiography (PCG) signals for valvular heart disease detection.

Analyze the provided PCG signal data and patient information to diagnose potential valvular heart diseases:
- Aortic Stenosis (AS), Aortic Regurgitation (AR)
- Pulmonary Stenosis (PS), Pulmonary Regurgitation (PR)  
- Tricuspid Stenosis (TS), Tricuspid Regurgitation (TR)
- Mitral Stenosis (MS), Mitral Regurgitation (MR)

Based on the PCG signal from {valve_site} and patient demographics:
Age: {age}, Gender: {gender}, BMI: {bmi}
Clinical Notes: {clinical_notes}

Provide a detailed analysis including:
1. Signal quality assessment
2. Heart sounds identification (S1, S2, murmurs)
3. Specific valve disease diagnosis with confidence level
4. Severity assessment (mild/moderate/severe)
5. Clinical recommendations
6. Follow-up suggestions

Format your response as structured medical report.
"""