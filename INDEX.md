# 📚 Zac Documentation Index

Quick navigation for all documentation and guides.

## 🚀 Getting Started

| Document | Purpose |
|----------|---------|
| [QUICKSTART.md](QUICKSTART.md) | **Start here** - 5-minute setup guide |
| [README.md](README.md) | Complete documentation and features |
| [install.bat](install.bat) | Automated Windows installation |

## 📖 Detailed Guides

| Document | Topic |
|----------|-------|
| [API.md](API.md) | REST API endpoints and usage examples |
| [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | Common issues and solutions |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Guidelines for contributing |
| [CHANGELOG.md](CHANGELOG.md) | Version history and roadmap |

## 📁 Project Structure

```
zac/
├── core/
│   ├── assistant.py           # Main orchestrator
│   ├── command_router.py      # Voice command parser
│   ├── scheduler.py           # Task scheduler
│   ├── interfaces.py          # Future extensions
│   └── __init__.py
│
├── voice/                      # Voice I/O
│   ├── speech_to_text.py      # Vosk speech recognition
│   ├── text_to_speech.py      # pyttsx3 voice synthesis
│   └── __init__.py
│
├── browser/                    # Browser automation
│   ├── browser_service.py     # Playwright wrapper
│   └── __init__.py
│
├── sheets/                     # Google Sheets integration
│   ├── google_sheets_service.py
│   └── __init__.py
│
├── tasks/                      # Task management
│   ├── task_service.py
│   └── __init__.py
│
├── calendar/                   # Calendar/Events
│   ├── calendar_service.py
│   └── __init__.py
│
├── memory/                     # Memory/Knowledge
│   ├── memory_service.py
│   └── __init__.py
│
├── database/                   # Data persistence
│   ├── models.py              # Data models
│   ├── sqlite_manager.py      # SQLite operations
│   └── __init__.py
│
├── api/                        # REST API
│   ├── server.py              # FastAPI server
│   └── __init__.py
│
├── tests/                      # Test suite
│   ├── test_basic.py
│   ├── test_services.py
│   └── __init__.py
│
├── main.py                     # Entry point
├── config.py                   # Configuration loader
├── setup.py                    # Package setup
├── requirements.txt            # Python dependencies
├── .env.example               # Environment template
├── .gitignore                 # Git ignore rules
└── conftest.py                # Pytest configuration
```

## 💻 Quick Commands

### Setup
```bash
.\install.bat              # Windows automatic setup
# or
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Run
```bash
python main.py             # Interactive mode
python -m pytest tests/ -v # Run tests
python -m uvicorn api.server:app --reload  # API server
```

### Development
```bash
black .                    # Format code
flake8 .                   # Lint
mypy .                     # Type check
```

## 🎯 Common Tasks

### Add a Task
```
Zac> adicionar tarefa estudar Python
```

### Check Tasks
```
Zac> quais são minhas tarefas
```

### Open Browser
```
Zac> abrir chrome
```

### Use API
```bash
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Nova tarefa","priority":"high"}'
```

### Listen for Voice
```
Zac> listen
# Then speak: "adicionar tarefa estudar"
```

## 🔑 Key Features

✅ **Voice Control** - Speak Portuguese commands
✅ **Task Management** - Create, update, complete tasks
✅ **Calendar** - Schedule events and reminders
✅ **Browser Automation** - Control web browsers
✅ **Google Sheets** - Read/write spreadsheets
✅ **Memory** - Store personal knowledge
✅ **Local** - Everything runs on your computer
✅ **Free** - No paid APIs or subscriptions
✅ **Modular** - Clean, extensible code
✅ **API** - REST interface for integration

## 🆘 Help Resources

| Issue | Solution |
|-------|----------|
| Installation fails | See [TROUBLESHOOTING.md](TROUBLESHOOTING.md#installation-issues) |
| Microphone not working | See [TROUBLESHOOTING.md](TROUBLESHOOTING.md#voice-recognition-issues) |
| Command not recognized | See [TROUBLESHOOTING.md](TROUBLESHOOTING.md#command-recognition-issues) |
| API connection error | See [TROUBLESHOOTING.md](TROUBLESHOOTING.md#api-server-issues) |
| Want to contribute | See [CONTRIBUTING.md](CONTRIBUTING.md) |

## 📊 Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Language | Python 3.12 | Core development |
| Voice In | Vosk | Speech recognition |
| Voice Out | pyttsx3 | Speech synthesis |
| Browser | Playwright | Web automation |
| Sheets | pygsheets | Google Sheets API |
| Database | SQLite | Local storage |
| API | FastAPI | REST endpoints |
| Testing | Pytest | Quality assurance |

## 🗺️ Development Roadmap

### ✅ v1.0 (Current)
- Voice control
- Task management
- Calendar
- Browser automation
- Google Sheets integration
- REST API

### 🔄 v1.1 (Planned)
- Multi-language support
- Dashboard web interface
- Windows service
- NLP improvements

### 🚀 v2.0 (Future)
- LLM integration (Ollama)
- Computer Vision
- Multi-agent system
- Plugin architecture

### 📱 v3.0 (Future)
- Android app
- Cloud sync
- Facial recognition
- Advanced analytics

## 📞 Support

- **Documentation**: This index and linked guides
- **Issues**: [GitHub Issues](https://github.com/yourusername/zac/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/zac/discussions)
- **Email**: support@zac.local

## 📝 License

MIT License - Free for personal and commercial use.

---

## 🎓 Learning Resources

### For Users
1. Read [QUICKSTART.md](QUICKSTART.md) - 5 min
2. Try basic commands in main.py - 10 min
3. Explore voice commands - 5 min
4. Read [README.md](README.md) for details - 20 min

### For Developers
1. Review [CONTRIBUTING.md](CONTRIBUTING.md)
2. Study project structure above
3. Review [core/assistant.py](core/assistant.py)
4. Read through test files
5. Check [API.md](API.md) for endpoints

### For Integrators
1. Read [API.md](API.md)
2. Try example requests
3. Run API server
4. Integrate with your application

---

**Start with [QUICKSTART.md](QUICKSTART.md) → Success! 🚀**
