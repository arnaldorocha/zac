# Zac - Personal AI Assistant

Uma assistente pessoal completa que roda localmente no Windows, com controle de voz, automação de navegador, gerenciamento de tarefas, agenda, e integração com Google Sheets.

## 🎯 Funcionalidades

### ✅ Implementadas
- ✨ **Comandos de Voz** - Reconhecimento de fala em português usando Vosk
- 🎤 **Síntese de Voz** - Resposta áudio usando pyttsx3
- 🌐 **Automação de Navegador** - Controle do Chrome via Playwright
- 📝 **Gerenciamento de Tarefas** - Criar, atualizar, concluir tarefas (SQLite)
- 📅 **Agenda** - Criar compromissos, consultar eventos (SQLite)
- 💾 **Memória Pessoal** - Salvar pessoas, metas, preferências (SQLite)
- 📊 **Integração Google Sheets** - Registrar gastos, estudos, metas
- 🔄 **Scheduler** - Executar tarefas programadas automaticamente
- 🚀 **API REST** - Controlar via FastAPI/Uvicorn
- 📦 **Modular e Escalável** - Arquitetura preparada para futuras integrações

### 🔮 Preparado para Futuro
- LLMService (Ollama, Qwen, Gemma, Llama)
- VisionService (visão computacional)
- AgentService (múltiplos agentes especializados)
- PluginService (extensões customizadas)
- RAG (Retrieval Augmented Generation)
- Dashboard web
- Aplicativo Android

## 📋 Pré-requisitos

- **Windows 10/11**
- **Python 3.12+** ([Download](https://www.python.org/downloads/))
- **Google Chrome** (para automação de navegador)

## 🚀 Instalação

### 1. Clonar ou Descarregar Projeto

```bash
cd zac
```

### 2. Criar Ambiente Virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Ou usar conda
conda create -n zac python=3.12
conda activate zac
```

### 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 4. Instalar PlayWright (Browser Automation)

```bash
playwright install chromium
```

### 5. (OPCIONAL) Configurar Google Sheets

Para integração com Google Sheets:

1. Acesse [Google Cloud Console](https://console.cloud.google.com)
2. Crie um novo projeto
3. Ative a API Google Sheets
4. Crie uma conta de serviço
5. Baixe o arquivo `credentials.json`
6. Copie para a raiz do projeto como `credentials.json`

```bash
# Teste a conexão
python -c "from sheets.google_sheets_service import GoogleSheetsService; s = GoogleSheetsService(); print('OK')"
```

## 📖 Como Usar

### Modo Interativo (Recomendado para Início)

```bash
python main.py
```

Você verá o menu:
```
Zac> help
```

Comandos disponíveis:

#### Tarefas
```
Zac> adicionar tarefa estudar álgebra linear
Zac> quais são minhas tarefas
Zac> concluir tarefa álgebra
```

#### Agenda
```
Zac> adicionar compromisso reunião com João amanhã às 14:00
Zac> qual é minha agenda
```

#### Navegador
```
Zac> abrir chrome
Zac> navegar para google.com
```

#### Google Sheets
```
Zac> registrar gasto de 50 reais com alimentação
Zac> registrar estudo de inglês por 2 horas
```

#### Memória
```
Zac> lembrar que João é meu colega de trabalho
```

#### Reconhecimento de Voz
```
Zac> listen
```
Então fale seu comando naturalmente em português.

### API REST

Para controlar via API:

```bash
# Terminal 1 - Iniciar servidor
python -m uvicorn api.server:app --host 127.0.0.1 --port 8000

# Terminal 2 - Usar API
curl http://127.0.0.1:8000/health

# Ou usar Python
import requests

# Criar tarefa
resp = requests.post("http://127.0.0.1:8000/tasks", json={
    "title": "Estudar Python",
    "priority": "high"
})
print(resp.json())

# Executar comando
resp = requests.post("http://127.0.0.1:8000/command", json={
    "text": "abrir chrome"
})
print(resp.json())
```

### Testes

```bash
# Executar testes
python -m pytest tests/ -v

# Ou dentro do programa
Zac> test
```

## 📁 Arquitetura

```
zac/
├── core/                          # Núcleo
│   ├── assistant.py               # Orquestrador principal
│   ├── command_router.py          # Parser de comandos
│   ├── scheduler.py               # Agendador de tarefas
│   └── memory_manager.py          # Gerenciador de memória (futura expansão)
│
├── voice/                         # Entrada/Saída de Voz
│   ├── speech_to_text.py         # Vosk (reconhecimento)
│   └── text_to_speech.py         # pyttsx3 (síntese)
│
├── browser/                       # Automação Web
│   └── browser_service.py        # Playwright (browser control)
│
├── sheets/                        # Integração Cloud
│   └── google_sheets_service.py  # pygsheets API (sem custo)
│
├── tasks/                         # Gerenciamento
│   └── task_service.py           # Serviço de tarefas
│
├── calendar/                      # Agenda
│   └── calendar_service.py       # Serviço de eventos
│
├── memory/                        # Conhecimento
│   └── memory_service.py         # Serviço de memória
│
├── database/                      # Persistência
│   ├── models.py                 # Modelos de dados
│   └── sqlite_manager.py         # Gerenciador SQLite
│
├── api/                           # Interface REST
│   └── server.py                 # FastAPI server
│
├── logs/                          # Logs de execução
│   └── zac.log
│
├── tests/                         # Testes
│   ├── test_basic.py            # Testes básicos
│   └── test_services.py         # Testes de serviços
│
├── main.py                        # Entrada principal
├── requirements.txt               # Dependências
└── README.md                      # Esta documentação
```

## 🏗️ Arquitetura Técnica

### Principles (SOLID)

- **Single Responsibility**: Cada serviço tem uma responsabilidade
- **Open/Closed**: Extensível para novos serviços sem alterar existentes
- **Liskov Substitution**: Interfaces bem definidas entre camadas
- **Interface Segregation**: Cada componente expõe apenas o necessário
- **Dependency Inversion**: Dependências injetadas, não hardcoded

### Type Hints

Todo código utiliza type hints para melhor legibilidade e IDE support:

```python
def create_task(
    self,
    title: str,
    priority: TaskPriority = TaskPriority.MEDIUM,
    due_date: Optional[datetime] = None
) -> Task:
    ...
```

### Tratamento de Erros

Erros tratados em cada camada com logging estruturado:

```python
try:
    # operação
except SpecificError as e:
    logger.error(f"Specific error: {e}")
    return None  # ou raise de novo
```

### Logging Estruturado

```python
import logging
logger = logging.getLogger(__name__)
logger.info("Informação")
logger.warning("Aviso")
logger.error("Erro")
```

## 🔧 Extensões Futuras

### 1. Integração com LLM Local

```python
# Implementação futura
from core.interfaces import LLMService

class OllamaService(LLMService):
    def generate_response(self, prompt: str) -> str:
        # Usar Ollama localmente
        pass
```

### 2. Visão Computacional

```python
from core.interfaces import VisionService

class OpenCVService(VisionService):
    def detect_objects(self, image_path: str) -> List[Object]:
        pass
```

### 3. Multi-Agent System

```python
from core.interfaces import AgentService

class SpecializedAgent(AgentService):
    def execute(self, task: Task) -> Result:
        pass
```

## 📚 Exemplos de Uso

### Exemplo 1: Adicionar Tarefa Programada

```python
from core.assistant import ZacAssistant
from datetime import datetime, timedelta

assistant = ZacAssistant()

# Criar tarefa
task = assistant.tasks.create_task(
    title="Estudar Machine Learning",
    priority=TaskPriority.HIGH,
    due_date=datetime.now() + timedelta(days=7)
)

# Programar lembrete
def remind():
    assistant.tts.speak("Lembre-se de estudar Machine Learning")

assistant.scheduler.schedule_at_time(
    task_id="study_reminder",
    callback=remind,
    hour=19,
    minute=0
)
```

### Exemplo 2: Automatizar Registro de Gastos

```python
# Registrar gasto automaticamente em Google Sheets
assistant.process_command("registrar gasto de 50 reais com alimentação")

# No Google Sheets, linha adicionada automaticamente:
# | Data       | Categoria   | Descrição  | Valor |
# | 04/06/2024 | Alimentação | -          | 50    |
```

### Exemplo 3: Controlar Navegador

```python
# Abrir Chrome
assistant.browser.open_browser()

# Navegar
assistant.browser.navigate("https://github.com")

# Buscar elemento
exists = assistant.browser.element_exists(".search-input")

# Clicar e preencher
assistant.browser.click(".search-input")
assistant.browser.type_text(".search-input", "python")

# Screenshot
assistant.browser.take_screenshot("screenshot.png")
```

## 🔌 Integração com Terceiros

### Via API REST

```bash
# Health check
curl http://localhost:8000/health

# Listar tarefas
curl http://localhost:8000/tasks

# Criar tarefa
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Nova tarefa","priority":"high"}'

# Executar comando
curl -X POST http://localhost:8000/command \
  -H "Content-Type: application/json" \
  -d '{"text":"abrir chrome"}'
```

### Via Python

```python
from core.assistant import ZacAssistant

# Usar como library
assistant = ZacAssistant()

# Processar comando
result = assistant.process_command("quais são minhas tarefas")

# Acessar serviços diretamente
tasks = assistant.tasks.get_today_tasks()
events = assistant.calendar.get_upcoming_events(days=7)
```

## 🐛 Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'vosk'"

```bash
pip install vosk
# Se ainda não funcionar:
pip install --upgrade vosk pyaudio
```

### Erro: "Playwright not installed"

```bash
playwright install chromium
```

### Erro de Microphone

```bash
# Verifique se há microfone disponível
python -c "import pyaudio; p = pyaudio.PyAudio(); print(p.get_default_input_device_info())"

# Se necessário, instale drivers de áudio
```

### Google Sheets não conecta

1. Verifique se `credentials.json` existe na raiz
2. Verifique permissões do arquivo
3. Teste: `python -c "from sheets.google_sheets_service import GoogleSheetsService; s = GoogleSheetsService(); print(s.client)"`

## 📊 Status do Projeto

| Componente | Status | Versão |
|------------|--------|---------|
| Voice I/O | ✅ Completo | 1.0 |
| Tasks | ✅ Completo | 1.0 |
| Calendar | ✅ Completo | 1.0 |
| Browser | ✅ Completo | 1.0 |
| Sheets | ✅ Completo | 1.0 |
| Memory | ✅ Completo | 1.0 |
| Scheduler | ✅ Completo | 1.0 |
| API REST | ✅ Completo | 1.0 |
| LLM Integration | 🔄 Planejado | 2.0 |
| Vision | 🔄 Planejado | 2.0 |
| Dashboard Web | 🔄 Planejado | 2.0 |

## 📝 Licença

MIT License - Sinta-se livre para usar, modificar e distribuir.

## 🤝 Contribuições

Contribuições são bem-vindas! Por favor:

1. Faça um fork
2. Crie uma branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📞 Suporte

- 📧 Email: support@zac.local
- 🐛 Issues: [GitHub Issues](https://github.com/seu-usuario/zac/issues)
- 💬 Discussões: [GitHub Discussions](https://github.com/seu-usuario/zac/discussions)

## 🚀 Performance e Otimizações

- Scheduler roda em thread separada (não bloqueia UI)
- Database caching para consultas frequentes
- Lazy loading de módulos pesados
- Async/await pronto para futuras expansões

## 📈 Roadmap

### v1.0 (Atual)
- [x] Core functionality
- [x] Voice control (pt-br)
- [x] Task management
- [x] Calendar
- [x] Browser automation
- [x] Google Sheets integration
- [x] REST API

### v1.1
- [ ] Melhorias de NLP
- [ ] Suporte a múltiplos idiomas
- [ ] Dashboard web básico
- [ ] Modo daemon/serviço Windows

### v2.0
- [ ] Integração Ollama (LLM local)
- [ ] Vision (visão computacional)
- [ ] Multi-agent system
- [ ] Plugin system
- [ ] RAG (memória vetorial)

### v3.0
- [ ] Aplicativo Android
- [ ] Sincronização em nuvem
- [ ] Backup automático
- [ ] Reconhecimento facial

---

**Zac** - Seu Assistente Pessoal Inteligente, 100% Local e Gratuito 🚀
