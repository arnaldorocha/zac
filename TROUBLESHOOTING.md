# 🔧 Zac Troubleshooting Guide

## Common Issues and Solutions

### Installation Issues

#### Problem: "Python not found"
**Solution:**
1. Install Python 3.12+ from https://python.org
2. Make sure to check "Add Python to PATH"
3. Restart terminal and try again

```bash
python --version  # Should be 3.12+
```

#### Problem: "ModuleNotFoundError: No module named 'vosk'"
**Solution:**
```bash
# Ensure virtual environment is activated
venv\Scripts\activate

# Install vosk and dependencies
pip install vosk pyaudio
```

#### Problem: "pip: command not found"
**Solution:**
```bash
# Use Python module directly
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

#### Problem: Permission denied / "Access is denied"
**Solution:**
1. Run PowerShell as Administrator
2. Or use the installation script
3. Check file permissions in folder properties

### Voice Recognition Issues

#### Problem: Microphone not working
**Solution:**
1. Check system sound settings
2. Test microphone: `python -c "import pyaudio; p = pyaudio.PyAudio(); print(p.get_default_input_device_info())"`
3. Update audio drivers
4. Restart Windows

#### Problem: Vosk language model not found
**Solution:**
```bash
# Vosk uses pre-trained models
# If error, manually download model for your language:

# For Portuguese (Brazil):
mkdir -p %APPDATA%\vosk
# Download from: https://alphacephei.com/vosk/models
# Extract to %APPDATA%\vosk\
```

#### Problem: "No module named 'vosk.Model'"
**Solution:**
```bash
# Uninstall and reinstall
pip uninstall vosk -y
pip install vosk

# Or use conda
conda install vosk
```

### Browser Automation Issues

#### Problem: "Playwright not installed"
**Solution:**
```bash
# Install browsers
playwright install chromium

# If that fails, try:
python -m playwright install chromium
```

#### Problem: Chrome/Chromium not found
**Solution:**
```bash
# Reinstall browser
playwright install chromium --reinstall

# Or specify Chrome path manually
from browser.browser_service import BrowserAutomationService
browser = BrowserAutomationService()
# Then set path in code
```

#### Problem: "Browser window doesn't respond"
**Solution:**
1. Close any existing Zac processes
2. Restart the application
3. Check system resources (CPU/Memory)

### Database Issues

#### Problem: "Database is locked"
**Solution:**
1. Close all Zac instances
2. Wait 10 seconds
3. Delete `zac.db` if corrupted
4. Restart

#### Problem: "No module named 'sqlite3'"
**Solution:**
```bash
# SQLite is built-in with Python
# If missing, reinstall Python

# Or on Linux:
sudo apt-get install python3-sqlite3
```

### Google Sheets Issues

#### Problem: "401 Unauthorized / Invalid credentials"
**Solution:**
1. Check if `credentials.json` exists in project root
2. Verify file isn't corrupted
3. Generate new credentials:
   - Go to https://console.cloud.google.com
   - Create new service account
   - Download JSON
   - Replace old `credentials.json`

#### Problem: "Sheet not found"
**Solution:**
1. Check spreadsheet ID is correct
2. Verify account has access to sheet
3. Sheet must be shared with service account email

#### Problem: API quota exceeded
**Solution:**
- Google Sheets API is free
- Quotas: 300 requests/minute
- Wait 60 seconds and retry
- Or implement caching

### API Server Issues

#### Problem: "Address already in use"
**Solution:**
```bash
# Port 8000 is already in use
# Option 1: Stop other process
# Option 2: Use different port
python -m uvicorn api.server:app --port 8001
```

#### Problem: "ConnectionRefusedError"
**Solution:**
1. Make sure API server is running
2. Check if running on correct host:port
3. Try: `http://127.0.0.1:8000/health`

#### Problem: CORS errors
**Solution:**
```bash
# For development, add to api/server.py:
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Text-to-Speech Issues

#### Problem: "No sound / pyttsx3 not working"
**Solution:**
```bash
# Reinstall pyttsx3
pip install --upgrade pyttsx3

# Check available voices
python -c "import pyttsx3; e = pyttsx3.init(); print(e.getProperty('voices'))"
```

#### Problem: "Wrong language / voice not found"
**Solution:**
```bash
# Edit voice/text_to_speech.py
# Manually set voice to available one
```

### Performance Issues

#### Problem: "Slow response / commands take long"
**Solution:**
1. Check CPU/RAM usage (Task Manager)
2. Close other applications
3. Check database size (`du data/zac.db`)
4. Run cleanup: delete old records
5. Check network (if using Google Sheets)

#### Problem: "Memory usage keeps increasing"
**Solution:**
1. Restart application periodically
2. Clear old logs: `del logs\*.log`
3. Commit to database properly
4. Close browser after automation

### Environment / Configuration Issues

#### Problem: ".env file not being read"
**Solution:**
1. Check if `.env` exists in project root
2. Must be named `.env` (not `.env.txt`)
3. Restart application
4. Manually set variables:

```python
import os
os.environ['VOICE_LANGUAGE'] = 'pt-br'
```

#### Problem: Wrong configuration loading
**Solution:**
1. Check `.env` syntax (no quotes around values)
2. Restart application
3. Manually check: `python -c "from config import Config; print(Config)"`

### Command Recognition Issues

#### Problem: "Command not recognized"
**Solution:**
1. Check exact wording matches examples
2. Prefix with "Zac" or "Jarvis"
3. Use Portuguese for Portuguese language
4. Check logs for what was recognized

#### Problem: "Listen timeout / voice not detected"
**Solution:**
1. Speak clearly and loud enough
2. Reduce background noise
3. Check microphone is selected
4. Increase timeout in code

### Testing Issues

#### Problem: "Tests fail with 'ModuleNotFoundError'"
**Solution:**
```bash
# Run from project root
cd /path/to/zac
python -m pytest tests/ -v

# Or activate environment first
venv\Scripts\activate
pytest tests/ -v
```

#### Problem: "Test database already exists"
**Solution:**
```bash
# Delete test database
del test_zac.db
del test_zac_services.db

# Then rerun tests
pytest tests/ -v
```

---

## Debug Mode

Enable debug logging:

```bash
# Set environment variable
set LOG_LEVEL=DEBUG
python main.py

# Or in code:
import logging
logging.basicConfig(level=logging.DEBUG)
```

Check logs:
```bash
# View recent logs
type logs\zac.log

# Or use tail
tail -f logs\zac.log
```

---

## Getting Help

1. **Check this guide** - Most common issues covered
2. **Check README.md** - General documentation
3. **Check logs** - Usually at `logs/zac.log`
4. **Check issues** - https://github.com/yourusername/zac/issues
5. **Ask community** - Discussions section

---

## System Requirements Check

Run this to verify your system:

```bash
python -c "
import sys
import platform
print(f'Python: {sys.version}')
print(f'OS: {platform.system()} {platform.release()}')
print(f'Processor: {platform.processor()}')

try:
    import vosk
    print('✓ Vosk installed')
except:
    print('✗ Vosk missing')

try:
    import playwright
    print('✓ Playwright installed')
except:
    print('✗ Playwright missing')

try:
    import pyttsx3
    print('✓ pyttsx3 installed')
except:
    print('✗ pyttsx3 missing')

try:
    import pyaudio
    print('✓ PyAudio installed')
except:
    print('✗ PyAudio missing')
"
```

---

## Still Having Issues?

1. **Collect information:**
   - What OS/version?
   - What Python version?
   - What's the error message?
   - What were you trying to do?
   - What's in the logs?

2. **Create GitHub issue** with:
   - Clear title
   - Steps to reproduce
   - Error message
   - System information
   - Log excerpts

3. **Ask for help:**
   - Discussions section
   - Stack Overflow tags: python, vosk, playwright
   - Community forums

---

**Remember: Most issues are easily solvable!** 💪
