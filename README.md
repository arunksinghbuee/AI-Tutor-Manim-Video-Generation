# 🧮 Neo — AI Tutor with Animated Explanations

Neo is an advanced AI-powered chatbot tutor built with **Python** and **Streamlit** that not only solves math problems but also visually explains them using **Manim** animations and voice narration. Designed for students, educators, and visual learners, this tool combines the power of conversational AI with interactive, video-based learning.

---
## 🚀 Features

### 🔍 AI-Powered Problem Solver
- Accepts **text or image-based problems**.
- Uses a **multi-agent GPT architecture** (Gemini, DeepSeek, GPT-4) to:
  - Understand and validate the problem
  - Generate step-by-step explanations
  - Output LaTeX-ready expressions for animation

### 🖼️ Image-to-Math (OCR)
- Upload handwritten or printed math problems as images
- Uses **Tesseract OCR + PIL** to extract the problem as text
- Feeds it directly to the AI pipeline for solution and animation

### 🎥 Highlight Feature: Animated Video Generation (with Manim)
> This is the core innovation of the project.

- Converts math explanations into **educational animations**
- Auto-generates Python files using the [Manim](https://www.manim.community/) library
- Renders:
  - Expressions step-by-step
  - Graphs, integrals, transformations
  - Visual breakdown of the solution
- Output is a **.mp4 animation** ready for viewing or download
- All animations are created dynamically per user input

### 🎙️ Voice Narration
- Uses **gTTS** or **ElevenLabs** to:
  - Convert the explanation text into voice
  - Synchronize narration with Manim visuals
  - Merge audio with animation to enhance learning for **auditory learners**

### 📊 Interactive & Responsive UI
- Built with **Streamlit**, enabling:
  - Sidebar navigation for different modules (solve, quiz, explore)
  - Upload sections for images
  - Embedded video players for animations
  - Live feedback and spinner status during generation

### 📈 Performance Tracking & Quizzes
- Track user performance over quizzes and practice sets
- Store scores and visualize metrics using **Plotly**
- Adaptive learning logic: suggests follow-up problems based on errors

### 🧾 Exportable PDF Reports
- Generate detailed **PDF documents** of solved problems
- Includes question, step-by-step explanation, and final answer
- Powered by **ReportLab** for structured and readable reports

### 🧠 Conceptual Math Explorer
- Type a topic like "integration by parts" or "matrix rank"
- Receive:
  - Definitions and use cases
  - Common misconceptions
  - Real-world applications

### 📁 Auto File Management
- Automatically organizes:
  - Input problems
  - Generated Python scripts (`MathExplanation_*.py`)
  - Animation files (`.mp4`)
  - Audio narration files (`.mp3`)
- Cleans up temporary files to keep the environment efficient

---

## 📦 Tech Stack

| Layer            | Technology Used                  |
|------------------|----------------------------------|
| Frontend UI      | Streamlit                        |
| Core Logic       | Python, OpenAI, Gemini, DeepSeek |
| Animation        | Manim Community Edition          |
| Narration        | gTTS, ElevenLabs (optional)      |
| Image Processing | Tesseract OCR, Pillow            |
| Audio-Video Sync | moviepy                          |
| Reports & Files  | ReportLab, os, shutil            |
| Storage          | SQLite3                          |
| Data Viz         | Plotly, pandas, numpy            |

---

## 📁 Project Structure

- **.**
- **├── MATTHSos.py                       # Main Streamlit application**
- **├── MathExplanation_*.py              # Auto-generated Manim scripts**
- **├── IntegrationAnimation/             # Output animation files (.mp4)**
- **├── requirements.txt                  # Python dependencies**
- **├── .gitignore**
- **└── README.md**

---

## ✨ Future Enhancements

- Support for multiple languages
- Real-time collaboration
  
---

## 🙌 Acknowledgements

- Streamlit
- Manim Community
- OpenAI
- Gemini
- ReportLab
- Pytesseract
- SQLite

---

## 📬 Contact

Reach out: [LinkedIn](https://www.linkedin.com/in/joshua-ranish-t-1065822b9) | [GitHub](https://github.com/Joshua-Ranish-T)
