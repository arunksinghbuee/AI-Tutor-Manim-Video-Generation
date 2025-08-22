# 📝 Logging Configuration Guide for Neo AI Tutor

This guide explains how to configure logging levels in your Neo AI Tutor application for different environments and debugging needs.

## 🔧 Logging Levels Available

| Level | Description | Use Case |
|-------|-------------|----------|
| **DEBUG** | Most detailed information | Development and troubleshooting |
| **INFO** | General application flow | Default level, good for monitoring |
| **WARNING** | Non-critical issues | Production monitoring |
| **ERROR** | Critical errors only | Production error tracking |
| **CRITICAL** | System-breaking errors | Emergency situations |

## 🚀 How to Configure Logging Level

### Method 1: Environment Variable (Recommended)

Add the `LOG_LEVEL` variable to your `.env` file:

```env
# Logging Configuration
LOG_LEVEL=DEBUG

# Other environment variables...
OPENROUTER_API_KEY=your_key_here
GOOGLE_GEMINI_API_KEY=your_key_here
```

### Method 2: System Environment Variable

Set the environment variable before running the application:

```bash
# Linux/macOS
export LOG_LEVEL=DEBUG
python3 -m streamlit run MATTHSos.py

# Windows (PowerShell)
$env:LOG_LEVEL="DEBUG"
python -m streamlit run MATTHSos.py

# Windows (Command Prompt)
set LOG_LEVEL=DEBUG
python -m streamlit run MATTHSos.py
```

### Method 3: Docker Environment Variable

If using Docker, add to your `docker run` command:

```bash
docker run -e LOG_LEVEL=DEBUG -p 8501:8501 neo-ai-tutor
```

Or in your `docker-compose.yml`:

```yaml
services:
  neo-ai-tutor:
    environment:
      - LOG_LEVEL=DEBUG
```

## 📊 Logging Level Examples

### DEBUG Level (Most Verbose)
```bash
LOG_LEVEL=DEBUG
```

**What you'll see:**
```
2024-01-15 10:30:15 - NeoAITutor - INFO - Neo AI Tutor Application Starting (Log Level: DEBUG)
2024-01-15 10:30:15 - NeoAITutor - DEBUG - Original script length: 1250 characters
2024-01-15 10:30:15 - NeoAITutor - DEBUG - Script has 45 lines
2024-01-15 10:30:15 - NeoAITutor - DEBUG - Removing boxed wrapper from script
2024-01-15 10:30:15 - NeoAITutor - DEBUG - Adding manim import statement
2024-01-15 10:30:15 - NeoAITutor - INFO - Script cleaned successfully. Final length: 1280 characters
```

### INFO Level (Default)
```bash
LOG_LEVEL=INFO
```

**What you'll see:**
```
2024-01-15 10:30:15 - NeoAITutor - INFO - Neo AI Tutor Application Starting (Log Level: INFO)
2024-01-15 10:30:15 - NeoAITutor - INFO - Loading configuration from environment variables
2024-01-15 10:30:15 - NeoAITutor - INFO - Environment variables loaded from .env file
2024-01-15 10:30:15 - NeoAITutor - INFO - Configuration loaded: app_title=Neo - AI Tutor, layout=wide
2024-01-15 10:30:15 - NeoAITutor - INFO - Script cleaned successfully. Final length: 1280 characters
```

### WARNING Level
```bash
LOG_LEVEL=WARNING
```

**What you'll see:**
```
2024-01-15 10:30:15 - NeoAITutor - WARNING - User 'john' already exists: UNIQUE constraint failed
2024-01-15 10:30:15 - NeoAITutor - WARNING - Failed to configure ElevenLabs client: Invalid API key
```

### ERROR Level (Minimal)
```bash
LOG_LEVEL=ERROR
```

**What you'll see:**
```
2024-01-15 10:30:15 - NeoAITutor - ERROR - Missing OPENROUTER_API_KEY
2024-01-15 10:30:15 - NeoAITutor - ERROR - Error generating Manim video: Command 'manim' not found
```

## 🎯 Recommended Configurations

### Development Environment
```env
LOG_LEVEL=DEBUG
```
- Full debugging information
- API request/response details
- File operation tracking
- Performance metrics

### Testing Environment
```env
LOG_LEVEL=INFO
```
- General application flow
- User actions and errors
- System status updates
- Moderate verbosity

### Production Environment
```env
LOG_LEVEL=WARNING
```
- Only warnings and errors
- Minimal log volume
- Focus on issues that need attention
- Better performance

### Emergency Debugging
```env
LOG_LEVEL=ERROR
```
- Only critical errors
- Minimal log output
- Fastest performance
- Use when investigating specific issues

## 📁 Log File Locations

### Default Location
```
logs/neo_ai_tutor.log
```

### View Logs in Real-Time
```bash
# Follow logs as they're written
tail -f logs/neo_ai_tutor.log

# View last 100 lines
tail -n 100 logs/neo_ai_tutor.log

# Search for specific errors
grep "ERROR" logs/neo_ai_tutor.log

# Search for specific user actions
grep "User.*logged in" logs/neo_ai_tutor.log
```

## 🔍 Debugging with Different Log Levels

### Troubleshooting API Issues
```bash
LOG_LEVEL=DEBUG
```
Look for:
- API request details
- Response content
- Error messages with full context

### Monitoring User Activity
```bash
LOG_LEVEL=INFO
```
Look for:
- Login/logout events
- Problem solving attempts
- Video generation requests

### Production Monitoring
```bash
LOG_LEVEL=WARNING
```
Look for:
- Failed operations
- System warnings
- Performance issues

### Emergency Situations
```bash
LOG_LEVEL=ERROR
```
Look for:
- Critical system failures
- Database connection issues
- File system problems

## ⚡ Performance Impact

| Log Level | Performance Impact | Log File Size |
|-----------|-------------------|---------------|
| DEBUG | High (detailed logging) | Large |
| INFO | Medium (standard logging) | Medium |
| WARNING | Low (minimal logging) | Small |
| ERROR | Very Low (errors only) | Very Small |

## 🛠️ Advanced Configuration

### Custom Log Format
You can modify the log format in `setup_logging()` function:

```python
format='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
```

This adds function name and line number to each log entry.

### Separate Log Files by Level
You can create separate log files for different levels:

```python
# Add to setup_logging() function
debug_handler = logging.FileHandler(log_dir / "debug.log")
debug_handler.setLevel(logging.DEBUG)

error_handler = logging.FileHandler(log_dir / "errors.log")
error_handler.setLevel(logging.ERROR)
```

## 📋 Quick Reference

### Common Commands
```bash
# Set debug level for development
export LOG_LEVEL=DEBUG && python3 -m streamlit run MATTHSos.py

# Set warning level for production
export LOG_LEVEL=WARNING && python3 -m streamlit run MATTHSos.py

# View logs in real-time
tail -f logs/neo_ai_tutor.log

# Search for errors
grep "ERROR" logs/neo_ai_tutor.log | tail -20
```

### Environment Variables
```env
# Development
LOG_LEVEL=DEBUG

# Testing
LOG_LEVEL=INFO

# Production
LOG_LEVEL=WARNING

# Emergency
LOG_LEVEL=ERROR
```

## 🎉 Tips for Effective Logging

1. **Start with DEBUG** when developing new features
2. **Use INFO** for general monitoring
3. **Switch to WARNING** in production
4. **Monitor log file size** and rotate if needed
5. **Search logs regularly** for patterns and issues
6. **Use ERROR level** only when investigating specific problems

Happy debugging! 🐛✨ 