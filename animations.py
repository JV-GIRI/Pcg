import streamlit as st
import time
import json
from streamlit_lottie import st_lottie
import requests
from typing import Optional, Dict, Any
import base64

class HeartestAnimations:
    def __init__(self):
        self.animation_cache = {}
    
    def load_lottie_url(self, url: str) -> Optional[Dict[Any, Any]]:
        """Load Lottie animation from URL"""
        try:
            r = requests.get(url)
            if r.status_code != 200:
                return None
            return r.json()
        except:
            return None
    
    def load_lottie_file(self, filepath: str) -> Optional[Dict[Any, Any]]:
        """Load Lottie animation from local file"""
        try:
            with open(filepath, "r") as f:
                return json.load(f)
        except:
            return None
    
    def get_heartbeat_animation(self) -> Optional[Dict[Any, Any]]:
        """Get heartbeat animation"""
        if "heartbeat" not in self.animation_cache:
            # Lottie heartbeat animation URL
            url = "https://assets5.lottiefiles.com/packages/lf20_a2eq6rfp.json"
            self.animation_cache["heartbeat"] = self.load_lottie_url(url)
        return self.animation_cache["heartbeat"]
    
    def get_medical_loading_animation(self) -> Optional[Dict[Any, Any]]:
        """Get medical loading animation"""
        if "medical_loading" not in self.animation_cache:
            # Medical loading animation URL
            url = "https://assets2.lottiefiles.com/packages/lf20_5njp3vgg.json"
            self.animation_cache["medical_loading"] = self.load_lottie_url(url)
        return self.animation_cache["medical_loading"]
    
    def get_stethoscope_animation(self) -> Optional[Dict[Any, Any]]:
        """Get stethoscope animation"""
        if "stethoscope" not in self.animation_cache:
            # Stethoscope animation URL
            url = "https://assets1.lottiefiles.com/packages/lf20_x1ytkhje.json"
            self.animation_cache["stethoscope"] = self.load_lottie_url(url)
        return self.animation_cache["stethoscope"]
    
    def get_ai_brain_animation(self) -> Optional[Dict[Any, Any]]:
        """Get AI brain animation"""
        if "ai_brain" not in self.animation_cache:
            # AI brain animation URL
            url = "https://assets9.lottiefiles.com/packages/lf20_w51pcehl.json"
            self.animation_cache["ai_brain"] = self.load_lottie_url(url)
        return self.animation_cache["ai_brain"]
    
    def get_success_animation(self) -> Optional[Dict[Any, Any]]:
        """Get success checkmark animation"""
        if "success" not in self.animation_cache:
            # Success animation URL
            url = "https://assets4.lottiefiles.com/private_files/lf30_t26law.json"
            self.animation_cache["success"] = self.load_lottie_url(url)
        return self.animation_cache["success"]
    
    def show_heartbeat_header(self):
        """Display animated heartbeat header"""
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            heartbeat_anim = self.get_heartbeat_animation()
            if heartbeat_anim:
                st_lottie(heartbeat_anim, height=150, key="header_heartbeat")
            else:
                st.markdown("### 💓 HEARTEST 💓", unsafe_allow_html=True)
    
    def show_loading_analysis(self, message: str = "Analyzing PCG Signal..."):
        """Show loading animation during AI analysis"""
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            medical_loading = self.get_medical_loading_animation()
            if medical_loading:
                st_lottie(medical_loading, height=200, key="analysis_loading")
            else:
                st.spinner(message)
            
            st.markdown(f"<h4 style='text-align: center; color: #1f77b4;'>{message}</h4>", 
                       unsafe_allow_html=True)
    
    def show_ai_thinking(self):
        """Show AI brain thinking animation"""
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col2:
            ai_brain = self.get_ai_brain_animation()
            if ai_brain:
                st_lottie(ai_brain, height=150, key="ai_thinking")
            else:
                st.markdown("🧠 AI Processing...")
    
    def show_success_message(self, message: str = "Analysis Complete!"):
        """Show success animation with message"""
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col2:
            success_anim = self.get_success_animation()
            if success_anim:
                st_lottie(success_anim, height=100, key="success_anim")
            else:
                st.success("✅ " + message)
    
    def create_animated_progress_bar(self, progress: float, text: str = "Processing..."):
        """Create animated progress bar"""
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i in range(int(progress * 100)):
            progress_bar.progress(i / 100)
            status_text.text(f'{text} {i + 1}%')
            time.sleep(0.01)
        
        return progress_bar, status_text
    
    def create_pulse_effect(self, element_id: str):
        """Create CSS pulse effect"""
        pulse_css = f"""
        <style>
        @keyframes pulse-{element_id} {{
            0% {{ transform: scale(1); }}
            50% {{ transform: scale(1.05); }}
            100% {{ transform: scale(1); }}
        }}
        
        .pulse-{element_id} {{
            animation: pulse-{element_id} 2s infinite;
        }}
        </style>
        """
        st.markdown(pulse_css, unsafe_allow_html=True)
    
    def create_gradient_background(self):
        """Create medical gradient background"""
        gradient_css = """
        <style>
        .stApp {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        
        .main-header {
            background: linear-gradient(90deg, #4CAF50, #2196F3);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 3rem;
            font-weight: bold;
            text-align: center;
            margin-bottom: 2rem;
        }
        
        .medical-card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            border: 1px solid rgba(255, 255, 255, 0.18);
            margin: 10px 0;
        }
        
        .heartbeat-icon {
            color: #e74c3c;
            animation: heartbeat 1.5s ease-in-out infinite both;
        }
        
        @keyframes heartbeat {
            from {
                transform: scale(1);
                transform-origin: center center;
                animation-timing-function: ease-out;
            }
            10% {
                transform: scale(0.91);
                animation-timing-function: ease-in;
            }
            17% {
                transform: scale(0.98);
                animation-timing-function: ease-out;
            }
            33% {
                transform: scale(0.87);
                animation-timing-function: ease-in;
            }
            45% {
                transform: scale(1);
                animation-timing-function: ease-out;
            }
        }
        
        .valve-button {
            background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
            border: none;
            border-radius: 50px;
            color: white;
            padding: 15px 30px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            transition: all 0.3s;
            box-shadow: 0 4px 15px 0 rgba(31, 38, 135, 0.2);
        }
        
        .valve-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px 0 rgba(31, 38, 135, 0.4);
        }
        
        .diagnosis-result {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 15px;
            margin: 15px 0;
            animation: slideInUp 0.5s ease-out;
        }
        
        @keyframes slideInUp {
            from {
                transform: translateY(30px);
                opacity: 0;
            }
            to {
                transform: translateY(0);
                opacity: 1;
            }
        }
        
        .floating-element {
            animation: floating 3s ease-in-out infinite;
        }
        
        @keyframes floating {
            0% { transform: translate(0, 0px); }
            50% { transform: translate(0, -10px); }
            100% { transform: translate(0, 0px); }
        }
        
        .glow-effect {
            box-shadow: 0 0 20px rgba(76, 175, 80, 0.5);
            transition: all 0.3s ease;
        }
        
        .glow-effect:hover {
            box-shadow: 0 0 30px rgba(76, 175, 80, 0.8);
        }
        </style>
        """
        st.markdown(gradient_css, unsafe_allow_html=True)
    
    def create_valve_selector_animation(self, valve_sites: Dict[str, str]):
        """Create animated valve selector"""
        st.markdown("""
        <div style='text-align: center; margin: 20px 0;'>
            <h3 style='color: #2E86AB; margin-bottom: 20px;'>🫀 Select Valve Site for Analysis</h3>
        </div>
        """, unsafe_allow_html=True)
        
        cols = st.columns(4)
        selected_valve = None
        
        valve_icons = {
            "AV": "🔴",  # Aortic - Red
            "PV": "🟠",  # Pulmonary - Orange  
            "TV": "🟡",  # Tricuspid - Yellow
            "MV": "🟢"   # Mitral - Green
        }
        
        for i, (code, name) in enumerate(valve_sites.items()):
            with cols[i]:
                icon = valve_icons.get(code, "🔵")
                
                button_html = f"""
                <div class="floating-element" style="text-align: center; margin: 10px;">
                    <div class="medical-card glow-effect" style="cursor: pointer; transition: all 0.3s;">
                        <div style="font-size: 3rem; margin-bottom: 10px;">{icon}</div>
                        <h4 style="color: #2E86AB; margin: 5px 0;">{code}</h4>
                        <p style="color: #666; font-size: 12px; margin: 0;">{name}</p>
                    </div>
                </div>
                """
                st.markdown(button_html, unsafe_allow_html=True)
                
                if st.button(f"Select {code}", key=f"valve_{code}", help=f"Analyze {name}"):
                    selected_valve = code
        
        return selected_valve
    
    def create_patient_form_animation(self):
        """Create animated patient form"""
        form_css = """
        <style>
        .patient-form {
            background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
            backdrop-filter: blur(10px);
            padding: 30px;
            border-radius: 20px;
            border: 1px solid rgba(255,255,255,0.2);
            animation: slideInLeft 0.8s ease-out;
        }
        
        @keyframes slideInLeft {
            from {
                transform: translateX(-50px);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        
        .form-header {
            background: linear-gradient(90deg, #FF6B6B, #4ECDC4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 2rem;
            font-weight: bold;
            text-align: center;
            margin-bottom: 20px;
        }
        </style>
        """
        st.markdown(form_css, unsafe_allow_html=True)
    
    def create_diagnosis_animation(self, diagnosis_data: Dict):
        """Create animated diagnosis display"""
        diagnosis_css = """
        <style>
        .diagnosis-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 20px;
            margin: 20px 0;
            animation: zoomIn 0.6s ease-out;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        
        @keyframes zoomIn {
            from {
                transform: scale(0.8);
                opacity: 0;
            }
            to {
                transform: scale(1);
                opacity: 1;
            }
        }
        
        .confidence-bar {
            background: rgba(255,255,255,0.2);
            border-radius: 10px;
            overflow: hidden;
            margin: 10px 0;
        }
        
        .confidence-fill {
            background: linear-gradient(90deg, #4CAF50, #8BC34A);
            height: 20px;
            border-radius: 10px;
            animation: fillBar 2s ease-out;
        }
        
        @keyframes fillBar {
            from { width: 0%; }
            to { width: var(--confidence-width); }
        }
        </style>
        """
        st.markdown(diagnosis_css, unsafe_allow_html=True)
        
        confidence = diagnosis_data.get('confidence_level', 0)
        
        diagnosis_html = f"""
        <div class="diagnosis-card">
            <h2 style="margin-top: 0;">🎯 Diagnosis Results</h2>
            <div style="display: flex; align-items: center; margin: 15px 0;">
                <span style="font-size: 2rem; margin-right: 15px;">🫀</span>
                <div>
                    <h3 style="margin: 0; color: #FFE4E1;">{diagnosis_data.get('valve_name', 'Unknown')}</h3>
                    <p style="margin: 5px 0; font-size: 1.2rem; font-weight: bold;">{diagnosis_data.get('primary_diagnosis', 'No diagnosis')}</p>
                </div>
            </div>
            
            <div style="margin: 20px 0;">
                <p style="margin: 5px 0;"><strong>Confidence Level:</strong></p>
                <div class="confidence-bar">
                    <div class="confidence-fill" style="--confidence-width: {confidence}%; width: {confidence}%;"></div>
                </div>
                <p style="text-align: center; margin: 5px 0; font-weight: bold;">{confidence}%</p>
            </div>
            
            <div style="margin: 15px 0;">
                <p><strong>Severity:</strong> {diagnosis_data.get('severity', 'Not specified')}</p>
            </div>
        </div>
        """
        
        st.markdown(diagnosis_html, unsafe_allow_html=True)
    
    def create_audio_visualizer_animation(self):
        """Create audio visualizer animation"""
        visualizer_css = """
        <style>
        .audio-visualizer {
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100px;
            margin: 20px 0;
        }
        
        .bar {
            width: 4px;
            margin: 0 2px;
            background: linear-gradient(to top, #FF6B6B, #4ECDC4);
            border-radius: 2px;
            animation: audioWave 1.5s ease-in-out infinite;
        }
        
        .bar:nth-child(2) { animation-delay: 0.1s; }
        .bar:nth-child(3) { animation-delay: 0.2s; }
        .bar:nth-child(4) { animation-delay: 0.3s; }
        .bar:nth-child(5) { animation-delay: 0.4s; }
        .bar:nth-child(6) { animation-delay: 0.5s; }
        .bar:nth-child(7) { animation-delay: 0.4s; }
        .bar:nth-child(8) { animation-delay: 0.3s; }
        .bar:nth-child(9) { animation-delay: 0.2s; }
        .bar:nth-child(10) { animation-delay: 0.1s; }
        
        @keyframes audioWave {
            0%, 100% { height: 20px; }
            50% { height: 80px; }
        }
        </style>
        """
        st.markdown(visualizer_css, unsafe_allow_html=True)
        
        visualizer_html = """
        <div class="audio-visualizer">
            <div class="bar"></div>
            <div class="bar"></div>
            <div class="bar"></div>
            <div class="bar"></div>
            <div class="bar"></div>
            <div class="bar"></div>
            <div class="bar"></div>
            <div class="bar"></div>
            <div class="bar"></div>
            <div class="bar"></div>
        </div>
        """
        st.markdown(visualizer_html, unsafe_allow_html=True)

# Global animations instance
animations = HeartestAnimations()