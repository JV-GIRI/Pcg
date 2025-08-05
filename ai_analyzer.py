import google.generativeai as genai
import numpy as np
import librosa
import matplotlib.pyplot as plt
import io
import base64
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import json

from config import GOOGLE_API_KEY, GEMINI_PCG_ANALYSIS_PROMPT, VALVE_SITES, VALVE_DISEASES

class GeminiPCGAnalyzer:
    def __init__(self):
        if GOOGLE_API_KEY:
            genai.configure(api_key=GOOGLE_API_KEY)
            self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        else:
            self.model = None
            print("Warning: Google API key not found. AI analysis will be simulated.")
    
    def extract_pcg_features(self, audio_data: np.ndarray, sample_rate: int) -> Dict:
        """Extract relevant features from PCG signal for AI analysis"""
        
        # Basic signal statistics
        duration = len(audio_data) / sample_rate
        rms_energy = np.sqrt(np.mean(audio_data**2))
        zero_crossing_rate = np.mean(librosa.feature.zero_crossing_rate(audio_data))
        
        # Spectral features
        stft = librosa.stft(audio_data)
        spectral_centroids = librosa.feature.spectral_centroid(S=np.abs(stft))[0]
        spectral_rolloff = librosa.feature.spectral_rolloff(S=np.abs(stft))[0]
        
        # Heart rate estimation (rough approximation)
        # Find dominant frequency in the low frequency range (30-200 Hz)
        freqs = np.fft.fftfreq(len(audio_data), 1/sample_rate)
        fft = np.abs(np.fft.fft(audio_data))
        
        # Focus on heart sound frequency range
        heart_freq_mask = (freqs >= 30) & (freqs <= 200)
        if np.any(heart_freq_mask):
            dominant_freq = freqs[heart_freq_mask][np.argmax(fft[heart_freq_mask])]
            estimated_heart_rate = dominant_freq * 60  # Convert to BPM
        else:
            estimated_heart_rate = 70  # Default
        
        # Frequency domain analysis
        low_freq_energy = np.sum(fft[(freqs >= 20) & (freqs <= 100)])
        mid_freq_energy = np.sum(fft[(freqs >= 100) & (freqs <= 300)])
        high_freq_energy = np.sum(fft[(freqs >= 300) & (freqs <= 1000)])
        
        return {
            'duration': duration,
            'rms_energy': float(rms_energy),
            'zero_crossing_rate': float(np.mean(zero_crossing_rate)),
            'spectral_centroid_mean': float(np.mean(spectral_centroids)),
            'spectral_rolloff_mean': float(np.mean(spectral_rolloff)),
            'estimated_heart_rate': float(estimated_heart_rate),
            'low_freq_energy': float(low_freq_energy),
            'mid_freq_energy': float(mid_freq_energy),
            'high_freq_energy': float(high_freq_energy),
            'sample_rate': sample_rate,
            'signal_length': len(audio_data)
        }
    
    def create_spectrogram_image(self, audio_data: np.ndarray, sample_rate: int) -> str:
        """Create spectrogram image for AI analysis"""
        
        plt.figure(figsize=(12, 8))
        
        # Create spectrogram
        D = librosa.amplitude_to_db(np.abs(librosa.stft(audio_data)), ref=np.max)
        librosa.display.specshow(D, sr=sample_rate, x_axis='time', y_axis='hz')
        plt.colorbar(format='%+2.0f dB')
        plt.title('PCG Spectrogram')
        plt.xlabel('Time (s)')
        plt.ylabel('Frequency (Hz)')
        
        # Save to bytes
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
        buf.seek(0)
        plt.close()
        
        # Encode to base64
        image_base64 = base64.b64encode(buf.getvalue()).decode()
        buf.close()
        
        return image_base64
    
    def analyze_pcg_signal(self, 
                          audio_data: np.ndarray, 
                          sample_rate: int,
                          valve_site: str,
                          patient_info: Dict) -> Dict:
        """Perform complete PCG analysis using Gemini AI"""
        
        # Extract features
        features = self.extract_pcg_features(audio_data, sample_rate)
        
        # Create spectrogram
        spectrogram_b64 = self.create_spectrogram_image(audio_data, sample_rate)
        
        if self.model:
            return self._analyze_with_gemini(features, spectrogram_b64, valve_site, patient_info)
        else:
            return self._simulate_analysis(features, valve_site, patient_info)
    
    def _analyze_with_gemini(self, 
                           features: Dict, 
                           spectrogram_b64: str,
                           valve_site: str, 
                           patient_info: Dict) -> Dict:
        """Analyze PCG using Gemini AI"""
        
        try:
            # Prepare the prompt
            prompt = GEMINI_PCG_ANALYSIS_PROMPT.format(
                valve_site=VALVE_SITES.get(valve_site, valve_site),
                age=patient_info.get('age', 'Unknown'),
                gender=patient_info.get('gender', 'Unknown'),
                bmi=patient_info.get('bmi', 'Unknown'),
                clinical_notes=patient_info.get('clinical_notes', 'None provided')
            )
            
            # Add technical data
            technical_data = f"""
            
            Technical PCG Signal Analysis Data:
            
            Signal Duration: {features['duration']:.2f} seconds
            Estimated Heart Rate: {features['estimated_heart_rate']:.1f} BPM
            RMS Energy: {features['rms_energy']:.6f}
            Spectral Centroid: {features['spectral_centroid_mean']:.2f} Hz
            Zero Crossing Rate: {features['zero_crossing_rate']:.6f}
            
            Frequency Domain Analysis:
            - Low Frequency Energy (20-100 Hz): {features['low_freq_energy']:.2e}
            - Mid Frequency Energy (100-300 Hz): {features['mid_freq_energy']:.2e}  
            - High Frequency Energy (300-1000 Hz): {features['high_freq_energy']:.2e}
            
            Valve Site: {valve_site} ({VALVE_SITES.get(valve_site, valve_site)})
            
            Please analyze this PCG signal and provide your expert diagnosis.
            """
            
            full_prompt = prompt + technical_data
            
            # Send to Gemini
            response = self.model.generate_content([
                full_prompt,
                {
                    "mime_type": "image/png",
                    "data": spectrogram_b64
                }
            ])
            
            # Parse response
            diagnosis = self._parse_gemini_response(response.text, valve_site)
            diagnosis['raw_response'] = response.text
            diagnosis['analysis_timestamp'] = datetime.now().isoformat()
            
            return diagnosis
            
        except Exception as e:
            print(f"Error in Gemini analysis: {e}")
            return self._simulate_analysis(features, valve_site, patient_info)
    
    def _parse_gemini_response(self, response_text: str, valve_site: str) -> Dict:
        """Parse Gemini response into structured diagnosis"""
        
        # Basic parsing - in a real implementation, you'd use more sophisticated NLP
        diagnosis = {
            'valve_site': valve_site,
            'valve_name': VALVE_SITES.get(valve_site, valve_site),
            'primary_diagnosis': 'Normal',
            'confidence_level': 85,
            'severity': 'None',
            'findings': [],
            'recommendations': [],
            'follow_up': 'Routine follow-up in 1 year'
        }
        
        # Look for disease indicators in response
        response_lower = response_text.lower()
        
        for disease_code, disease_name in VALVE_DISEASES.items():
            if disease_name.lower() in response_lower or disease_code.lower() in response_lower:
                diagnosis['primary_diagnosis'] = disease_name
                diagnosis['diagnosis_code'] = disease_code
                break
        
        # Extract confidence level
        if 'confidence' in response_lower:
            import re
            confidence_match = re.search(r'confidence[:\s]*(\d+)%?', response_lower)
            if confidence_match:
                diagnosis['confidence_level'] = int(confidence_match.group(1))
        
        # Extract severity
        if 'severe' in response_lower:
            diagnosis['severity'] = 'Severe'
        elif 'moderate' in response_lower:
            diagnosis['severity'] = 'Moderate'
        elif 'mild' in response_lower:
            diagnosis['severity'] = 'Mild'
        
        # Extract key findings
        lines = response_text.split('\n')
        for line in lines:
            line = line.strip()
            if line and any(keyword in line.lower() for keyword in ['murmur', 'sound', 'finding', 'abnormal']):
                diagnosis['findings'].append(line)
        
        return diagnosis
    
    def _simulate_analysis(self, features: Dict, valve_site: str, patient_info: Dict) -> Dict:
        """Simulate AI analysis when Gemini is not available"""
        
        # Simple rule-based simulation
        heart_rate = features['estimated_heart_rate']
        energy = features['rms_energy']
        
        diagnosis = {
            'valve_site': valve_site,
            'valve_name': VALVE_SITES.get(valve_site, valve_site),
            'primary_diagnosis': 'Normal',
            'confidence_level': 75,
            'severity': 'None',
            'findings': [
                f"Heart rate: {heart_rate:.1f} BPM",
                f"Signal quality: {'Good' if energy > 0.01 else 'Fair'}",
                "Automated analysis (Gemini AI not available)"
            ],
            'recommendations': [
                "Clinical correlation recommended",
                "Consider manual review by cardiologist"
            ],
            'follow_up': 'Routine follow-up in 6 months',
            'analysis_timestamp': datetime.now().isoformat(),
            'simulation_mode': True
        }
        
        # Simple heuristics for demonstration
        if heart_rate > 100:
            diagnosis['findings'].append("Tachycardia detected")
        elif heart_rate < 60:
            diagnosis['findings'].append("Bradycardia detected")
            
        if energy < 0.005:
            diagnosis['findings'].append("Low signal amplitude - consider re-recording")
        
        return diagnosis

# Global AI analyzer instance
ai_analyzer = GeminiPCGAnalyzer()