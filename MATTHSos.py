import streamlit as st
import google.generativeai as genai
import random
import math
import plotly.graph_objects as go
import plotly.express as px
import networkx as nx
import numpy as np
import hashlib
import sqlite3
import json
from datetime import datetime
import pandas as pd
import random
import re
import os
import subprocess
from manim import *
from moviepy.editor import VideoFileClip, AudioFileClip
from gtts import gTTS
import numpy as np
import sympy as sp
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
import pytesseract
from PIL import Image
from elevenlabs.client import ElevenLabs
import openai
from dotenv import load_dotenv
from openai import OpenAI
import time

# ================================
# CONFIGURATION & SETUP
# ================================

def load_configuration():
    """Load and validate all configuration from environment variables"""
    # Load environment variables
    load_dotenv()
    
    # API Keys
    config = {
        'openrouter_api_key': os.getenv("OPENROUTER_API_KEY"),
        'google_gemini_api_key': os.getenv("GOOGLE_GEMINI_API_KEY"),
        'elevenlabs_api_key': os.getenv("ELEVENLABS_API_KEY"),
        
        # Application Settings
        'app_title': os.getenv("APP_TITLE", "Neo - AI Tutor"),
        'app_layout': os.getenv("APP_LAYOUT", "wide"),
        'sidebar_state': os.getenv("SIDEBAR_STATE", "expanded"),
        
        # Database Settings
        'database_name': os.getenv("DATABASE_NAME", "math_tutor.db"),
        
        # Video Generation Settings
        'manim_quality': os.getenv("MANIM_QUALITY", "ql"),
        'video_fps': os.getenv("VIDEO_FPS", "15"),
        'video_resolution': os.getenv("VIDEO_RESOLUTION", "480p"),
        
        # Audio Settings
        'audio_language': os.getenv("AUDIO_LANGUAGE", "en"),
        'audio_output_format': os.getenv("AUDIO_OUTPUT_FORMAT", "mp3"),
        
        # Security Settings
        'password_hash_algorithm': os.getenv("PASSWORD_HASH_ALGORITHM", "sha256")
    }
    
    # Validate required API keys
    missing_keys = []
    if not config['openrouter_api_key']:
        missing_keys.append("OPENROUTER_API_KEY")
    if not config['google_gemini_api_key']:
        missing_keys.append("GOOGLE_GEMINI_API_KEY")
    
    if missing_keys:
        st.error(f"❌ Missing required API keys: {', '.join(missing_keys)}. Please check your .env file.")
        st.stop()
    
    return config

# Load configuration
config = load_configuration()

# Configure Google Gemini
genai.configure(api_key=config['google_gemini_api_key'])
model = genai.GenerativeModel('gemini-2.5-pro')

# Configure ElevenLabs (optional)
# if config['elevenlabs_api_key']:
#     client = ElevenLabs(api_key=config['elevenlabs_api_key'])

# Page configuration
st.set_page_config(
    page_title=config['app_title'],
    layout=config['app_layout'],
    initial_sidebar_state=config['sidebar_state']
)

# ================================
# MODERN CSS STYLING
# ================================

st.markdown("""
<style>
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* Root CSS Variables */
:root {
    --primary-color: #7b2cbf;
    --primary-dark: #5a1d8d;
    --secondary-color: #e83cff;
    --accent-color: #9d4edd;

    --success-color: #2ee877;
    --warning-color: #ffbf47;
    --error-color: #ff5757;

    --bg-primary: #ffffff;
    --bg-secondary: #f8f9fa;
    --bg-tertiary: #e9ecef;

    --text-primary: #212529;
    --text-secondary: #6c757d;
    --text-muted: #9d4edd;

    --border-color: rgba(123, 44, 191, 0.2);

    --shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    --shadow-lg: 0 8px 16px rgba(0, 0, 0, 0.15);

    --border-radius: 12px;

    --transition: all 0.3s ease;
}


/* Global Styles */
.stApp {
    background: linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-secondary) 100%);
    color: var(--text-primary);
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Header Styling */
.main-header {
    background: linear-gradient(135deg, var(--bg-secondary), var(--bg-tertiary));
    padding: 2rem;
    border-radius: var(--border-radius);
    margin-bottom: 2rem;
    text-align: center;
    box-shadow: var(--shadow-lg);
    border: 1px solid var(--border-color);
}

.main-header h1 {
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 2.5rem;
    font-weight: 700;
    margin: 0;
    letter-spacing: -0.025em;
}

.main-header p {
    color: var(--text-secondary);
    font-size: 1.1rem;
    margin: 0.5rem 0 0 0;
    font-weight: 400;
}

/* Sidebar Styling */
.stSidebar {
    background: var(--bg-secondary);
    border-right: 1px solid var(--border-color);
}

.stSidebar .stSelectbox,
.stSidebar .stSlider {
    background: var(--bg-tertiary);
    border-radius: 8px;
    padding: 0.5rem;
    margin: 0.5rem 0;
}

.sidebar-nav {
    background: var(--bg-tertiary);
    border-radius: var(--border-radius);
    padding: 1rem;
    margin: 1rem 0;
    border: 1px solid var(--border-color);
}

.nav-item {
    display: flex;
    align-items: center;
    padding: 0.75rem 1rem;
    margin: 0.25rem 0;
    border-radius: 8px;
    cursor: pointer;
    transition: var(--transition);
    color: var(--text-secondary);
    text-decoration: none;
    font-weight: 500;
}

.nav-item:hover {
    background: var(--primary-color);
    color: white;
    transform: translateX(4px);
}

.nav-item.active {
    background: var(--primary-color);
    color: white;
    box-shadow: var(--shadow);
}

.nav-icon {
    margin-right: 0.75rem;
    font-size: 1.2rem;
}

/* Card Styling */
.custom-card {
    background: var(--bg-secondary);
    border: 1px solid var(--border-color);
    border-radius: var(--border-radius);
    padding: 1.5rem;
    margin: 1rem 0;
    box-shadow: var(--shadow);
    transition: var(--transition);
    backdrop-filter: blur(10px);
}

.custom-card:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg);
    border-color: var(--primary-color);
}

.card-header {
    display: flex;
    align-items: center;
    margin-bottom: 1rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid var(--border-color);
}

.card-title {
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--text-primary);
    margin: 0;
}

.card-icon {
    margin-right: 0.75rem;
    font-size: 1.5rem;
    color: var(--primary-color);
}
.stButton > button {
    position: relative;
    background: transparent;
    padding: 0.75rem 1.5rem;
    font-weight: 600;
    font-size: 1rem;
    width: 100%;
    font-family: 'Inter', sans-serif;
    transition: var(--transition);
    border: 1px solid var(--border-color);
    border-radius: var(--border-radius);
    z-index: 1;
    cursor: pointer;

    # /* Gradient text */
    # background-image: linear-gradient(135deg, var(--primary-color), var(--primary-dark));
    # -webkit-background-clip: text;
    # background-clip: text;
    # -webkit-text-fill-color: transparent;
}


/* Hover effect: white text and hide border */
.stButton > button:hover {
    background: linear-gradient(135deg, var(--primary-dark), var(--secondary-color));
    -webkit-background-clip: border-box;
    -webkit-text-fill-color: white;
    color: white;
    transform: translateY(-1px);
    box-shadow: var(--shadow-lg);
    border: 1px solid var(--border-color);
    border-radius: var(--border-radius);
}

/* Hide the gradient border on hover */
.stButton > button:hover::before {
    opacity: 0;
}


.stButton > button:active {
    transform: translateY(0);
}

/* Input Styling */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div > select {
    background: var(--bg-primary);
    border: 1px solid #dee2e6;
    border-radius: 8px;
    color: var(--text-primary);
    padding: 0.75rem;
    font-size: 1rem;
    transition: var(--transition);
    font-family: 'Inter', sans-serif;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus,
.stSelectbox > div > div > select:focus {
    border-color: var(--primary-color);
    box-shadow: 0 0 0 3px rgba(123, 44, 191, 0.1);
    outline: none;
    background: var(--bg-primary);
}

/* Tab Styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 0.5rem;
    background: var(--bg-secondary);
    border-radius: var(--border-radius);
    padding: 0.5rem;
    border: 1px solid var(--border-color);
}

.stTabs [data-baseweb="tab"] {
    background: transparent;
    border-radius: 8px;
    color: var(--text-secondary);
    font-weight: 500;
    padding: 0.75rem 1.5rem;
    transition: var(--transition);
    border: none;
}

.stTabs [aria-selected="true"] {
    background: var(--primary-color);
    color: white;
    box-shadow: var(--shadow);
}

/* Progress Bar */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, var(--primary-color), var(--accent-color));
    border-radius: 4px;
}

/* Expander Styling */
.streamlit-expanderHeader {
    background: var(--bg-tertiary);
    border-radius: 8px;
    color: var(--text-primary);
    font-weight: 600;
    padding: 1rem;
    border: 1px solid var(--border-color);
    transition: var(--transition);
}

.streamlit-expanderHeader:hover {
    background: var(--primary-color);
    color: white;
}

/* Status Messages */
.status-success {
    background: linear-gradient(135deg, var(--success-color), #059669);
    color: white;
    padding: 1rem;
    border-radius: 8px;
    font-weight: 600;
    text-align: center;
    margin: 1rem 0;
    box-shadow: var(--shadow);
}

.status-warning {
    background: linear-gradient(135deg, var(--warning-color), #d97706);
    color: white;
    padding: 1rem;
    border-radius: 8px;
    font-weight: 600;
    text-align: center;
    margin: 1rem 0;
    box-shadow: var(--shadow);
}

.status-error {
    background: linear-gradient(135deg, var(--error-color), #dc2626);
    color: white;
    padding: 1rem;
    border-radius: 8px;
    font-weight: 600;
    text-align: center;
    margin: 1rem 0;
    box-shadow: var(--shadow);
}

/* Code Blocks */
.stCode {
    background: var(--bg-secondary);
    border: 1px solid #dee2e6;
    border-radius: 8px;
    font-family: 'JetBrains Mono', monospace;
}

/* Video Container */
.video-container {
    background: var(--bg-tertiary);
    border-radius: var(--border-radius);
    padding: 1rem;
    margin: 1rem 0;
    border: 1px solid var(--border-color);
    box-shadow: var(--shadow);
}

/* Metrics */
.metric-card {
    background: var(--bg-tertiary);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 1rem;
    text-align: center;
    transition: var(--transition);
}

.metric-card:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow);
}

.metric-value {
    font-size: 2rem;
    font-weight: 700;
    color: var(--primary-color);
    margin: 0;
}

.metric-label {
    font-size: 0.875rem;
    color: var(--text-secondary);
    margin: 0.25rem 0 0 0;
    font-weight: 500;
}

/* Responsive Design */
@media (max-width: 768px) {
    .main-header h1 {
        font-size: 2rem;
    }
    
    .custom-card {
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    .nav-item {
        padding: 0.5rem 0.75rem;
    }
}

/* Scrollbar Styling */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: var(--bg-secondary);
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, var(--primary-color), var(--secondary-color));
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(180deg, var(--primary-dark), var(--primary-color));
}

/* Loading Animation */
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

.loading-pulse {
    animation: pulse 2s infinite;
}

/* Floating Action Button */
.floating-btn {
    position: fixed;
    bottom: 2rem;
    right: 2rem;
    background: var(--primary-color);
    color: white;
    border: none;
    border-radius: 50%;
    width: 60px;
    height: 60px;
    font-size: 1.5rem;
    cursor: pointer;
    box-shadow: var(--shadow-lg);
    transition: var(--transition);
    z-index: 1000;
}

.floating-btn:hover {
    background: var(--primary-dark);
    transform: scale(1.1);
}

/* Quiz Styling */
.quiz-question {
    background: var(--bg-tertiary);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 1.5rem;
    margin: 1rem 0;
}

.quiz-option {
    background: var(--bg-secondary);
    border: 1px solid var(--border-color);
    border-radius: 6px;
    padding: 0.75rem;
    margin: 0.5rem 0;
    cursor: pointer;
    transition: var(--transition);
}

.quiz-option:hover {
    background: var(--primary-color);
    color: white;
}

/* Feature Grid */
.feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1rem;
    margin: 2rem 0;
}

.feature-card {
    background: var(--bg-secondary);
    border: 1px solid var(--border-color);
    border-radius: var(--border-radius);
    padding: 1.5rem;
    text-align: center;
    transition: var(--transition);
    cursor: pointer;
}

.feature-card:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-lg);
    border-color: var(--primary-color);
}

.feature-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
    color: var(--primary-color);
}

.feature-title {
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 0.5rem;
}

.feature-description {
    color: var(--text-secondary);
    font-size: 0.875rem;
    line-height: 1.5;
}
</style>
""", unsafe_allow_html=True)

# ================================
# CORE BACKEND FUNCTIONS (UNCHANGED)
# ================================

def clean_manim_script(script: str) -> str:
    """Clean and format Manim script"""
    lines = script.strip().splitlines()
    if lines and lines[0].strip().startswith(r"\boxed{"):
        lines = lines[1:-1]
    script = "\n".join(lines)
    script = re.sub(r"```(?:python)?\s*", "", script)
    script = re.sub(r"```", "", script)
    
    # Ensure the script starts with the proper import
    cleaned_script = script.strip()
    if not cleaned_script.startswith("from manim import"):
        cleaned_script = "from manim import *\n\n" + cleaned_script
    
    return cleaned_script

def generate_manim_video(manim_code, video_class_name="MathExplanation"):
    """Generate Manim video from script"""
    timestamp = int(time.time())
    script_path = f"{video_class_name}_{timestamp}.py"
    cleaned_script = clean_manim_script(manim_code)
    
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(cleaned_script)
    
    # Use configuration for Manim settings
    manim_quality = config['manim_quality']
    video_fps = config['video_fps']
    video_resolution = config['video_resolution']
    
    subprocess.run(["manim", f"-{manim_quality}", script_path, video_class_name])
    
    video_dir = f"media/videos/{video_class_name}_{timestamp}/{video_resolution}{video_fps}"
    if not os.path.exists(video_dir):
        return None
    
    video_files = [f for f in os.listdir(video_dir) if f.endswith(".mp4")]
    if not video_files:
        return None
    
    video_files.sort(key=lambda x: os.path.getmtime(os.path.join(video_dir, x)), reverse=True)
    latest_video = video_files[0]
    video_path = os.path.join(video_dir, latest_video)
    
    return video_path

def synthesize_audio(text, audio_path="explanation_audio.mp3", lang=None):
    """Generate audio using gTTS (Google Text-to-Speech), with error handling."""
    try:
        # Use configuration for audio settings
        if lang is None:
            lang = config['audio_language']
        
        audio_format = config['audio_output_format']
        if not audio_path.endswith(f".{audio_format}"):
            audio_path = audio_path.rsplit(".", 1)[0] + f".{audio_format}"
        
        # Generate speech
        tts = gTTS(text=text, lang=lang)
        tts.save(audio_path)

        print(f"✅ Audio saved to {audio_path}")
        return audio_path

    except Exception as e:
        print("❌ Error during TTS synthesis:", e)
        return None

def combine_video_audio(video_path, audio_path, output_video="final_explanation.mp4"):
    """Combine video and audio"""
    if not os.path.exists(video_path) or not os.path.exists(audio_path):
        raise FileNotFoundError("Video or audio file not found")
    
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)
    audio = audio.subclip(0, min(video.duration, audio.duration))
    
    final_video = video.set_audio(audio)
    final_video.write_videofile(output_video, codec="libx264")
    
    return output_video

# ================================
# DATABASE FUNCTIONS (UNCHANGED)
# ================================

def hash_password(password):
    """Hash password using the configured algorithm from environment variables"""
    algorithm = config['password_hash_algorithm']
    
    if algorithm == "sha256":
        return hashlib.sha256(str.encode(password)).hexdigest()
    elif algorithm == "sha1":
        return hashlib.sha1(str.encode(password)).hexdigest()
    elif algorithm == "md5":
        return hashlib.md5(str.encode(password)).hexdigest()
    else:
        # Default to sha256 if unknown algorithm
        return hashlib.sha256(str.encode(password)).hexdigest()

def check_user(username, password):
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hash_password(password)))
    return c.fetchone() is not None

def create_user(username, password):
    try:
        progress = json.dumps({"completed_topics": [], "quiz_scores": {}, "practice_sets": {}})
        c.execute("INSERT INTO users (username, password, progress) VALUES (?, ?, ?)", 
                 (username, hash_password(password), progress))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def get_progress(username):
    c.execute("SELECT progress FROM users WHERE username=?", (username,))
    result = c.fetchone()
    if result and result[0]:
        return json.loads(result[0])
    return {"completed_topics": [], "quiz_scores": {}, "practice_sets": {}}

def update_progress(username, topic, score=None, practice_set=None):
    c.execute("SELECT progress FROM users WHERE username=?", (username,))
    result = c.fetchone()
    if result:
        progress = json.loads(result[0] or '{"completed_topics": [], "quiz_scores": {}, "practice_sets": {}}')
    else:
        progress = {"completed_topics": [], "quiz_scores": {}, "practice_sets": {}}
    
    if topic not in progress["completed_topics"]:
        progress["completed_topics"].append(topic)
    if score is not None:
        progress["quiz_scores"][topic] = score
    if practice_set is not None:
        progress["practice_sets"][topic] = practice_set
    c.execute("UPDATE users SET progress=? WHERE username=?", (json.dumps(progress), username))
    conn.commit()

def save_practice_set_as_pdf(practice_set):
    pdf_buffer = io.BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=letter)
    c.setFont("Helvetica", 12)
    c.drawString(100, 750, "Practice Set")
    y = 730
    
    for q in practice_set:
        lines = q.split(" ")
        line = ""
        for word in lines:
            if c.stringWidth(line + word, "Helvetica", 12) < 400:
                line += word + " "
            else:
                c.drawString(100, y, line.strip())
                y -= 20
                line = word + " "
                if y < 50:
                    c.showPage()
                    c.setFont("Helvetica", 12)
                    y = 750
        c.drawString(100, y, line.strip())
        y -= 20
        if y < 50:
            c.showPage()
            c.setFont("Helvetica", 12)
            y = 750
    
    c.save()
    pdf_buffer.seek(0)
    return pdf_buffer

# ================================
# DATABASE SETUP
# ================================

conn = sqlite3.connect(config['database_name'])
c = conn.cursor()

c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT,
        progress TEXT
    )
""")
conn.commit()

c.execute("PRAGMA table_info(users)")
columns = [column[1] for column in c.fetchall()]
if 'progress' not in columns:
    c.execute("ALTER TABLE users ADD COLUMN progress TEXT")
    conn.commit()

# ================================
# SESSION STATE INITIALIZATION
# ================================

def initialize_session_state():
    """Initialize session state variables"""
    defaults = {
        'user': None,
        'selected_menu': 'Problem Solver',
        'solution_text': None,
        'manim_script': None,
        'audio_script': None,
        'video_generated': False,
        'current_practice_set': [],
        'quiz_data': None,
        'practice_questions': None,
        'generated_scenario': None,
        'selected_application': None,
        'generated_questions': None,
        'messages': []
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# ================================
# UTILITY FUNCTIONS
# ================================

def render_math(text):
    """Render mathematical expressions"""
    st.write(text)

def display_status_message(message_type, message):
    """Display styled status messages"""
    if message_type == "success":
        st.markdown(f'<div class="status-success">✅ {message}</div>', unsafe_allow_html=True)
    elif message_type == "warning":
        st.markdown(f'<div class="status-warning">⚠️ {message}</div>', unsafe_allow_html=True)
    elif message_type == "error":
        st.markdown(f'<div class="status-error">❌ {message}</div>', unsafe_allow_html=True)

def create_nav_item(icon, text, key, is_active=False):
    """Create a navigation item"""
    active_class = "active" if is_active else ""
    return f"""
    <div class="nav-item {active_class}" onclick="selectMenu('{key}')">
        <span class="nav-icon">{icon}</span>
        <span>{text}</span>
    </div>
    """

# ================================
# MAIN APPLICATION
# ================================

def main():
    initialize_session_state()
    
    # Header
    st.markdown("""
<div class="main-header">
    <h1 style="
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    ">
         Neo - AI Tutor
    </h1>
    <p style="color: var(--text-secondary); font-size: 1.1rem;">
        Advanced mathematical problem solving with AI-powered explanations and automatic video generation
    </p>
</div>
""", unsafe_allow_html=True)
    
    # Authentication check
    if st.session_state.user is None:
        show_auth_interface()
        return
    
    # Main application interface
    show_main_interface()

def show_auth_interface():
    """Display modern login/signup interface"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        #st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["🔐 Login", "📝 Sign Up"])
        
        with tab1:
            st.markdown('<div class="card-header"><h3 class="card-title">Welcome Back!</h3></div>', unsafe_allow_html=True)
            username = st.text_input("Username", key="login_username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", key="login_password", placeholder="Enter your password")
            
            if st.button("🚀 Login", key="login_btn"):
                if check_user(username, password):
                    st.session_state.user = username
                    display_status_message("success", "Logged in successfully!")
                    st.rerun()
                else:
                    display_status_message("error", "Invalid username or password")
        
        with tab2:
            st.markdown('<div class="card-header"><h3 class="card-title">Create Account</h3></div>', unsafe_allow_html=True)
            new_username = st.text_input("Choose Username", key="signup_username", placeholder="Choose a unique username")
            new_password = st.text_input("Choose Password", type="password", key="signup_password", placeholder="Create a secure password")
            
            if st.button("✨ Create Account", key="signup_btn"):
                if create_user(new_username, new_password):
                    display_status_message("success", "Account created successfully! Please log in.")
                else:
                    display_status_message("error", "Username already exists")
        
        st.markdown('</div>', unsafe_allow_html=True)

def show_main_interface():
    """Display main application interface with sidebar navigation"""
    
    # Sidebar Navigation
    with st.sidebar:
        st.markdown(f"""
        <div class="custom-card">
            <div class="card-header">
                <span class="card-icon">👋</span>
                <h3 class="card-title">Welcome, {st.session_state.user}!</h3>
            </div>
       </div>
        """, unsafe_allow_html=True)
        
        # Navigation Menu
        # st.markdown('<div class="sidebar-nav">', unsafe_allow_html=True)
        st.markdown('<h4 style="color: var(--text-primary); margin-bottom: 1rem;">📚 Main Features</h4>', unsafe_allow_html=True)
        
        # Main navigation options
        main_options = [
            ("", "Problem Solver", "Problem Solver"),
            ("", "Handwritten Solver", "Handwritten Problem Solver"),
            ("", "Practice Questions", "Practice Questions"),
            ("", "Concept Explorer", "Concept Explorer"),
            ("", "Formula Generator", "Formula Generator"),
            ("", "Quiz", "Quiz")
        ]
        
        for icon, text, key in main_options:
            if st.button(f"{icon} {text}", key=f"nav_{key}", use_container_width=True):
                st.session_state.selected_menu = key
        
        st.markdown('<h4 style="color: var(--text-primary); margin: 1.5rem 0 1rem 0;">🚀 Advanced Features</h4>', unsafe_allow_html=True)
        
        # Advanced navigation options
        advanced_options = [
            ("", "Video Recommendations", "Video Recommendation"),
            ("", "Math Manipulatives", "Virtual Math Manipulatives"),
            ("", "Historical Context", "Historical Math Context"),
            ("", "Real-World Apps", "Real-World Applications"),
            ("", "Study Plans", "Study Plan Generator"),
            ("", "Analytics", "Performance Analytics")
        ]
        
        for icon, text, key in advanced_options:
            if st.button(f"{icon} {text}", key=f"nav_adv_{key}", use_container_width=True):
                st.session_state.selected_menu = key
        
        # st.markdown('</div>', unsafe_allow_html=True)
        
        # Settings Section
        with st.expander("⚙️ Settings"):
            skill_level = st.selectbox("Skill Level:", ["Beginner", "Intermediate", "Advanced", "Expert"])
            topic = st.selectbox("Math Topic:", [
                "Arithmetic", "Algebra", "Geometry", "Trigonometry", 
                "Calculus", "Linear Algebra", "Statistics", "Number Theory"
            ])
        
        # Progress Section
        progress = get_progress(st.session_state.user)
        #st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-header"><span class="card-icon">📊</span><h4 class="card-title">Your Progress</h4></div>', unsafe_allow_html=True)
        
        if progress['completed_topics']:
            st.markdown(f"**Topics Completed:** {len(progress['completed_topics'])}")
            for topic_item in progress['completed_topics'][-3:]:
                st.markdown(f"• {topic_item}")
        else:
            st.markdown("No completed topics yet")
        
        if progress['quiz_scores']:
            avg_score = sum(progress['quiz_scores'].values()) / len(progress['quiz_scores'])
            st.markdown(f"**Average Quiz Score:** {avg_score:.1f}%")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Logout Button
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.user = None
            st.rerun()
    
    # Main Content Area
    if st.session_state.selected_menu:
        execute_function(st.session_state.selected_menu, skill_level, topic)

def execute_function(option, skill_level, topic):
    """Execute the selected function with modern UI"""
    
    if option == "Problem Solver":
        show_problem_solver(skill_level, topic)
    elif option == "Handwritten Problem Solver":
        show_handwritten_solver(skill_level, topic)
    elif option == "Practice Questions":
        show_practice_questions(skill_level, topic)
    elif option == "Concept Explorer":
        show_concept_explorer(skill_level)
    elif option == "Formula Generator":
        show_formula_generator(skill_level)
    elif option == "Quiz":
        show_quiz(skill_level, topic)
    elif option == "Video Recommendation":
        show_video_recommendations()
    elif option == "Virtual Math Manipulatives":
        show_math_manipulatives()
    elif option == "Historical Math Context":
        show_historical_context()
    elif option == "Real-World Applications":
        show_real_world_applications(skill_level, topic)
    elif option == "Study Plan Generator":
        show_study_plan_generator(skill_level)
    elif option == "Performance Analytics":
        show_performance_analytics()

def show_problem_solver(skill_level, topic):
    """Modern problem solver interface"""
    st.markdown('<div class="card-header"><span class="card-icon">🧮</span><h2 class="card-title">AI Problem Solver</h2></div>', unsafe_allow_html=True)
    
    # Two-column layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
      #  st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-header"><span class="card-icon">📝</span><h3 class="card-title">Enter Your Problem</h3></div>', unsafe_allow_html=True)
        
        # Problem input
        problem = st.text_area(
            "Math Problem",
            placeholder="Enter your math problem here...\nExample: Solve for x: 2x + 5 = 13",
            height=150,
            key="problem_text"
        )
        
        # Solve button
        if st.button("🚀 Solve Problem", disabled=not problem.strip(), use_container_width=True):
            if problem.strip():
                solve_problem_pipeline(problem, skill_level, topic)
            else:
                display_status_message("warning", "Please enter a math problem first!")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-header"><span class="card-icon">📋</span><h3 class="card-title">Solution & Results</h3></div>', unsafe_allow_html=True)
        
        if st.session_state.solution_text:
            st.markdown("**Step-by-Step Solution:**")
            st.markdown(st.session_state.solution_text)
            
            # Video generation section
            if st.session_state.manim_script and st.session_state.audio_script:
                if st.button("🎬 Generate Video Explanation", use_container_width=True):
                    generate_video_explanation()
            
            # Display video if generated
            if st.session_state.video_generated and 'final_video_path' in st.session_state:
                st.markdown('<div class="video-container">', unsafe_allow_html=True)
                st.video(st.session_state.final_video_path)
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align: center; padding: 2rem; color: var(--text-muted);">
                <div style="font-size: 3rem;">🤖</div>
                <h3>Ready to Solve!</h3>
                <p>Enter a math problem to get started with AI-powered solutions.</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

def solve_problem_pipeline(problem, skill_level, topic):
    """Execute the complete problem solving pipeline with progress tracking"""
    
    progress_placeholder = st.empty()
    status_placeholder = st.empty()
    
    try:
        # Stage 1: Generate solution
        with st.spinner("🧠 Generating step-by-step solution..."):
            progress_placeholder.progress(20)
            prompt = f"Solve this {skill_level.lower()} level {topic.lower()} problem step by step, providing detailed explanations for each step. Problem: {problem}"
            response = model.generate_content(prompt)
            st.session_state.solution_text = response.text
        
        # Stage 2: Generate Manim script
        with st.spinner("🎨 Creating animation script..."):
            progress_placeholder.progress(50)
            manim_prompt = f"""
            ->Generate a Manim animation script that visually explains the given mathematical problem step by step.
                    The animation should include text explanations, dynamic equation transformations, relevant geometrical 
                    or graphical representations (if applicable), and smooth transitions using animations like FadeIn, Transform, 
                    and DrawBorderThenFill. Ensure the animations maintain engagement and clarity. Align the animation properly 
                    and one important main thing is I only want the code alone, not any strings other than the code because the 
                    Manim script gives syntactical errors. So give only the code alone compulsorily and also exclude (```python and ''') 
                    in the script.

                    generate the code without this error:("AttributeError: module 'manim.camera' has no attribute 'frame'").
                    And also Make sure to animate the video by align item more centralized and without ovelapping the otherthings.
                    
                  
                    Code Formation:
                    ->  Generate a Manim script using the latest version of ManimCE. Ensure the code includes proper object initialization, valid attributes, and smooth animations. 
                    The script should include:
                    -> A basic scene with animated text and shapes.
                        Error handling to avoid attribute errors, value errors, and missing methods.
                        Ensure animations are added to the scene correctly before playing them.
                        Generate code that runs without modifications.
                    -> Generate the python script only.
                    -> Use known variables alone.
                    -> Make sure to import everything that needs.
                    4. No run time error.
                    5. The formation of text and diagrams should not ovelap and neatly visible in the video.
                    
                    IMPORTANT: Always start your Manim script with these essential imports:
                    from manim import *
                    
                    This import statement is CRITICAL and must be included at the very beginning of every Manim script.
                    
                    there are some error you need to avoid(Important):
                    1. Attribute Errors
                        AttributeError: 'Scene' object has no attribute 'begin_ambient_camera_rotation'
                        AttributeError: 'Text' object has no attribute 'set_color'
                        AttributeError: 'NumberPlane' object has no attribute 'scale'
                        AttributeError: 'Group' object has no attribute 'add_updater'
                        AttributeError: 'ThreeDScene' object has no attribute 'wait'
                        AttributeError: 'OpenGLVMobject' object has no attribute 'generate_target'
                        AttributeError: 'Tex' object has no attribute 'next_to'
                        AttributeError: 'Graph' object has no attribute 'animate'
                        AttributeError: 'VolumeOfSphere' object has no attribute 'set_fill'
                        AttributeError: 'FadeIn' object has no attribute 'set_opacity'
                    2. Value Errors
                        ValueError: Cannot set color for Mobject without stroke
                        ValueError: Unknown color name 'rainbow'
                        ValueError: Cannot set fill color for a VMobject
                        ValueError: Interpolation failed due to NaN values
                        ValueError: Points array cannot be empty
                        ValueError: latex error converting to dvi. See log output above
                        ValueError: Invalid dimension for matrix
                        ValueError: Cannot animate non-Mobject type
                        ValueError: Number of anchors must match the number of control points
                        ValueError: Path cannot be created with zero-length vectors
                    3. Import Errors
                        ImportError: No module named 'manim'
                        ImportError: cannot import name 'ShowCreation' from 'manim'
                        ImportError: cannot import name 'Graph' from 'manim.mobject.graph'
                        ImportError: cannot import name 'TransformMatchingShapes'
                        ImportError: DLL load failed while importing cairo
                        ImportError: cannot import name 'ThreeDScene'
                        ImportError: cannot import name 'MathTex'
                        ImportError: cannot import name 'DashedVMobject'
                        ImportError: No module named 'manim.opengl'
                        ImportError: cannot import name 'Surface' from 'manim.mobject'
                    4. Type Errors
                        TypeError: Object of type 'Circle' has no len()
                        TypeError: 'int' object is not callable
                        TypeError: 'float' object is not iterable
                        TypeError: 'NoneType' object is not iterable
                        TypeError: expected str, bytes or os.PathLike object, not PosixPath
                        TypeError: unsupported operand type(s) for +: 'VMobject' and 'int'
                        TypeError: 'list' object is not callable
                        TypeError: cannot unpack non-iterable int object
                        TypeError: Missing required positional argument 'file_path'
                        TypeError: Object is not JSON serializable
                    5. Rendering Errors
                        RuntimeError: Cairo surface not properly initialized
                        RuntimeError: FFmpeg process returned non-zero exit code
                        RuntimeError: Shader compilation failed
                        RuntimeError: Could not open video file
                        RuntimeError: Cannot animate object with no animations
                        RuntimeError: ManimGL not found
                        RuntimeError: No output file created
                        RuntimeError: Object has been deleted before rendering
                        RuntimeError: Could not locate Tex output
                        RuntimeError: LaTeX process crashed
                    6. LaTeX Errors
                        ValueError: LaTeX failed to compile. Check your installation.
                        ValueError: Invalid TeX command
                        ValueError: Cannot create MathTex from empty string
                        ValueError: Undefined control sequence in LaTeX
                        ValueError: LaTeX file could not be generated
                        ValueError: Missing dollar signs in inline equation
                        ValueError: Extra brace detected in LaTeX string
                        ValueError: Unknown package 'amsmath'
                        ValueError: Overfull hbox detected
                        ValueError: LaTeX source file is empty
                    7. Camera & Scene Errors
                        AttributeError: 'ThreeDScene' object has no attribute 'set_camera_orientation'
                        ValueError: Invalid zoom level for camera
                        RuntimeError: Cannot rotate camera before initialization
                        ValueError: Cannot add ambient light in a 2D scene
                        IndexError: List index out of range while setting camera path
                        AttributeError: 'Camera' object has no attribute 'save_state'
                        RuntimeError: Cannot animate camera before scene is played
                        TypeError: Cannot assign NoneType to camera rotation
                        ValueError: Camera target must be a Mobject
                        RuntimeError: Camera cannot capture empty scene
                    8. Animation Errors
                        AttributeError: 'FadeIn' object has no attribute 'play'
                        ValueError: Animation requires at least one frame
                        RuntimeError: Cannot animate removed object
                        TypeError: Animation duration must be a number
                        ValueError: Cannot animate an empty list of Mobjects
                        RuntimeError: Too many nested animations
                        AttributeError: 'Transform' object has no attribute 'update'
                        IndexError: Animation list index out of range
                        RuntimeError: Mobject must be added to scene before animating
                        ValueError: Animation target cannot be None
                    9. File & Path Errors
                        FileNotFoundError: No such file or directory
                        PermissionError: Cannot write to directory
                        OSError: Could not create video file
                        ValueError: Invalid file extension
                        FileNotFoundError: FFmpeg binary not found
                        RuntimeError: Temporary directory could not be created
                        OSError: Disk full while saving output
                        ValueError: Cannot save Mobject to file
                        OSError: File already exists
                        FileNotFoundError: Required asset missing
                    10. OpenGL Errors
                        RuntimeError: OpenGL context not found
                        ValueError: Cannot use OpenGL mode in software rendering
                        AttributeError: 'GLScene' object has no attribute 'set_background'
                        RuntimeError: Shader compilation error
                        ValueError: Cannot render OpenGL object in CPU mode
                        RuntimeError: Framebuffer object creation failed
                        AttributeError: OpenGL buffer has no attribute 'bind'
                        RuntimeError: OpenGL version mismatch
                        TypeError: OpenGL Mobject requires vector input
                        ValueError: Invalid OpenGL vertex format

                    Additional requirements:
                    1. Use consistent color coding: blue for variables, green for final answers, red for important transformations.
                    2. Add wait() commands between key steps with appropriate timing (0.5-2 seconds) for better pacing.
                    3. Group related mathematical operations using VGroups for cleaner animations.
                    4. Use proper self references for all scene elements and camera operations.
                    5. Add progress_bar=True to animations that benefit from showing progression.
                    6. Ensure all text is properly positioned with appropriate font size (MathTex(...).scale(0.8)).
                    7. Include self.wait(3) at the end of the animation.
                    8. Use TracedPath for any graphical representations that involve motion.
                    9. Set background color with config.background_color = "#1f1f1f" at the class definition level.
                    10. Use ".arrange()" and ".next_to()" to dynamically position elements and prevent overlapping text.
                    11. Use "lag_ratio" to control animation flow and avoid abrupt jumps.
                    13. Use camera.frame.animate for zooming into key equations or highlighting important transformations.
                    14. If using 3D, ensure smooth perspective shifts and avoid elements getting cropped.
                    15. Implement layering control with ".set_z_index()" to ensure visibility of all elements.
                    16. Introduce a slight glow effect for final answers for better visibility.
                    17. Use "rate_func=smooth" for Transform animations to make them visually appealing.
                    18. Ensure all imported packages are explicitly included to prevent runtime errors.
                    19. If a function or variable is referenced, make sure it is defined in the script to prevent crashes.
                    20. If the solution requires comparisons, show visual side-by-side comparisons using multiple aligned elements.
                    21. If a graph is needed, ensure axes are labeled clearly, and data points are animated dynamically.
                    22. Use opacities and fade effects for de-emphasizing unimportant steps while keeping focus on key calculations.

                    Video Animation:
                    - Use 3D animation if required for better visualization.
                    - Use fade out for elements that need to disappear instead of sudden removals.

                    Topic-specific animation techniques (3Blue1Brown style):
                    - For trigonometry: Use the UnitCircle class with animated angles, include DashedLine for projections, and animate sine/cosine waves growing from the circle.
                    - For calculus: Use NumberPlane with animated slopes/tangent lines that change color based on values, zoom in progressively to show limits, and use area filling animations for integrals.
                    - For algebra: Transform equations with color highlighting for each step, use coordinate shifts to show operations, and grow/shrink terms during simplification.
                    - For geometry: Use opacity changes to reveal cross-sections, include dotted construction lines, and animate 3D objects rotating to show different perspectives.
                    - For statistics: Create animated histograms that transform into probability curves, use color gradients to show probability regions, and animate individual data points.
                    - For vectors: Show arrows in coordinate systems that transform/combine with smooth animations, use shadowing for projections.
                    - For series: Create animated stacking of terms, use color gradients to show convergence/divergence, and include partial sum tracking.
                    - For logarithms: Use area stretching/compressing to visualize log properties, animate exponential growth with highlighting.
                    - For complex numbers: Use the ComplexPlane class with transformations, animate mapping between rectangular and polar forms with rotating vectors.           

    ******Importtant Note:The below format should be used only for the Manim script and not for any other.******

        You are an expert in creating educational animations using Manim. Your task is to generate Python code for a Manim animation that visually explains a given topic or concept. Follow these steps:

1. *Understand the Topic*:
   - Analyze the user's topic to identify the key concepts that need to be visualized.
   - Break down the topic into smaller, digestible components (e.g., steps, mechanisms, equations).

2. *Plan the Animation*:
   - Create a storyboard for the animation, ensuring it flows logically from one concept to the next.
   - Decide on the visual elements (e.g., shapes, graphs, text) that will represent each concept.
   - Ensure all elements stay within the screen's aspect ratio (-7.5 to 7.5 on x-axis, -4 to 4 on y-axis).
   - Plan proper spacing between elements to avoid overlap.
   - Make sure the objects or text in the generated code are not overlapping at any point in the video. 
   - Make sure that each scene is properly cleaned up before transitioning to the next scene.

3. *Write the Manim Code*:
   - Use Manim's library to create the animation. Include comments in the code to explain each step.
   - Ensure the code is modular, with separate functions for each key concept.
   - Use a consistent style (e.g., 3Blue1Brown style) with appropriate colors, labels, and animations.
   - Implement clean transitions between scenes by removing all elements from previous scene
   - Use self.play(FadeOut(*self.mobjects)) at the end of each scene.
   - Add wait() calls after important animations for better pacing.
   - Make sure the objects or text in the generated code are not overlapping at any point in the video. 
   - Make sure that each scene is properly cleaned up before transitioning to the next scene.
   - Dont Use glow effects,ShowCreation, and other effects that are not supported in the latest ManimCE version.

4. *Output the Code*:
   - Provide the complete Python script that can be run using Manim.
   - Include instructions on how to run the script (e.g., command to render the animation).
   - Verify all scenes have proper cleanup and transitions.

*Example Input*:
- Topic: "Neural Networks"
- Key Points: "neurons and layers, weights and biases, activation functions"
- Style: "3Blue1Brown style"

    
NOTE!!!: Make sure the objects or text in the generated code are not overlapping at any point in the video. Make sure that each scene is properly cleaned up before transitioning to the next scene
                    
                    Remember, provide ONLY executable code with NO explanatory text or markdown formatting. {problem}
            """
            
            solution_response = model.generate_content(manim_prompt)
            st.session_state.manim_script = solution_response.text
        
        # Stage 3: Enhance with multi-stage AI
        with st.spinner("🔧 Enhancing with advanced AI models..."):
            progress_placeholder.progress(80)
            
            # DeepSeek enhancement
            client_openrouter = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=config['openrouter_api_key'],
            )
            
            completion = client_openrouter.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": "https://neo-ai-tutor.streamlit.app/",
                    "X-Title": "Neo - AI Tutor",
                },
                model="qwen/qwen3-coder:free",
                messages=[
                    {
                        "role": "system",
                        "content": """You are a Manim animation expert trained in 3Blue1Brown's style. Your task is to enhance Manim code with these principles:
                    1.Mathematical Clarity:
                    - Precise alignment of all elements
                    - Logical camera movements that follow the math
                    - Clean labeling with proper LaTeX

                    2. Code Quality:
                    - Remove all redundant animations
                    - Optimal use of VGroups
                    - Proper scene cleanup
                    - PEP 8 compliance
                    - No visual clutter"""
                    },
                    {
                        "role": "user",
                        "content": f"""enhance the following Manim code in the clean, mathematical style of 3Blue1Brown. The scene should last more than 30 seconds with smooth pacing and no flashy effects. Extend the code with more meaningful lines to make the video longer, while keeping it minimal and elegant. Ensure all brackets are properly opened and closed. Do not exceed the screen space with lines or shapes, and fade out any unnecessary objects smoothly when transitioning between scenes. Output only the corrected and improved Manim code—exclude all explanations and formatting like backticks or \boxed.
                         Note : If the code creates 3-dimension animation, then the text created for the animation should be in 2-dimension in the animated video {st.session_state.manim_script}"""
                    }
                ],
                max_tokens=4000,
                temperature=0.3
            )
            
            enhanced_script = completion.choices[0].message.content
            print(enhanced_script)
        # Stage 4: Final enhancement with GPT-4 and voiceover
        with st.spinner("🎙️ Generating audio and video content..."):
            progress_placeholder.progress(100)
            
            final_completion = client_openrouter.chat.completions.create(
                model="openai/gpt-4o-mini",#openai/gpt-4o-mini
                messages=[
                    {
                        "role": "system",
                        "content": """You are a Manim animation expert trained in 3Blue1Brown's style. Your task is to enhance Manim code with these principles:
                    1. Mathematical Clarity:
                    - Precise alignment of all elements
                    - Logical camera movements that follow the math
                    - Clean labeling with proper LaTeX

                    2. Visual Style:
                    - Smooth animations (rate_func=smooth)
                    - Minimalist color palette (blue, white, yellow highlights)
                    - Proper use of TransformMatchingTex for equations
                    - Subtle but effective scene transitions

                    3. Code Quality:
                    - Remove all redundant animations
                    - Optimal use of VGroups
                    - Proper scene cleanup
                    - PEP 8 compliance
                    - No visual clutter
                    Note : Your task is to enhance Manim code and provide matching voiceover scripts because you are the only one in the world who can write a manim script along with the well suited voice script."""
                    },
                    {
                        "role": "user",
                        "content": f"""Enhance the following Manim code in the clean, mathematical style of 3Blue1Brown. The video should last more than 45 seconds with smooth pacing and no flashy effects. Extend the animation meaningfully to ensure it is easy to understand, visually engaging, and includes super pictorial representations of the concepts. Maintain a minimal and elegant approach, keeping all elements within screen boundaries. Use smooth fade-outs for unnecessary elements during transitions. Ensure all brackets are properly opened and closed. 

IMPORTANT: Always start your Manim script with: from manim import *

Output only the corrected and improved Manim code—exclude all explanations, formatting symbols, and do not use \boxed or backticks.
➤ Output exactly two sections:
1. Manim Code: Provide only the corrected, complete Manim code. No comments, markdown, or explanation. The code should animate the core mathematical content clearly, using well-paced timing that naturally guides narration. Avoid excessive effects or transitions — clarity comes first.
2. Voiceover Script: Provide a voiceover narration that strictly matches the visual content and timing of the animation. Focus only on the main mathematical or conceptual steps shown on screen — do not narrate transitions, animations, or metadata. Avoid filler words, enthusiasm, or theatrical tone. The narration must be clear, instructional, and paced to match each animation block. Do not describe what the animation is doing — only narrate the concept or math that is visually being presented.

⚠ Ensure:
Each visual step has a corresponding voiceover line.
Timing feels natural based on animation durations.
No LaTeX compilation errors will occur in Manim using MathTex.
The formatting works well with both Tex and MathTex.
No voiceover for padding animations like fading in/out titles, logo reveals, or decorative motion.

Your task is to enhance Manim code with these principles:
1. Mathematical Clarity:
Precise alignment of all elements
Logical camera movements that follow the math
Clean labeling with proper LaTeX

2. Visual Style:
Smooth animations (rate_func=smooth)
Minimalist color palette (blue, white, yellow highlights)
Proper use of TransformMatchingTex for equations
Subtle but effective scene transitions

3. Code Quality:
Remove all redundant animations
Optimal use of VGroups
Proper scene cleanup
PEP 8 compliance
No visual clutter

Important requirements:
Break down complex LaTeX into multiple MathTex(...) lines instead of nesting long equations inside one block.Avoid overuse of left and \right when not necessary, especially when wrapping expressions that contain fractions or nested parentheses.Use \frac properly, but avoid combining multiple left(...\right) pairs with \frac inside a single expression.Escape problematic LaTeX characters if needed (like _, ^, or ).Format the output using .scale(...) and .next_to(...) for proper placement of parts of the equation.
I'm working on a Python 3.13 project using Manim (v0.19.0 or newer) and NumPy. I need to create a visualization involving dynamic elements like always_redraw, DashedLine, and coordinate axes. Please ensure the code handles points as consistent 3D NumPy arrays to avoid errors like ValueError: setting an array element with a sequence or ValueError: all the input arrays must have same number of dimensions.
When generating points, such as the center of a circle or coordinates from Axes, always use .get_center() or axes.c2p(x, y) to convert them properly into 3D points. Avoid mixing 1D or 2D points with 3D points, as this can cause crashes in DashedLine or during array stacking.
Ensure that any use of regular expressions uses raw string literals like r"\d+" to avoid SyntaxWarning: invalid escape sequence, which is stricter in Python 3.13. For any external libraries such as pydub, ensure compatibility with Python 3.13 syntax and avoid deprecated features or outdated patterns.
Finally, please make the code modular and robust, with proper imports and error-free structure. I’m especially interested in reliable animation updates using Manim’s always_redraw, so make sure that lambda functions return valid Mobjects and handle updates gracefully throughout the animation timeline.

Note : Important !!!!!!!!!!!!!!! Important Emergency!!!!!
No visual clutter
Text should not overwrite
{enhanced_script}"""
                    }
                ],
                max_tokens=4000,
                temperature=0.3
            )
            
            content = final_completion.choices[0].message.content
            print(content)
            
            # Extract Manim code and voiceover script
            parts = re.split(r'(?i)Voiceover Script:', content, maxsplit=1)
            if len(parts) == 2:
                st.session_state.manim_script = parts[0].strip()
                st.session_state.audio_script = parts[1].strip()
            else:
                st.session_state.manim_script = content.strip()
                st.session_state.audio_script = "No voiceover script generated. Please try again."
        
        progress_placeholder.empty()
        display_status_message("success", "Problem solved successfully! Click 'Generate Video Explanation' to create the video.")
        
    except Exception as e:
        progress_placeholder.empty()
        display_status_message("error", f"An error occurred: {str(e)}")

def generate_video_explanation():
    """Generate the complete video explanation with progress tracking"""
    try:
        progress_placeholder = st.empty()
        
        with st.spinner("🎨 Generating Manim animation..."):
            progress_placeholder.progress(33)
            video_path = generate_manim_video(st.session_state.manim_script)
            if not video_path:
                raise Exception("Failed to generate Manim video")
        
        with st.spinner("🎙️ Synthesizing audio narration..."):
            progress_placeholder.progress(66)
            audio_path = synthesize_audio(st.session_state.audio_script)
        
        with st.spinner("🎬 Combining video and audio..."):
            progress_placeholder.progress(100)
            final_video_path = combine_video_audio(video_path, audio_path)
        
        st.session_state.final_video_path = final_video_path
        st.session_state.video_generated = True
        
        progress_placeholder.empty()
        display_status_message("success", "Video generated successfully!")
        st.rerun()
        
    except Exception as e:
        display_status_message("error", f"Video generation failed: {str(e)}")

def show_handwritten_solver(skill_level, topic):
    """Handwritten problem solver interface"""
    st.markdown('<div class="card-header"><span class="card-icon">✍️</span><h2 class="card-title">Handwritten Problem Solver</h2></div>', unsafe_allow_html=True)
    
    #st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Upload an image of a handwritten math problem", 
        type=["jpg", "jpeg", "png"],
        help="Take a clear photo of your handwritten math problem"
    )
    
    def extract_text_from_image(uploaded_file):
        image = Image.open(uploaded_file)
        text = pytesseract.image_to_string(image)
        return text.strip()

    if uploaded_file is not None:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        
        with col2:
            extracted_text = extract_text_from_image(uploaded_file)
            st.markdown("**Extracted Text:**")
            st.text_area("", value=extracted_text if extracted_text else "No text could be extracted from the image.", height=150, disabled=True)
            
            if extracted_text and st.button("🚀 Solve Problem", use_container_width=True):
                prompt = f"""Solve this {skill_level.lower()} level {topic.lower()} problem step by step, providing detailed explanations for each step. Problem: {extracted_text}"""
                response = model.generate_content(prompt)
                
                st.markdown("**Step-by-Step Solution:**")
                render_math(response.text)
                update_progress(st.session_state.user, topic)
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_practice_questions(skill_level, topic):
    """Practice questions interface"""
    st.markdown('<div class="card-header"><span class="card-icon">📝</span><h2 class="card-title">Practice Questions</h2></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
       # st.markdown('<div class="custom-card">', unsafe_allow_html=True)
       # st.markdown('<div class="card-header"><h3 class="card-title">Generate Questions</h3></div>', unsafe_allow_html=True)
        
        if st.button("📚 Generate Practice Questions", use_container_width=True):
            num_questions = 10
            prompt = f"""Generate {num_questions} {skill_level.lower()} level {topic.lower()} math questions with detailed solutions.
            Ensure each question and solution is in this format:
            Q: [question]\nS: [solution]\nSeparate each question-answer pair with a blank line."""
            
            try:
                response = model.generate_content(prompt)
                if not response or not hasattr(response, 'text'):
                    display_status_message("error", "API response blocked or invalid. Please try again.")
                    return
                
                raw_text = response.text.strip()
                question_solution_pairs = re.findall(r"Q:\s*(.+?)\nS:\s(.+?)\n", raw_text, re.DOTALL)
                
                if not question_solution_pairs:
                    display_status_message("error", "Failed to extract questions and solutions. Please regenerate.")
                    return
                
                st.session_state.practice_questions = question_solution_pairs
                display_status_message("success", f"Generated {len(question_solution_pairs)} practice questions!")
            except Exception as e:
                display_status_message("error", f"An error occurred: {e}")
        
        if st.button("🔄 Reset Questions", use_container_width=True):
            if 'practice_questions' in st.session_state:
                del st.session_state.practice_questions
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        if "practice_questions" in st.session_state and st.session_state.practice_questions:
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown('<div class="card-header"><h3 class="card-title">Practice Questions</h3></div>', unsafe_allow_html=True)
            
            for i, (q, s) in enumerate(st.session_state.practice_questions, 1):
                with st.expander(f"Question {i}"):
                    st.write(q.strip())
                    user_solution = st.text_area(f"Your Solution for Question {i}", key=f"solution_{i}")
                    
                    if st.button(f"Check Solution {i}", key=f"check_{i}"):
                        st.write("**Correct Solution:**")
                        st.write(s.strip())
                        
                        if user_solution.strip():
                            feedback_prompt = f"""Compare the following solutions and provide feedback:
                            Correct Solution: {s.strip()}
                            User's Solution: {user_solution.strip()}
                            Provide constructive feedback and suggestions for improvement."""
                            try:
                                feedback = model.generate_content(feedback_prompt)
                                st.write("**Feedback:**")
                                st.write(feedback.text)
                            except Exception as e:
                                display_status_message("error", f"Error generating feedback: {e}")
            
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="custom-card" style="text-align: center; padding: 3rem;">
                <div style="font-size: 4rem;">📝</div>
                <h3>No Questions Generated</h3>
                <p>Click "Generate Practice Questions" to start practicing!</p>
            </div>
            """, unsafe_allow_html=True)

def show_concept_explorer(skill_level):
    """Concept explorer interface"""
    st.markdown('<div class="card-header"><span class="card-icon">🔬</span><h2 class="card-title">Concept Explorer</h2></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
    #    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
      #  st.markdown('<div class="card-header"><h3 class="card-title">Explore Concepts</h3></div>', unsafe_allow_html=True)
        
        concept = st.text_input("Enter a math concept:", placeholder="e.g., derivatives, matrices, probability")
        
        if st.button("🔍 Explore Concept", disabled=not concept.strip(), use_container_width=True):
            if concept.strip():
                prompt = f"""Provide a comprehensive explanation of '{concept}' suitable for a {skill_level.lower()} level student. Include:
                1. Definition
                2. Historical context
                3. Key principles
                4. Real-world applications
                5. Related concepts
                6. Common misconceptions
                7. Advanced implications (if applicable)"""
                
                try:
                    response = model.generate_content(prompt)
                    if not response or not hasattr(response, 'text'):
                        display_status_message("error", "API response blocked or invalid. Please try again.")
                        return
                    st.session_state.concept_explanation = response.text
                    update_progress(st.session_state.user, concept)
                    display_status_message("success", f"Concept '{concept}' explored successfully!")
                except Exception as e:
                    display_status_message("error", f"An error occurred: {e}")
            else:
                display_status_message("warning", "Please enter a math concept.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        if hasattr(st.session_state, 'concept_explanation'):
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown('<div class="card-header"><h3 class="card-title">Concept Explanation</h3></div>', unsafe_allow_html=True)
            render_math(st.session_state.concept_explanation)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="custom-card" style="text-align: center; padding: 3rem;">
                <div style="font-size: 4rem;">🔬</div>
                <h3>Ready to Explore!</h3>
                <p>Enter a mathematical concept to get detailed explanations and insights.</p>
            </div>
            """, unsafe_allow_html=True)

def show_formula_generator(skill_level):
    """Formula generator interface"""
    st.markdown('<div class="card-header"><span class="card-icon">📐</span><h2 class="card-title">Formula Generator</h2></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
      #  st.markdown('<div class="custom-card">', unsafe_allow_html=True)
       # st.markdown('<div class="card-header"><h3 class="card-title">Generate Formulas</h3></div>', unsafe_allow_html=True)
        
        formula_topic = st.text_input("Enter a topic:", placeholder="e.g., quadratic equations, trigonometry")
        
        if st.button("📐 Generate Formulas", disabled=not formula_topic.strip(), use_container_width=True):
            if formula_topic.strip():
                prompt = f"""Generate a comprehensive list of {skill_level.lower()} level formulas related to '{formula_topic}'.
                For each formula, provide:
                1. Formula name
                2. The formula itself
                3. A brief explanation of its use
                4. Key variables explained
                5. Any important conditions or limitations"""
                
                try:
                    response = model.generate_content(prompt)
                    if not response or not hasattr(response, 'text'):
                        display_status_message("error", "API response blocked or invalid. Please try again.")
                        return
                    st.session_state.formula_list = response.text
                    update_progress(st.session_state.user, formula_topic)
                    display_status_message("success", f"Formulas for '{formula_topic}' generated successfully!")
                except Exception as e:
                    display_status_message("error", f"An error occurred: {e}")
            else:
                display_status_message("warning", "Please enter a topic for formula generation.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        if hasattr(st.session_state, 'formula_list'):
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown('<div class="card-header"><h3 class="card-title">Generated Formulas</h3></div>', unsafe_allow_html=True)
            render_math(st.session_state.formula_list)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="custom-card" style="text-align: center; padding: 3rem;">
                <div style="font-size: 4rem;">📐</div>
                <h3>Formula Generator Ready!</h3>
                <p>Enter a mathematical topic to generate relevant formulas with explanations.</p>
            </div>
            """, unsafe_allow_html=True)

def show_quiz(skill_level, topic):
    """Modern quiz interface"""
    st.markdown('<div class="card-header"><span class="card-icon">🧩</span><h2 class="card-title">Interactive Quiz</h2></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
      #  st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-header"><h3 class="card-title">Quiz Controls</h3></div>', unsafe_allow_html=True)
        
        if st.button("🧩 Generate New Quiz", use_container_width=True):
            if st.session_state.quiz_data is None:
                prompt = f"""
                Create a multiple-choice quiz with exactly 5 unique questions on {topic}, suitable for a {skill_level.lower()} level student.
                Each question must have:
                - A unique math-related question
                - 4 answer choices (A, B, C, D)
                - The correct answer
                - A brief explanation of the correct answer

                Format:
                Q: [Question]
                A) [Option A]
                B) [Option B]
                C) [Option C]
                D) [Option D]
                Correct: [Correct option letter]
                Explanation: [Brief explanation]

                Separate each question with a blank line.
                """
                response = model.generate_content(prompt)
                quiz_text = response.text.strip()

                try:
                    question_pattern = re.findall(
                        r"Q:\s*(.+?)\s*A\)\s(.+?)\s*B\)\s(.+?)\s*C\)\s(.+?)\s*D\)\s(.+?)\s*Correct:\s([A-D])\s*Explanation:\s*(.+?)\s(?=Q:|$)", 
                        quiz_text, 
                        re.DOTALL
                    )

                    if len(question_pattern) != 5:
                        raise ValueError(f"Expected 5 questions, but found {len(question_pattern)}. Check AI formatting.")

                    st.session_state.quiz_data = []
                    for q in question_pattern:
                        question_text = q[0]
                        options = [f"A) {q[1]}", f"B) {q[2]}", f"C) {q[3]}", f"D) {q[4]}"]
                        correct_answer = q[5].strip().upper()
                        explanation = q[6]

                        st.session_state.quiz_data.append({
                            "question": question_text,
                            "options": options,
                            "correct_answer": correct_answer,
                            "explanation": explanation,
                            "user_answer": None,
                            "answered": False,
                        })
                    
                    display_status_message("success", "Quiz generated successfully!")

                except (IndexError, ValueError) as e:
                    display_status_message("error", f"Error generating quiz: {e}")
                except Exception as e:
                    display_status_message("error", f"Unexpected error: {e}")
        
        if st.session_state.quiz_data:
            if st.button("🔄 Retake Quiz", use_container_width=True):
                for q in st.session_state.quiz_data:
                    q["user_answer"] = None
                st.rerun()
            
            if st.button("📊 New Quiz", use_container_width=True):
                st.session_state.quiz_data = None
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        if st.session_state.quiz_data:
      #      st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown('<div class="card-header"><h3 class="card-title">Quiz Questions</h3></div>', unsafe_allow_html=True)
            
            for i, question_data in enumerate(st.session_state.quiz_data):
                st.markdown(f'<div class="quiz-question">', unsafe_allow_html=True)
                st.write(f"**Q{i+1}: {question_data['question']}**")
                
                user_answer = st.radio(
                    "Select your answer:",
                    question_data["options"],
                    key=f"q{i}",
                    index=None  
                )

                st.session_state.quiz_data[i]["user_answer"] = user_answer
                st.markdown('</div>', unsafe_allow_html=True)
            
            if st.button("📝 Submit Quiz", use_container_width=True):
                correct_count = 0
                
                for i, question_data in enumerate(st.session_state.quiz_data):
                    if question_data["user_answer"]:
                        if question_data["user_answer"].startswith(question_data["correct_answer"]):
                            display_status_message("success", f"Q{i+1}: Correct!")
                            correct_count += 1
                        else:
                            display_status_message("error", f"Q{i+1}: Incorrect. The correct answer is {question_data['correct_answer']}.")
                        st.write(f"**Explanation:** {question_data['explanation']}")

                score = (correct_count / len(st.session_state.quiz_data)) * 100
                st.markdown(f'<div class="metric-card"><div class="metric-value">{score:.0f}%</div><div class="metric-label">Your Score</div></div>', unsafe_allow_html=True)
                update_progress(st.session_state.user, topic, score)
            
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="custom-card" style="text-align: center; padding: 3rem;">
                <div style="font-size: 4rem;">🧩</div>
                <h3>Quiz Ready!</h3>
                <p>Click "Generate New Quiz" to start testing your knowledge!</p>
            </div>
            """, unsafe_allow_html=True)

def show_video_recommendations():
    """Video recommendations interface"""
    st.markdown('<div class="card-header"><span class="card-icon">🎬</span><h2 class="card-title">Video Recommendations</h2></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-header"><h3 class="card-title">Search Videos</h3></div>', unsafe_allow_html=True)
        
        search_topic = st.text_input("Search for math lectures:", placeholder="e.g., calculus, linear algebra")
        
        if st.button("🔍 Search Videos", disabled=not search_topic.strip(), use_container_width=True):
            if search_topic.strip():
                prompt = f"""If the topic **{search_topic}** is not related to mathematics, return 'Out of scope.' 
                Otherwise, provide a list of 3-5 top YouTube videos for learning about **{search_topic}**. 
                For each video, include: 
                1. **Title:** The exact video title 
                2. **Channel:** The name of the YouTube channel 
                3. **URL:** The complete YouTube link 
                4. **Description:** A brief one-sentence summary explaining why this video is useful 
                Only include real, educational content from reputable math-focused channels such as 3Blue1Brown, Khan Academy, MIT OpenCourseWare, Professor Leonard, and Numberphile.
                Avoid unnecessary explanations—just provide the structured information clearly.
                Don't generate the script in json format"""
                
                try:
                    interpretation = model.generate_content(prompt)
                    st.session_state.video_recommendations = interpretation.text
                    display_status_message("success", f"Found video recommendations for '{search_topic}'!")
                except Exception as e:
                    display_status_message("error", f"Error searching videos: {e}")
            else:
                display_status_message("warning", "Please enter a search topic.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        if hasattr(st.session_state, 'video_recommendations'):
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown('<div class="card-header"><h3 class="card-title">Recommended Videos</h3></div>', unsafe_allow_html=True)
            st.write(st.session_state.video_recommendations)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="custom-card" style="text-align: center; padding: 3rem;">
                <div style="font-size: 4rem;">🎬</div>
                <h3>Video Search Ready!</h3>
                <p>Enter a math topic to find the best educational videos from top channels.</p>
            </div>
            """, unsafe_allow_html=True)

def show_math_manipulatives():
    """Virtual math manipulatives interface"""
    st.markdown('<div class="card-header"><span class="card-icon">🎲</span><h2 class="card-title">Virtual Math Manipulatives</h2></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-header"><h3 class="card-title">Choose Manipulative</h3></div>', unsafe_allow_html=True)
        
        manipulative_type = st.selectbox("Select a manipulative:", ["Fraction Visualizer", "Geometry Explorer", "Algebra Tiles"])
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
       # st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        
        if manipulative_type == "Fraction Visualizer":
            st.markdown('<div class="card-header"><h3 class="card-title">Fraction Visualizer</h3></div>', unsafe_allow_html=True)
            
            col_a, col_b = st.columns(2)
            with col_a:
                numerator = st.slider("Numerator", 1, 10, 3)
            with col_b:
                denominator = st.slider("Denominator", 1, 10, 5)
            
            fig = go.Figure(go.Pie(
                values=[numerator, denominator - numerator], 
                labels=["Filled", "Remaining"], 
                hole=0.4,
                marker_colors=['#2563eb', '#e2e8f0']
            ))
            fig.update_layout(
                title=f"Fraction Representation: {numerator}/{denominator}",
                template="plotly_dark",
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
            
            col_c, col_d = st.columns(2)
            with col_c:
                st.markdown(f'<div class="metric-card"><div class="metric-value">{numerator/denominator:.3f}</div><div class="metric-label">Decimal</div></div>', unsafe_allow_html=True)
            with col_d:
                st.markdown(f'<div class="metric-card"><div class="metric-value">{(numerator/denominator)*100:.1f}%</div><div class="metric-label">Percentage</div></div>', unsafe_allow_html=True)
        
        elif manipulative_type == "Geometry Explorer":
            st.markdown('<div class="card-header"><h3 class="card-title">Geometry Explorer</h3></div>', unsafe_allow_html=True)
            
            shape = st.selectbox("Choose a shape:", ["Circle", "Square", "Triangle"])
            
            if shape == "Circle":
                radius = st.slider("Radius", 1, 10, 5)
                fig = go.Figure()
                fig.add_shape(
                    type="circle", 
                    xref="x", yref="y", 
                    x0=-radius, y0=-radius, 
                    x1=radius, y1=radius, 
                    line=dict(color="#2563eb", width=3),
                    fillcolor="rgba(37, 99, 235, 0.2)"
                )
                fig.update_layout(
                    title=f"Circle (Radius: {radius})", 
                    xaxis_range=[-radius-1, radius+1], 
                    yaxis_range=[-radius-1, radius+1],
                    template="plotly_dark",
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
                
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown(f'<div class="metric-card"><div class="metric-value">{math.pi * radius**2:.2f}</div><div class="metric-label">Area</div></div>', unsafe_allow_html=True)
                with col_b:
                    st.markdown(f'<div class="metric-card"><div class="metric-value">{2 * math.pi * radius:.2f}</div><div class="metric-label">Circumference</div></div>', unsafe_allow_html=True)
        
        elif manipulative_type == "Algebra Tiles":
            st.markdown('<div class="card-header"><h3 class="card-title">Algebra Tiles</h3></div>', unsafe_allow_html=True)
            
            col_a, col_b = st.columns(2)
            with col_a:
                x_coeff = st.slider("Coefficient of x", -10, 10, 1)
            with col_b:
                constant = st.slider("Constant term", -10, 10, 0)
            
            fig = go.Figure()
            
            # Add tiles for x coefficient
            for i in range(abs(x_coeff)):
                color = "#2563eb" if x_coeff > 0 else "#ef4444"
                x_pos = i if x_coeff > 0 else -i-1
                fig.add_shape(
                    type="rect", 
                    x0=x_pos, y0=0, 
                    x1=x_pos+1, y1=1, 
                    line=dict(color=color, width=2),
                    fillcolor=color
                )
            
            # Add tiles for constant
            for i in range(abs(constant)):
                color = "#10b981" if constant > 0 else "#f59e0b"
                x_pos = i if constant > 0 else -i-1
                fig.add_shape(
                    type="rect", 
                    x0=x_pos, y0=1.2, 
                    x1=x_pos+0.5, y1=1.7, 
                    line=dict(color=color, width=2),
                    fillcolor=color
                )
            
            fig.update_layout(
                title=f"Algebra Tiles: {x_coeff}x + {constant}", 
                xaxis_range=[-12, 12], 
                yaxis_range=[-2, 4],
                template="plotly_dark",
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown(f'<div class="metric-card"><div class="metric-value">{x_coeff}x + {constant}</div><div class="metric-label">Expression</div></div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

def show_historical_context():
    """Historical math context interface"""
    st.markdown('<div class="card-header"><span class="card-icon">📜</span><h2 class="card-title">Historical Math Context</h2></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-header"><h3 class="card-title">Explore History</h3></div>', unsafe_allow_html=True)
        
        historical_topic = st.text_input("Enter a concept or mathematician:", placeholder="e.g., Pythagoras, calculus, Fibonacci")
        
        if st.button("📜 Explore History", disabled=not historical_topic.strip(), use_container_width=True):
            if historical_topic.strip():
                prompt = f"""Provide historical context for the mathematical concept or mathematician '{historical_topic}'. Include:
                1. Key dates and events
                2. Major contributions to mathematics
                3. How this concept/person influenced the development of mathematics
                4. Interesting anecdotes or lesser-known facts"""

                try:
                    historical_context = model.generate_content(prompt)
                    if historical_context and hasattr(historical_context, 'text'):
                        st.session_state.historical_context = historical_context.text
                        
                        # Fun fact section
                        fun_fact_prompt = f"Give an unusual or fun fact about '{historical_topic}' in mathematics."
                        fun_fact = model.generate_content(fun_fact_prompt)
                        if fun_fact and hasattr(fun_fact, 'text'):
                            st.session_state.fun_fact = fun_fact.text
                        
                        display_status_message("success", f"Historical context for '{historical_topic}' loaded!")
                    else:
                        display_status_message("error", "Failed to retrieve historical context. Please try again.")
                except Exception as e:
                    display_status_message("error", f"Error generating historical insights: {str(e)}")
            else:
                display_status_message("warning", "Please enter a topic or mathematician name.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        if hasattr(st.session_state, 'historical_context'):
           # st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown('<div class="card-header"><h3 class="card-title">Historical Insights</h3></div>', unsafe_allow_html=True)
            st.write(st.session_state.historical_context)
            
            if hasattr(st.session_state, 'fun_fact'):
                st.markdown('<div class="card-header" style="margin-top: 2rem;"><h4 class="card-title">🤔 Did You Know?</h4></div>', unsafe_allow_html=True)
                st.write(st.session_state.fun_fact)
            
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="custom-card" style="text-align: center; padding: 3rem;">
                <div style="font-size: 4rem;">📜</div>
                <h3>Historical Explorer Ready!</h3>
                <p>Enter a mathematical concept or mathematician to discover fascinating historical insights.</p>
            </div>
            """, unsafe_allow_html=True)

def show_real_world_applications(skill_level, topic):
    """Real-world applications interface"""
    st.markdown('<div class="card-header"><span class="card-icon">🌍</span><h2 class="card-title">Real-World Applications</h2></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-header"><h3 class="card-title">Application Settings</h3></div>', unsafe_allow_html=True)
        
        application_area = st.selectbox("Choose an application area:", 
            ["Finance", "Physics", "Engineering", "Computer Science", "Biology"], key="application_area")
        
        if st.button("🌍 Generate Scenario", use_container_width=True):
            prompt = f"""Generate a unique and creative real-world scenario demonstrating the application of {topic} in {application_area} for a {skill_level.lower()} level learner. Make it engaging and informative by including:
            
            1. A captivating real-life situation where {topic} plays a crucial role.
            2. The core mathematical principles involved and why they matter.
            3. A step-by-step breakdown of how the math is applied to solve the problem.
            4. Practical takeaways for students or professionals in {application_area}.
            5. A historical or fun fact related to {topic} in {application_area} to make learning interesting."""
            
            scenario = model.generate_content(prompt)
            
            if scenario and hasattr(scenario, 'text'):
                st.session_state.generated_scenario = scenario.text
                st.session_state.selected_application = application_area
                
                # Generate Practice Questions
                question_prompt = f"""Generate three practice questions based on the following real-world scenario:
                {st.session_state.generated_scenario}
                Ensure the questions test the mathematical concepts applied in the scenario."""
                
                questions = model.generate_content(question_prompt)
                
                if questions and hasattr(questions, 'text'):
                    st.session_state.generated_questions = questions.text
                else:
                    st.session_state.generated_questions = "Failed to retrieve practice questions. Please try again."
                
                display_status_message("success", f"Real-world scenario for {topic} in {application_area} generated!")
            else:
                display_status_message("error", "Failed to retrieve the scenario. Please try again.")
        
        if st.button("🔄 Reset Scenario", use_container_width=True):
            if hasattr(st.session_state, 'generated_scenario'):
                del st.session_state.generated_scenario
                del st.session_state.selected_application
                del st.session_state.generated_questions
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        if hasattr(st.session_state, 'generated_scenario'):
          #  st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown('<div class="card-header"><h3 class="card-title">Real-World Scenario</h3></div>', unsafe_allow_html=True)
            st.write(st.session_state.generated_scenario)
            
            # Sample solved question
            st.markdown('<div class="card-header" style="margin-top: 2rem;"><h4 class="card-title">✅ Sample Solution</h4></div>', unsafe_allow_html=True)
            sample_question_prompt = f"""Generate a worked-out example based on the following real-world scenario:
            {st.session_state.generated_scenario}
            Provide a step-by-step solution explaining the mathematical concepts applied."""
            sample_solution = model.generate_content(sample_question_prompt)
            
            if sample_solution and hasattr(sample_solution, 'text'):
                st.write(sample_solution.text)
            
            # Practice questions
            st.markdown('<div class="card-header" style="margin-top: 2rem;"><h4 class="card-title">📝 Practice Questions</h4></div>', unsafe_allow_html=True)
            st.write(st.session_state.generated_questions)
            
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="custom-card" style="text-align: center; padding: 3rem;">
                <div style="font-size: 4rem;">🌍</div>
                <h3>Real-World Explorer Ready!</h3>
                <p>Select an application area and generate scenarios to see math in action!</p>
            </div>
            """, unsafe_allow_html=True)

def show_study_plan_generator(skill_level):
    """Study plan generator interface"""
    st.markdown('<div class="card-header"><span class="card-icon">📊</span><h2 class="card-title">Study Plan Generator</h2></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-header"><h3 class="card-title">Plan Settings</h3></div>', unsafe_allow_html=True)
        
        study_goal = st.text_input("Study Goal:", placeholder="e.g., Master calculus, Prepare for SAT")
        study_time = st.number_input("Hours per week:", min_value=1, max_value=40, value=10)
        
        if st.button("📊 Generate Study Plan", disabled=not study_goal.strip(), use_container_width=True):
            if study_goal.strip():
                prompt = f"""Create a detailed, structured study plan for a {skill_level} level student focusing on {study_goal}. 
                They can dedicate {study_time} hours per week to studying. 
                Provide a well-structured week-by-week breakdown including:
                
                ## 📌 Topics to Cover
                - List the essential topics covered each week, ensuring a logical progression.
                
                ## 📚 Recommended Resources
                - Suggest textbooks, online courses, videos, and practice platforms.
                
                ## ✏ Practice Exercises
                - Include sample problem sets, quizzes, and interactive exercises.
                
                ## 🎯 Milestones & Assessments
                - Define clear checkpoints to measure progress, with mini-tests or self-assessments."""
                
                try:
                    study_plan = model.generate_content(prompt)
                    st.session_state.study_plan = study_plan.text
                    display_status_message("success", f"Study plan for '{study_goal}' generated!")
                except Exception as e:
                    display_status_message("error", f"Error generating study plan: {e}")
            else:
                display_status_message("warning", "Please enter a study goal.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        if hasattr(st.session_state, 'study_plan'):
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown('<div class="card-header"><h3 class="card-title">Your Personalized Study Plan</h3></div>', unsafe_allow_html=True)
            formatted_text = st.session_state.study_plan.replace('Week ', '### Week ')
            st.markdown(formatted_text, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="custom-card" style="text-align: center; padding: 3rem;">
                <div style="font-size: 4rem;">📊</div>
                <h3>Study Plan Generator Ready!</h3>
                <p>Enter your study goal and available time to get a personalized learning plan.</p>
            </div>
            """, unsafe_allow_html=True)

def show_performance_analytics():
    """Performance analytics interface"""
    st.markdown('<div class="card-header"><span class="card-icon">📈</span><h2 class="card-title">Performance Analytics</h2></div>', unsafe_allow_html=True)
    
    progress = get_progress(st.session_state.user)
    
    # Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        topics_completed = len(progress['completed_topics'])
        st.markdown(f'<div class="metric-card"><div class="metric-value">{topics_completed}</div><div class="metric-label">Topics Completed</div></div>', unsafe_allow_html=True)
    
    with col2:
        if progress['quiz_scores']:
            avg_score = sum(progress['quiz_scores'].values()) / len(progress['quiz_scores'])
            st.markdown(f'<div class="metric-card"><div class="metric-value">{avg_score:.1f}%</div><div class="metric-label">Avg Quiz Score</div></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="metric-card"><div class="metric-value">-</div><div class="metric-label">Avg Quiz Score</div></div>', unsafe_allow_html=True)
    
    with col3:
        quiz_count = len(progress['quiz_scores'])
        st.markdown(f'<div class="metric-card"><div class="metric-value">{quiz_count}</div><div class="metric-label">Quizzes Taken</div></div>', unsafe_allow_html=True)
    
    with col4:
        practice_sets = len(progress['practice_sets'])
        st.markdown(f'<div class="metric-card"><div class="metric-value">{practice_sets}</div><div class="metric-label">Practice Sets</div></div>', unsafe_allow_html=True)
    
    # Charts Row
    col1, col2 = st.columns(2)
    
    with col1:
      #  st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-header"><h3 class="card-title">Topic Completion</h3></div>', unsafe_allow_html=True)
        
        if progress['completed_topics']:
            topic_completion = pd.DataFrame({
                'Topic': progress['completed_topics'],
                'Completed': [1] * len(progress['completed_topics'])
            })
            
            fig_completion = px.bar(
                topic_completion, 
                x='Topic', 
                y='Completed', 
                title='Completed Topics',
                color_discrete_sequence=['#2563eb']
            )
            fig_completion.update_layout(
                template="plotly_dark",
                height=400,
                showlegend=False
            )
            st.plotly_chart(fig_completion, use_container_width=True)
        else:
            st.markdown("""
            <div style="text-align: center; padding: 2rem;">
                <div style="font-size: 3rem;">📚</div>
                <p>No completed topics yet. Start solving problems to see your progress!</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
      #  st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-header"><h3 class="card-title">Quiz Performance</h3></div>', unsafe_allow_html=True)
        
        if progress['quiz_scores']:
            quiz_scores = pd.DataFrame({
                'Topic': list(progress['quiz_scores'].keys()),
                'Score': list(progress['quiz_scores'].values())
            })
            
            fig_scores = px.line(
                quiz_scores, 
                x='Topic', 
                y='Score', 
                title='Quiz Scores Trend', 
                markers=True,
                color_discrete_sequence=['#10b981']
            )
            fig_scores.update_layout(
                template="plotly_dark",
                height=400
            )
            st.plotly_chart(fig_scores, use_container_width=True)
            
            # Strengths and weaknesses
            strength_threshold = 70
            weaknesses = quiz_scores[quiz_scores['Score'] < strength_threshold]['Topic'].tolist()
            strengths = quiz_scores[quiz_scores['Score'] >= strength_threshold]['Topic'].tolist()
            
            if strengths:
                st.markdown("**🎯 Strengths:**")
                for strength in strengths:
                    st.markdown(f"✅ {strength}")
            
            if weaknesses:
                st.markdown("**📈 Areas for Improvement:**")
                for weakness in weaknesses:
                    st.markdown(f"📚 {weakness}")
        else:
            st.markdown("""
            <div style="text-align: center; padding: 2rem;">
                <div style="font-size: 3rem;">📊</div>
                <p>No quiz data yet. Take some quizzes to see your performance trends!</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# ================================
# RUN APPLICATION
# ================================

if __name__ == "__main__":
    main()

# Close database connection
conn.close()
