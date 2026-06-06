@echo off
REM Zac Personal Assistant - Installation Script for Windows

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                                                                ║
echo ║          Zac - Personal AI Assistant                          ║
echo ║               Installation Script                             ║
echo ║                                                                ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

setlocal enabledelayedexpansion

REM Check Python installation
echo [1/5] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ✗ Python não encontrado! Instale Python 3.12+ de https://python.org
    pause
    exit /b 1
)
echo ✓ Python encontrado

REM Create virtual environment
echo.
echo [2/5] Criando ambiente virtual...
if exist venv (
    echo ✓ Ambiente virtual já existe
) else (
    python -m venv venv
    if errorlevel 1 (
        echo ✗ Erro ao criar ambiente virtual
        pause
        exit /b 1
    )
    echo ✓ Ambiente virtual criado
)

REM Activate virtual environment
echo.
echo [3/5] Ativando ambiente virtual...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ✗ Erro ao ativar ambiente virtual
    pause
    exit /b 1
)
echo ✓ Ambiente virtual ativado

REM Upgrade pip
echo.
echo [4/5] Instalando dependências...
python -m pip install --upgrade pip setuptools wheel >nul 2>&1
pip install -r requirements.txt
if errorlevel 1 (
    echo ✗ Erro ao instalar dependências
    pause
    exit /b 1
)
echo ✓ Dependências instaladas

REM Install Playwright browsers
echo.
echo [5/5] Configurando Playwright...
playwright install chromium
if errorlevel 1 (
    echo ⚠ Aviso: Erro ao instalar browsers do Playwright
    echo   Tente executar: playwright install chromium
)
echo ✓ Playwright configurado

REM Create necessary directories
echo.
echo Criando diretórios necessários...
if not exist data mkdir data
if not exist logs mkdir logs
echo ✓ Diretórios criados

REM Create .env file
echo.
if not exist .env (
    echo Criando arquivo .env...
    copy .env.example .env >nul
    echo ✓ Arquivo .env criado (configure conforme necessário)
) else (
    echo ✓ Arquivo .env já existe
)

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                                                                ║
echo ║               Instalação Completa! ✓                          ║
echo ║                                                                ║
echo ║  Para começar:                                                 ║
echo ║                                                                ║
echo ║  1. Abra um novo Terminal PowerShell/CMD                       ║
echo ║                                                                ║
echo ║  2. Execute:                                                   ║
echo ║     venv\Scripts\activate.bat                                  ║
echo ║     python main.py                                             ║
echo ║                                                                ║
echo ║  3. Digite 'help' para ver os comandos disponíveis             ║
echo ║                                                                ║
echo ║  Documentação: README.md                                       ║
echo ║  Testes: python -m pytest tests/ -v                            ║
echo ║  API: python -m uvicorn api.server:app --host 127.0.0.1       ║
echo ║                                                                ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

pause
