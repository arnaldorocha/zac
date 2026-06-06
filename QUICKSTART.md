# 🚀 Zac - Quick Start Guide

## 1️⃣ Instalação Rápida (2 minutos)

### Opção A: Script Automático (Recomendado)
```bash
# No PowerShell/CMD na pasta do projeto
.\install.bat
```

### Opção B: Manual
```bash
# Criar ambiente virtual
python -m venv venv
venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Instalar Playwright
playwright install chromium
```

## 2️⃣ Primeiro Uso

```bash
# Ativar ambiente (se não estiver)
venv\Scripts\activate

# Executar
python main.py

# Você verá:
# Zac> 
```

## 3️⃣ Seus Primeiros Comandos

Digite direto no terminal:

```
Zac> help                                    # Ver todos os comandos

Zac> adicionar tarefa estudar Python         # Criar tarefa
Zac> quais são minhas tarefas               # Listar tarefas

Zac> adicionar compromisso almoço amanhã     # Criar evento
Zac> qual é minha agenda                     # Ver agenda

Zac> abrir chrome                            # Abrir navegador
Zac> navegar para google.com                 # Ir para site

Zac> lembrar que João é meu colega          # Salvar na memória

Zac> listen                                  # Falar um comando

Zac> quit                                    # Sair
```

## 4️⃣ API REST (Opcional)

```bash
# Terminal 1
python -m uvicorn api.server:app --reload

# Terminal 2 (Python)
import requests

# Criar tarefa
r = requests.post("http://localhost:8000/tasks", 
    json={"title": "Estudar", "priority": "high"})
print(r.json())

# Ver tarefas
r = requests.get("http://localhost:8000/tasks")
print(r.json())
```

## 5️⃣ Testes

```bash
# Rodar testes
python -m pytest tests/ -v

# Ou no programa
Zac> test
```

## 6️⃣ Configuração Google Sheets (Opcional)

1. Acesse https://console.cloud.google.com
2. Crie novo projeto
3. Ative Google Sheets API
4. Crie conta de serviço → baixar JSON
5. Copie JSON como `credentials.json` na pasta raiz

```bash
# Testar
python -c "from sheets.google_sheets_service import GoogleSheetsService; s = GoogleSheetsService()"
```

## 📱 Modo Voz

```bash
Zac> listen
# Fale seu comando em português:
# "abrir chrome"
# "adicionar tarefa estudar"
# "qual é minha agenda"
```

## 📊 Status

- ✅ Tarefas - Funcional
- ✅ Agenda - Funcional  
- ✅ Navegador - Funcional
- ✅ Memória - Funcional
- ✅ Voz - Funcional
- ✅ Google Sheets - Funcional (requer credenciais)
- ✅ API REST - Funcional

## 🆘 Problemas Comuns

### "ModuleNotFoundError: No module named 'vosk'"
```bash
pip install vosk pyaudio
```

### "Playwright not installed"
```bash
playwright install chromium
```

### "Microphone not working"
- Verifique os drivers de áudio
- Teste: `python -c "import pyaudio; print(pyaudio.PyAudio().get_default_input_device_info())"`

### Google Sheets não conecta
- Verifique se `credentials.json` existe na raiz
- Se não tem: veja seção 6️⃣ acima

## 📚 Próximos Passos

1. Leia [README.md](README.md) para documentação completa
2. Veja [API Documentation](#) para endpoints REST
3. Contribua com melhorias no [GitHub](#)

## 💡 Dicas

- Use `help` no programa para ver todos os comandos
- Tarefas com `amanhã` criam evento para amanhã
- `listen` ativa reconhecimento de voz em português
- Digite `quit` para sair

---

**Pronto para começar? Execute `python main.py` e divirta-se! 🎉**
