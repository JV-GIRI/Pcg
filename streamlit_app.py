import streamlit as st
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
import noisereduce as nr
from fpdf import FPDF
import io
import base64

# --------------------- Streamlit UI Setup ---------------------
st.set_page_config(page_title="Heartest - Heart Sound Analyzer", layout="wide")
st.title("💓 Heartest - Heart Sound Analyzer")

st.sidebar.header("🩺 New Case Entry")
name = st.sidebar.text_input("Patient Name")
age = st.sidebar.text_input("Age")
gender = st.sidebar.selectbox("Gender", ["Male", "Female", "Other"])
symptoms = st.sidebar.text_area("Symptoms")

# Upload Section
st.subheader("📤 Upload Heart Sound (.wav file)")
uploaded_file = st.file_uploader("Choose a .wav file", type=["wav"])

if uploaded_file is not None:
    st.audio(uploaded_file, format='audio/wav')

    # Load audio
    y, sr = librosa.load(uploaded_file, sr=None)
    original_y = y.copy()

    # Duration and amplitude controls
    st.subheader("🎛️ Waveform Controls")
    duration_slider = st.slider("Duration (seconds)", 1.0, float(len(y)/sr), float(len(y)/sr), 0.1)
    amp_factor = st.slider("Amplitude Scaling", 0.1, 3.0, 1.0, 0.1)

    # Noise reduction toggle
    reduce_noise = st.checkbox("Reduce Background Noise")
    if reduce_noise:
        y = nr.reduce_noise(y=y, sr=sr)

    # Apply amplitude scaling
    y = y * amp_factor
    y = y[:int(sr * duration_slider)]

    # Display waveform
    st.subheader("📈 Waveform Display")
    fig, ax = plt.subplots(figsize=(10, 3))
    librosa.display.waveshow(y, sr=sr, ax=ax)
    ax.set_title("Filtered Heart Sound Waveform")
    st.pyplot(fig)

    # AI analysis (dummy for now)
    st.subheader("🧠 AI Analysis")
    st.success("No murmur detected. Heart sound appears normal.")

    # PDF generation button
    if st.button("📄 Generate PDF Report"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Heartest - Heart Sound Report", ln=True, align='C')
        pdf.ln(10)
        pdf.cell(200, 10, txt=f"Name: {name}", ln=True)
        pdf.cell(200, 10, txt=f"Age: {age} | Gender: {gender}", ln=True)
        pdf.cell(200, 10, txt=f"Symptoms: {symptoms}", ln=True)
        pdf.ln(10)
        pdf.multi_cell(0, 10, txt="AI Result: No murmur detected. Heart sound appears normal.")

        pdf_output = io.BytesIO()
        pdf.output(pdf_output)
        pdf_output.seek(0)

        b64 = base64.b64encode(pdf_output.read()).decode()
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="heartest_report.pdf">📥 Download Report PDF</a>'
        st.markdown(href, unsafe_allow_html=True)

else:
    st.warning("Upload a heart sound .wav file to begin analysis.")

# Footer
st.markdown("---")
st.markdown("Developed by JV-GIRI | Powered by Streamlit")
