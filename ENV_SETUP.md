# Environment Variables Setup for Neo AI Tutor

This document explains how to configure the environment variables for the MATTHSos.py application.

## 📁 Creating the .env File

Create a `.env` file in the root directory of the project with the following variables:

```env
# API Keys for Neo AI Tutor
OPENROUTER_API_KEY=your_openrouter_api_key_here
GOOGLE_GEMINI_API_KEY=your_google_gemini_api_key_here
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here

# Application Configuration
APP_TITLE=Neo - AI Tutor
APP_LAYOUT=wide
SIDEBAR_STATE=expanded

# Database Configuration
DATABASE_NAME=math_tutor.db

# Video Generation Settings
MANIM_QUALITY=ql
VIDEO_FPS=15
VIDEO_RESOLUTION=480p

# Audio Settings
AUDIO_LANGUAGE=en
AUDIO_OUTPUT_FORMAT=mp3

# Security Settings
PASSWORD_HASH_ALGORITHM=sha256
```

## 🔑 Required API Keys

### 1. OPENROUTER_API_KEY
- **Required**: Yes
- **Description**: API key for OpenRouter service (used for GPT-4o-mini and Qwen3-Coder)
- **How to get**: Sign up at [OpenRouter](https://openrouter.ai/) and generate an API key

### 2. GOOGLE_GEMINI_API_KEY
- **Required**: Yes
- **Description**: API key for Google Gemini 2.5 Pro
- **How to get**: 
  1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
  2. Create a new API key
  3. Copy the key to your .env file

### 3. ELEVENLABS_API_KEY
- **Required**: No (optional)
- **Description**: API key for ElevenLabs text-to-speech service
- **How to get**: Sign up at [ElevenLabs](https://elevenlabs.io/) and generate an API key

## ⚙️ Configuration Options

### Application Settings
- `APP_TITLE`: The title displayed in the browser tab
- `APP_LAYOUT`: Streamlit layout mode ("wide" or "centered")
- `SIDEBAR_STATE`: Initial sidebar state ("expanded" or "collapsed")

### Database Settings
- `DATABASE_NAME`: SQLite database filename

### Video Generation Settings
- `MANIM_QUALITY`: Manim rendering quality ("ql" for quick, "l" for low, "m" for medium, "h" for high)
- `VIDEO_FPS`: Video frames per second
- `VIDEO_RESOLUTION`: Video resolution (e.g., "480p", "720p", "1080p")

### Audio Settings
- `AUDIO_LANGUAGE`: Language code for text-to-speech (e.g., "en", "es", "fr")
- `AUDIO_OUTPUT_FORMAT`: Audio file format ("mp3", "wav", etc.)

### Security Settings
- `PASSWORD_HASH_ALGORITHM`: Hashing algorithm for passwords ("sha256", "sha1", "md5")

## 🚀 Getting Started

1. **Copy the example**: Copy the environment variables above
2. **Create .env file**: Create a new file named `.env` in the project root
3. **Add your keys**: Replace the placeholder values with your actual API keys
4. **Save the file**: Make sure the file is saved in the project root directory
5. **Run the application**: The app will automatically load the environment variables

## 🔒 Security Notes

- **Never commit your .env file** to version control
- **Keep your API keys secure** and don't share them
- **Use different keys** for development and production
- **Rotate your keys** regularly for security

## 🐛 Troubleshooting

### Common Issues

1. **"Missing required API keys" error**
   - Check that your .env file exists in the project root
   - Verify that OPENROUTER_API_KEY and GOOGLE_GEMINI_API_KEY are set
   - Ensure there are no extra spaces or quotes around the values

2. **API key not working**
   - Verify your API keys are valid and active
   - Check your account balance/quotas
   - Ensure you have the correct permissions

3. **Environment variables not loading**
   - Make sure python-dotenv is installed: `pip install python-dotenv`
   - Check that the .env file is in the correct location
   - Restart your application after making changes

### Example .env File

```env
# API Keys (replace with your actual keys)
OPENROUTER_API_KEY=sk-or-v1-your-actual-key-here
GOOGLE_GEMINI_API_KEY=AIza-your-actual-key-here
ELEVENLABS_API_KEY=your-elevenlabs-key-here

# Application Settings
APP_TITLE=Neo - AI Tutor
APP_LAYOUT=wide
SIDEBAR_STATE=expanded

# Database Configuration
DATABASE_NAME=math_tutor.db

# Video Generation Settings
MANIM_QUALITY=ql
VIDEO_FPS=15
VIDEO_RESOLUTION=480p

# Audio Settings
AUDIO_LANGUAGE=en
AUDIO_OUTPUT_FORMAT=mp3

# Security Settings
PASSWORD_HASH_ALGORITHM=sha256
```

## 📝 Notes

- The application will automatically validate required API keys on startup
- Missing optional keys will not prevent the application from running
- Configuration changes require restarting the application
- Default values are provided for all optional settings 