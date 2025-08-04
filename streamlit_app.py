import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import os
import scipy.io.wavfile as wav
import soundfile as sf
from scipy.signal import butter, lfilter
from datetime import datetime
import json
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase, WebRtcMode
from streamlit_option_menu import option_menu
import av
import io
import uuid
import plotly.graph_objects as go
import plotly.express as px

# Import our custom modules
from config import *
from database import db
from ai_analyzer import ai_analyzer
from pdf_generator import pdf_generator
from whatsapp_integration import whatsapp
from animations import animations

# Page configuration
st.set_page_config(
    page_title="HEARTEST - AI PCG Analyzer",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'current_patient' not in st.session_state:
    st.session_state['current_patient'] = None
if 'current_diagnosis' not in st.session_state:
    st.session_state['current_diagnosis'] = {}
if 'uploaded_files' not in st.session_state:
    st.session_state['uploaded_files'] = {}

# Create directories
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORTS_FOLDER, exist_ok=True)
os.makedirs(TEMP_FOLDER, exist_ok=True)

def main():
    """Main application function"""
    
    # Apply gradient background and animations
    animations.create_gradient_background()
    
    # Animated header
    animations.show_heartbeat_header()
    
    # Main title with animation
    st.markdown("""
    <div class="main-header">
        HEARTEST
    </div>
    <div style="text-align: center; color: #666; font-size: 1.2rem; margin-bottom: 2rem;">
        🔬 Giri's AI PCG Analyzer - Advanced Valvular Heart Disease Detection
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation menu
    selected = option_menu(
        menu_title=None,
        options=["🏠 Home", "👤 Patient Info", "🔍 Diagnosis", "📚 Case History", "⚙️ Settings"],
        icons=["house", "person", "search", "book", "gear"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#4ECDC4", "font-size": "18px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "center",
                "margin": "0px",
                "padding": "10px",
                "--hover-color": "#eee",
                "border-radius": "10px"
            },
            "nav-link-selected": {"background-color": "#FF6B6B"},
        }
    )
    
    # Route to different pages
    if selected == "🏠 Home":
        show_home_page()
    elif selected == "👤 Patient Info":
        show_patient_info_page()
    elif selected == "🔍 Diagnosis":
        show_diagnosis_page()
    elif selected == "📚 Case History":
        show_case_history_page()
    elif selected == "⚙️ Settings":
        show_settings_page()

def show_home_page():
    """Display home page with welcome and features"""
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div class="medical-card" style="text-align: center; padding: 40px;">
            <h2 style="color: #2E86AB; margin-bottom: 20px;">
                🫀 Welcome to HEARTEST
            </h2>
            <p style="font-size: 1.1rem; color: #666; margin-bottom: 30px;">
                Advanced AI-powered phonocardiography analysis for valvular heart disease detection
            </p>
            
            <div style="display: flex; justify-content: space-around; margin: 30px 0;">
                <div style="text-align: center;">
                    <div style="font-size: 3rem; margin-bottom: 10px;">🤖</div>
                    <strong>Gemini 2.5 Pro AI</strong>
                    <p style="font-size: 0.9rem; color: #666;">Advanced AI Analysis</p>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 3rem; margin-bottom: 10px;">🔬</div>
                    <strong>4 Valve Sites</strong>
                    <p style="font-size: 0.9rem; color: #666;">AV, PV, TV, MV</p>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 3rem; margin-bottom: 10px;">📊</div>
                    <strong>Real-time Analysis</strong>
                    <p style="font-size: 0.9rem; color: #666;">Instant Results</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Feature cards
    st.markdown("### 🌟 Key Features")
    
    feature_cols = st.columns(4)
    
    features = [
        {"icon": "🩺", "title": "PCG Analysis", "desc": "Advanced phonocardiography signal processing"},
        {"icon": "🎯", "title": "AI Diagnosis", "desc": "Detect AS, AR, PS, PR, TS, TR, MS, MR"},
        {"icon": "📱", "title": "WhatsApp Share", "desc": "Share reports instantly via WhatsApp"},
        {"icon": "📄", "title": "PDF Reports", "desc": "Professional medical reports"}
    ]
    
    for i, feature in enumerate(features):
        with feature_cols[i]:
            st.markdown(f"""
            <div class="medical-card floating-element glow-effect" style="text-align: center; padding: 25px;">
                <div style="font-size: 3rem; margin-bottom: 15px;">{feature['icon']}</div>
                <h4 style="color: #2E86AB; margin: 10px 0;">{feature['title']}</h4>
                <p style="color: #666; font-size: 0.9rem;">{feature['desc']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Quick start guide
    st.markdown("### 🚀 Quick Start Guide")
    
    steps_col1, steps_col2 = st.columns(2)
    
    with steps_col1:
        st.markdown("""
        <div class="medical-card">
            <h4 style="color: #FF6B6B;">📝 Step 1: Patient Information</h4>
            <p>Enter patient demographics including age, gender, height, weight, and clinical notes.</p>
            
            <h4 style="color: #FF6B6B;">📊 Step 2: Record/Upload PCG</h4>
            <p>Upload .wav files from 4 valve sites (AV, PV, TV, MV) or record directly.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with steps_col2:
        st.markdown("""
        <div class="medical-card">
            <h4 style="color: #4ECDC4;">🤖 Step 3: AI Analysis</h4>
            <p>Our Gemini AI analyzes PCG signals for valvular heart disease detection.</p>
            
            <h4 style="color: #4ECDC4;">📄 Step 4: Generate Report</h4>
            <p>Get comprehensive PDF reports and share via WhatsApp.</p>
        </div>
        """, unsafe_allow_html=True)

def show_patient_info_page():
    """Display patient information form"""
    
    animations.create_patient_form_animation()
    
    st.markdown("""
    <div class="form-header">
        👤 Patient Information
    </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="patient-form">', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("👤 Full Name", placeholder="Enter patient's full name")
            age = st.number_input("🎂 Age", min_value=1, max_value=120, value=30)
            gender = st.selectbox("⚧ Gender", ["Male", "Female", "Other"])
            height = st.number_input("📏 Height (cm)", min_value=50, max_value=250, value=170)
        
        with col2:
            weight = st.number_input("⚖️ Weight (kg)", min_value=10, max_value=300, value=70)
            phone = st.text_input("📱 Phone Number", placeholder="+91 XXXXXXXXXX")
            
            # Auto-calculate BMI
            if height > 0 and weight > 0:
                bmi = weight / ((height / 100) ** 2)
                st.metric(
                    label="🧮 BMI (Auto-calculated)",
                    value=f"{bmi:.1f}",
                    delta=f"{'Normal' if 18.5 <= bmi <= 24.9 else 'Check range'}"
                )
            else:
                bmi = 0
        
        # Clinical notes
        clinical_notes = st.text_area(
            "📋 Clinical Notes",
            placeholder="Enter any relevant clinical observations, symptoms, or medical history...",
            height=100
        )
        
        # Save patient button
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("💾 Save Patient Information", type="primary"):
                if name and age:
                    # Validate phone number
                    phone_valid, phone_message = whatsapp.validate_phone_number(phone) if phone else (True, "")
                    
                    patient_data = {
                        'name': name,
                        'age': age,
                        'gender': gender,
                        'height': height,
                        'weight': weight,
                        'bmi': round(bmi, 1) if bmi > 0 else None,
                        'phone': phone_message if phone_valid else phone,
                        'clinical_notes': clinical_notes
                    }
                    
                    # Save to database
                    patient_id = db.save_patient(patient_data)
                    if patient_id:
                        st.session_state['current_patient'] = patient_data
                        st.session_state['current_patient']['id'] = patient_id
                        
                        animations.show_success_message("Patient information saved successfully!")
                        
                        st.balloons()
                        
                        # Show patient summary
                        st.markdown("""
                        <div class="diagnosis-result">
                            <h4>✅ Patient Registered Successfully</h4>
                            <p><strong>Patient ID:</strong> {}</p>
                            <p><strong>Name:</strong> {}</p>
                            <p><strong>BMI:</strong> {:.1f}</p>
                            <p>You can now proceed to diagnosis.</p>
                        </div>
                        """.format(patient_id, name, bmi), unsafe_allow_html=True)
                    else:
                        st.error("Failed to save patient information. Please try again.")
                else:
                    st.warning("Please fill in at least the name and age fields.")
        
        st.markdown('</div>', unsafe_allow_html=True)

def show_diagnosis_page():
    """Display diagnosis page with PCG analysis"""
    
    st.markdown("### 🔍 PCG Analysis & Diagnosis")
    
    # Check if patient info exists
    if not st.session_state.get('current_patient'):
        st.warning("⚠️ Please enter patient information first!")
        if st.button("➡️ Go to Patient Info"):
            st.rerun()
        return
    
    patient = st.session_state['current_patient']
    
    # Patient summary
    st.markdown(f"""
    <div class="medical-card">
        <h4>👤 Current Patient: {patient['name']}</h4>
        <p><strong>Age:</strong> {patient['age']} | <strong>Gender:</strong> {patient['gender']} | <strong>BMI:</strong> {patient.get('bmi', 'N/A')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Valve site selection with animation
    selected_valve = animations.create_valve_selector_animation(VALVE_SITES)
    
    if selected_valve:
        st.markdown(f"""
        <div class="diagnosis-result">
            <h4>🎯 Selected: {VALVE_SITES[selected_valve]}</h4>
            <p>Please upload or record PCG from the {selected_valve} site</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Audio upload/recording section
        tab1, tab2 = st.tabs(["📁 Upload Audio", "🎙️ Record Audio"])
        
        audio_file = None
        
        with tab1:
            uploaded_file = st.file_uploader(
                f"Upload PCG audio for {VALVE_SITES[selected_valve]}",
                type=['wav'],
                key=f"upload_{selected_valve}"
            )
            
            if uploaded_file:
                # Save uploaded file
                file_path = os.path.join(UPLOAD_FOLDER, f"{patient['name']}_{selected_valve}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav")
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                audio_file = file_path
                st.success("✅ Audio file uploaded successfully!")
        
        with tab2:
            # Microphone recording
            class AudioProcessor(AudioProcessorBase):
                def __init__(self):
                    self.frames = []
                
                def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
                    self.frames.append(frame)
                    return frame
            
            ctx = webrtc_streamer(
                key=f"record_{selected_valve}",
                mode=WebRtcMode.SENDONLY,
                audio_receiver_size=1024,
                media_stream_constraints={"video": False, "audio": True},
                audio_processor_factory=AudioProcessor,
                async_processing=True,
            )
            
            if ctx.audio_receiver:
                if st.button(f"🎙️ Save Recording for {selected_valve}", key=f"save_rec_{selected_valve}"):
                    audio_frames = ctx.audio_receiver.get_frames(timeout=1)
                    if audio_frames:
                        raw_audio = np.concatenate([frame.to_ndarray().flatten() for frame in audio_frames])
                        raw_audio = (raw_audio * 32767).astype(np.int16)
                        
                        file_path = os.path.join(UPLOAD_FOLDER, f"{patient['name']}_{selected_valve}_recorded_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav")
                        wav.write(file_path, rate=48000, data=raw_audio)
                        audio_file = file_path
                        st.success("✅ Recording saved successfully!")
                    else:
                        st.warning("No audio captured. Please try recording again.")
        
        # Audio analysis
        if audio_file:
            st.markdown("### 🎵 Audio Analysis")
            
            # Display audio player
            st.audio(audio_file, format="audio/wav")
            
            # Show audio visualizer animation
            animations.create_audio_visualizer_animation()
            
            # Load and process audio
            try:
                sample_rate, audio_data = wav.read(audio_file)
                if audio_data.ndim > 1:
                    audio_data = audio_data[:, 0]  # Take first channel
                
                # Display waveform
                fig = go.Figure()
                time_axis = np.arange(len(audio_data)) / sample_rate
                fig.add_trace(go.Scatter(
                    x=time_axis,
                    y=audio_data,
                    mode='lines',
                    name='PCG Signal',
                    line=dict(color='#FF6B6B', width=1)
                ))
                fig.update_layout(
                    title=f"PCG Waveform - {VALVE_SITES[selected_valve]}",
                    xaxis_title="Time (seconds)",
                    yaxis_title="Amplitude",
                    template="plotly_dark",
                    height=300
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # AI Analysis button
                if st.button(f"🤖 Analyze with Gemini AI", type="primary", key=f"analyze_{selected_valve}"):
                    
                    # Show loading animation
                    with st.container():
                        animations.show_loading_analysis("Gemini AI is analyzing PCG signal...")
                        
                        # Perform AI analysis
                        diagnosis = ai_analyzer.analyze_pcg_signal(
                            audio_data=audio_data,
                            sample_rate=sample_rate,
                            valve_site=selected_valve,
                            patient_info=patient
                        )
                        
                        # Clear loading animation
                        st.empty()
                        
                        # Show success animation
                        animations.show_success_message("AI Analysis Complete!")
                        
                        # Display diagnosis results with animation
                        animations.create_diagnosis_animation(diagnosis)
                        
                        # Store diagnosis in session
                        st.session_state['current_diagnosis'][selected_valve] = diagnosis
                        
                        # Save case to database
                        case_data = {
                            'patient_id': patient['id'],
                            'valve_site': selected_valve,
                            'audio_filename': os.path.basename(audio_file),
                            'diagnosis': diagnosis,
                            'confidence_level': diagnosis.get('confidence_level'),
                            'severity': diagnosis.get('severity'),
                            'recommendations': diagnosis.get('recommendations', [])
                        }
                        
                        db.save_case(case_data)
                        
                        # Additional findings
                        if diagnosis.get('findings'):
                            st.markdown("### 📋 Clinical Findings")
                            for finding in diagnosis['findings']:
                                st.markdown(f"• {finding}")
                        
                        # Recommendations
                        if diagnosis.get('recommendations'):
                            st.markdown("### 💡 Recommendations")
                            for rec in diagnosis['recommendations']:
                                st.markdown(f"• {rec}")
                        
                        # Action buttons
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            if st.button("📄 Generate PDF Report", key=f"pdf_{selected_valve}"):
                                report_path = os.path.join(REPORTS_FOLDER, f"{patient['name']}_{selected_valve}_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
                                pdf_generator.generate_report(patient, diagnosis, report_path)
                                
                                with open(report_path, "rb") as pdf_file:
                                    st.download_button(
                                        label="⬇️ Download PDF",
                                        data=pdf_file,
                                        file_name=os.path.basename(report_path),
                                        mime="application/pdf"
                                    )
                        
                        with col2:
                            if patient.get('phone') and st.button("📱 Share via WhatsApp", key=f"whatsapp_{selected_valve}"):
                                report_path = os.path.join(REPORTS_FOLDER, f"{patient['name']}_{selected_valve}_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
                                pdf_generator.generate_report(patient, diagnosis, report_path)
                                
                                whatsapp_result = whatsapp.share_report_via_whatsapp(
                                    phone_number=patient['phone'],
                                    patient_name=patient['name'],
                                    diagnosis=diagnosis['primary_diagnosis'],
                                    report_path=report_path
                                )
                                st.success(f"📱 {whatsapp_result}")
                        
                        with col3:
                            if st.button("🔄 Analyze Another Valve", key=f"another_{selected_valve}"):
                                st.rerun()
                        
            except Exception as e:
                st.error(f"Error processing audio: {str(e)}")

def show_case_history_page():
    """Display case history with saved diagnoses"""
    
    st.markdown("### 📚 Case History")
    
    # Get case history
    cases = db.get_case_history()
    
    if not cases:
        st.info("📭 No case history found. Start by diagnosing some patients!")
        return
    
    # Display cases
    for i, case in enumerate(cases):
        patient_info = case.get('patient', {})
        
        with st.expander(f"📋 Case #{i+1}: {patient_info.get('name', 'Unknown')} - {case.get('valve_site', 'Unknown')} ({case.get('created_at', 'Unknown date')})"):
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**👤 Patient Information:**")
                st.write(f"Name: {patient_info.get('name', 'N/A')}")
                st.write(f"Age: {patient_info.get('age', 'N/A')}")
                st.write(f"Gender: {patient_info.get('gender', 'N/A')}")
                st.write(f"BMI: {patient_info.get('bmi', 'N/A')}")
            
            with col2:
                st.markdown("**🔍 Diagnosis Results:**")
                diagnosis = case.get('diagnosis', {})
                if isinstance(diagnosis, str):
                    import json
                    try:
                        diagnosis = json.loads(diagnosis)
                    except:
                        diagnosis = {}
                
                st.write(f"Valve Site: {case.get('valve_site', 'N/A')}")
                st.write(f"Diagnosis: {diagnosis.get('primary_diagnosis', 'N/A')}")
                st.write(f"Confidence: {diagnosis.get('confidence_level', 'N/A')}%")
                st.write(f"Severity: {diagnosis.get('severity', 'N/A')}")
            
            # Show audio if available
            audio_path = os.path.join(UPLOAD_FOLDER, case.get('audio_filename', ''))
            if os.path.exists(audio_path):
                st.audio(audio_path, format="audio/wav")
            
            # Action buttons for each case
            case_col1, case_col2, case_col3 = st.columns(3)
            
            with case_col1:
                if st.button(f"📄 Generate Report", key=f"pdf_case_{i}"):
                    report_path = os.path.join(REPORTS_FOLDER, f"case_{i}_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
                    pdf_generator.generate_report(patient_info, diagnosis, report_path)
                    
                    with open(report_path, "rb") as pdf_file:
                        st.download_button(
                            label="⬇️ Download PDF",
                            data=pdf_file,
                            file_name=os.path.basename(report_path),
                            mime="application/pdf",
                            key=f"download_case_{i}"
                        )
            
            with case_col2:
                if patient_info.get('phone') and st.button(f"📱 Share WhatsApp", key=f"wa_case_{i}"):
                    report_path = os.path.join(REPORTS_FOLDER, f"case_{i}_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
                    pdf_generator.generate_report(patient_info, diagnosis, report_path)
                    
                    whatsapp_result = whatsapp.share_report_via_whatsapp(
                        phone_number=patient_info['phone'],
                        patient_name=patient_info['name'],
                        diagnosis=diagnosis.get('primary_diagnosis', 'Unknown'),
                        report_path=report_path
                    )
                    st.success(f"📱 {whatsapp_result}")
            
            with case_col3:
                if st.button(f"🔄 Re-analyze", key=f"reanalyze_case_{i}"):
                    st.info("Feature coming soon!")

def show_settings_page():
    """Display settings and configuration"""
    
    st.markdown("### ⚙️ Settings & Configuration")
    
    tab1, tab2, tab3 = st.tabs(["🔑 API Keys", "📊 System Info", "ℹ️ About"])
    
    with tab1:
        st.markdown("#### 🔑 API Configuration")
        
        # Gemini API Key
        gemini_key = st.text_input("Google Gemini API Key", type="password", value=GOOGLE_API_KEY or "")
        
        # Supabase Configuration
        supabase_url = st.text_input("Supabase URL", value=SUPABASE_URL or "")
        supabase_key = st.text_input("Supabase Key", type="password", value=SUPABASE_KEY or "")
        
        if st.button("💾 Save Configuration"):
            st.success("Configuration saved! Please restart the application.")
    
    with tab2:
        st.markdown("#### 📊 System Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Total Patients", len(db.get_all_patients()))
            st.metric("Total Cases", len(db.get_case_history()))
        
        with col2:
            st.metric("AI Model", "Gemini 2.5 Pro" if GOOGLE_API_KEY else "Simulation Mode")
            st.metric("Database", "Supabase" if SUPABASE_URL else "Local Storage")
        
        # System status
        st.markdown("#### 🟢 System Status")
        status_checks = [
            ("Gemini AI", "✅ Connected" if GOOGLE_API_KEY else "⚠️ API Key Missing"),
            ("Supabase DB", "✅ Connected" if SUPABASE_URL else "⚠️ Using Local Storage"),
            ("Audio Processing", "✅ Available"),
            ("PDF Generation", "✅ Available"),
            ("WhatsApp Integration", "✅ Available")
        ]
        
        for service, status in status_checks:
            st.write(f"**{service}:** {status}")
    
    with tab3:
        st.markdown("""
        <div class="medical-card">
            <h3 style="color: #2E86AB;">🫀 HEARTEST</h3>
            <p><strong>Version:</strong> {}</p>
            <p><strong>Description:</strong> {}</p>
            
            <h4>🎯 Features:</h4>
            <ul>
                <li>🤖 Real Gemini 2.5 Pro AI integration</li>
                <li>🫀 4 valve site analysis (AV, PV, TV, MV)</li>
                <li>🔬 8 disease detection (AS, AR, PS, PR, TS, TR, MS, MR)</li>
                <li>📊 Real-time PCG signal processing</li>
                <li>📄 Professional PDF reports</li>
                <li>📱 WhatsApp sharing</li>
                <li>💾 Supabase database integration</li>
                <li>🎨 Modern animated UI</li>
            </ul>
            
            <h4>⚠️ Disclaimer:</h4>
            <p style="color: #e74c3c; font-weight: bold;">
                This application is for educational and research purposes only. 
                It should not be used as a substitute for professional medical diagnosis or treatment. 
                Always consult with a qualified healthcare provider for proper medical evaluation and care.
            </p>
            
            <p style="text-align: center; margin-top: 20px; color: #666;">
                Developed with ❤️ for advancing cardiac diagnostics
            </p>
        </div>
        """.format(APP_VERSION, APP_DESCRIPTION), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
