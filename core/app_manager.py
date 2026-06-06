"""Application manager service for Zac assistant."""
import logging
import os
import subprocess
import webbrowser
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class AppManagerService:
    """Manages application, file, folder and URL actions on Windows."""

    APPS: Dict[str, List[str]] = {
        "vscode": ["code"],
        "code": ["code"],
        "edge": ["msedge", "edge"],
        "chrome": ["chrome", "google chrome"],
        "notepad": ["notepad"],
        "explorer": ["explorer"],
        "spotify": ["spotify"],
        "discord": ["discord"],
        "whatsapp": ["WhatsApp"],
        "terminal": ["cmd", "powershell"],
    }

    def __init__(self):
        self.platform = os.name

    def _find_app_command(self, app_name: str) -> Optional[str]:
        normalized = app_name.strip().lower()
        for key, commands in self.APPS.items():
            if normalized == key or normalized in [cmd.lower() for cmd in commands]:
                return commands[0]
        for key, commands in self.APPS.items():
            if key in normalized:
                return commands[0]
        return None

    def open_app(self, app_name: str) -> str:
        """Open application by name."""
        if not app_name:
            return "Nome do aplicativo não informado."

        command = self._find_app_command(app_name)
        if not command:
            return f"Aplicativo '{app_name}' não encontrado."

        try:
            subprocess.Popen([command], shell=False)
            logger.info(f"Opening application: {command}")
            return f"Abrindo {app_name}."
        except FileNotFoundError:
            logger.error(f"Application executable not found: {command}")
            return f"Não foi possível abrir {app_name}. Executável não encontrado."
        except Exception as exc:
            logger.error(f"Failed to open app {app_name}: {exc}")
            return f"Erro ao abrir {app_name}: {exc}"

    def open_folder(self, path: str) -> str:
        """Open folder in Windows Explorer."""
        if not path:
            return "Caminho da pasta não informado."

        target = Path(path).expanduser()
        if not target.exists() or not target.is_dir():
            return f"Pasta não encontrada: {target}"

        try:
            os.startfile(str(target))
            logger.info(f"Opening folder: {target}")
            return f"Abrindo pasta {target}."
        except Exception as exc:
            logger.error(f"Failed to open folder {target}: {exc}")
            return f"Erro ao abrir a pasta: {exc}"

    def open_file(self, path: str) -> str:
        """Open any file with the default program."""
        if not path:
            return "Caminho do arquivo não informado."

        target = Path(path).expanduser()
        if not target.exists() or not target.is_file():
            return f"Arquivo não encontrado: {target}"

        try:
            os.startfile(str(target))
            logger.info(f"Opening file: {target}")
            return f"Abrindo arquivo {target}."
        except Exception as exc:
            logger.error(f"Failed to open file {target}: {exc}")
            return f"Erro ao abrir o arquivo: {exc}"

    def open_vscode_project(self, project_path: str) -> str:
        """Open specific folder in VS Code."""
        if not project_path:
            return "Caminho do projeto não informado."

        target = Path(project_path).expanduser()
        if not target.exists() or not target.is_dir():
            return f"Projeto não encontrado: {target}"

        try:
            subprocess.Popen(["code", str(target)], shell=False)
            logger.info(f"Opening VSCode project: {target}")
            return f"Abrindo projeto VSCode em {target}."
        except FileNotFoundError:
            logger.error("VSCode command not found")
            return "Não foi possível encontrar o VSCode. Verifique se o comando 'code' está no PATH."
        except Exception as exc:
            logger.error(f"Failed to open VSCode project {target}: {exc}")
            return f"Erro ao abrir o projeto no VSCode: {exc}"

    def open_url(self, url: str) -> str:
        """Open URL in the default browser."""
        if not url:
            return "URL não informada."

        normalized_url = url.strip()
        if not normalized_url.startswith(("http://", "https://")):
            normalized_url = f"https://{normalized_url}"

        try:
            webbrowser.open(normalized_url)
            logger.info(f"Opening URL: {normalized_url}")
            return f"Abrindo URL {normalized_url}."
        except Exception as exc:
            logger.error(f"Failed to open URL {normalized_url}: {exc}")
            return f"Erro ao abrir URL: {exc}"

    def search_youtube(self, query: str) -> str:
        """Open YouTube search in browser."""
        if not query:
            return "Termo de pesquisa do YouTube não informado."

        encoded_query = query.strip().replace(" ", "+")
        url = f"https://www.youtube.com/results?search_query={encoded_query}"
        return self.open_url(url)

    def search_google(self, query: str) -> str:
        """Open Google search in browser."""
        if not query:
            return "Termo de pesquisa do Google não informado."

        encoded_query = query.strip().replace(" ", "+")
        url = f"https://www.google.com/search?q={encoded_query}"
        return self.open_url(url)
