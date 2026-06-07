"""
Command router for parsing and routing voice commands.
"""
import logging
import re
from typing import Dict, Callable, Optional, List, Tuple
from enum import Enum

logger = logging.getLogger(__name__)


class CommandType(str, Enum):
    """Command types."""
    APP = "app"
    BROWSER = "browser"
    TASK = "task"
    CALENDAR = "calendar"
    MEMORY = "memory"
    SHEETS = "sheets"
    SYSTEM = "system"
    UNKNOWN = "unknown"


class Command:
    """Parsed command."""
    
    def __init__(
        self,
        command_type: CommandType,
        action: str,
        params: Dict[str, str]
    ):
        self.type = command_type
        self.action = action
        self.params = params


class CommandRouter:
    """Routes commands to appropriate handlers."""
    
    def __init__(self):
        """Initialize command router."""
        self.handlers: Dict[str, Callable] = {}
        self._setup_patterns()
    
    def _setup_patterns(self) -> None:
        """Setup command patterns."""
        self.patterns = {
            # App commands (before browser to catch abrir variations)
            CommandType.APP: [
                (r"abri(?:u|r|a)?\s+(?:o\s+)?(\w+)", self._parse_open_app),
               
            ],
            # Browser commands
            CommandType.BROWSER: [
                (r"abrir\s+(chrome|navigator|firefox|edge|navegador)", self._parse_open_browser),
                (r"abril\s+(chrome|navigator|firefox|edge|navegador)", self._parse_open_browser),
                (r"abriu\s+(chrome|navigator|firefox|edge|navegador)", self._parse_open_browser),
                (r"abri\s+(chrome|navigator|firefox|edge|navegador)", self._parse_open_browser),
                (r"abre\s+(chrome|navigator|firefox|edge|navegador)", self._parse_open_browser),
                (r"navigar\s+para\s+(.+)", self._parse_navigate),
                (r"mavigar\s+para\s+(.+)", self._parse_navigate),
                (r"navegar\s+(?:o\s+|para\s+o\s+|para\s+)?(.+)", self._parse_navigate),
                (r"navegar\s+para\s+(.+)", self._parse_navigate),
                (r"clicar\s+em\s+(.+)", self._parse_click),
            ],
            # Task commands
            CommandType.TASK: [
                (r"adicionar\s+tarefa\s+(.+?)(?:\s+amanhã|\s+hoje|\s+em\s+)?(.*)$", self._parse_add_task),
                (r"quais\s+são\s+(?:minhas\s+)?tarefas\s+(?:de\s+)?(.+)", self._parse_get_tasks),
                (r"tarefas\s+(?:de\s+)?(.+)", self._parse_get_tasks),
                (r"concluir\s+tarefa\s+(.+)", self._parse_complete_task),
            ],
            # Calendar commands
            CommandType.CALENDAR: [
                (r"adicionar\s+(?:compromisso|evento|reunião)\s+(.+?)(?:\s+às?\s+)?(.*)$", self._parse_add_event),
                (r"minha\s+agenda", self._parse_get_agenda),
                (r"agenda(?:\s+(?:de\s+)?(.+))?", self._parse_get_agenda),
            ],
            # Memory commands
            CommandType.MEMORY: [
                (r"lembrar\s+que\s+(.+)", self._parse_remember),
                (r"salvar\s+(.+)", self._parse_remember),
            ],
            # Sheets commands
            CommandType.SHEETS: [
                (r"registrar\s+(?:gasto|gastos)\s+de\s+(.+?)(?:\s+com\s+)?(.+)?", self._parse_log_expense),
                (r"registrar\s+estudo\s+(?:de\s+)?(.+?)(?:\s+por\s+)?(.+)?", self._parse_log_study),
                (r"atualizar\s+(?:minha\s+)?planilha", self._parse_update_sheets),
            ],
        }
    
    def parse_command(self, text: str) -> Command:
        """Parse command from text."""
        text_lower = text.lower().strip()
        text_lower = text_lower.replace(",", "").replace(".", "").replace("!", "").replace("?", "")


        # Remove greeting prefix if present
        if text_lower.startswith("zac "):
            text_lower = text_lower[4:]
        elif text_lower.startswith("jarvis "):
            text_lower = text_lower[7:]
        
        logger.info(f"Parsing command: {text_lower}")
        
        # Try to match patterns
        for command_type, patterns in self.patterns.items():
            for pattern, parser in patterns:
                match = re.match(pattern, text_lower)
                if match:
                    result = parser(match)
                    if result:
                        logger.info(f"Command parsed: {command_type.value} - {result['action']}")
                        return Command(
                            command_type=command_type,
                            action=result['action'],
                            params=result.get('params', {})
                        )
        
        logger.warning(f"Unknown command: {text}")
        return Command(
            command_type=CommandType.UNKNOWN,
            action="unknown",
            params={"original": text}
        )
    
    def register_handler(
        self,
        command_type: CommandType,
        action: str,
        handler: Callable
    ) -> None:
        """Register command handler."""
        key = f"{command_type.value}:{action}"
        self.handlers[key] = handler
        logger.info(f"Handler registered: {key}")
    
    def execute(self, command: Command) -> Optional[str]:
        """Execute command."""
        key = f"{command.type.value}:{command.action}"
        
        if key not in self.handlers:
            logger.warning(f"No handler for command: {key}")
            return f"Comando não reconhecido: {command.action}"
        
        try:
            result = self.handlers[key](command.params)
            return result
        except Exception as e:
            logger.error(f"Error executing command {key}: {e}")
            return f"Erro ao executar comando: {str(e)}"
    
    # Parsers
    def _parse_open_app(self, match) -> Dict:
        """Parse open app command."""
        return {
            'action': 'open_app',
            'params': {'app_name': match.group(1)}
        }
    
    def _parse_open_browser(self, match) -> Dict:
        """Parse open browser command."""
        return {
            'action': 'open_browser',
            'params': {'browser': match.group(1)}
        }
    
    def _parse_navigate(self, match) -> Dict:
        """Parse navigate command."""
        return {
            'action': 'navigate',
            'params': {'url': match.group(1)}
        }
    
    def _parse_click(self, match) -> Dict:
        """Parse click command."""
        return {
            'action': 'click',
            'params': {'element': match.group(1)}
        }
    
    def _parse_add_task(self, match) -> Dict:
        """Parse add task command."""
        return {
            'action': 'add_task',
            'params': {
                'title': match.group(1),
                'when': match.group(2) if match.group(2) else ''
            }
        }
    
    def _parse_get_tasks(self, match) -> Dict:
        """Parse get tasks command."""
        return {
            'action': 'get_tasks',
            'params': {'filter': match.group(1) if match.group(1) else 'today'}
        }
    
    def _parse_complete_task(self, match) -> Dict:
        """Parse complete task command."""
        return {
            'action': 'complete_task',
            'params': {'task_name': match.group(1)}
        }
    
    def _parse_add_event(self, match) -> Dict:
        """Parse add event command."""
        return {
            'action': 'add_event',
            'params': {
                'title': match.group(1),
                'time': match.group(2) if match.group(2) else ''
            }
        }
    
    def _parse_get_agenda(self, match) -> Dict:
        """Parse get agenda command."""
        return {
            'action': 'get_agenda',
            'params': {'date': match.group(1) if match.group(1) else 'today'}
        }
    
    def _parse_remember(self, match) -> Dict:
        """Parse remember command."""
        return {
            'action': 'remember',
            'params': {'info': match.group(1)}
        }
    
    def _parse_log_expense(self, match) -> Dict:
        """Parse log expense command."""
        return {
            'action': 'log_expense',
            'params': {
                'amount': match.group(1),
                'category': match.group(2) if match.group(2) else 'outro'
            }
        }
    
    def _parse_log_study(self, match) -> Dict:
        """Parse log study command."""
        return {
            'action': 'log_study',
            'params': {
                'discipline': match.group(1),
                'hours': match.group(2) if match.group(2) else '1'
            }
        }
    
    def _parse_update_sheets(self, match) -> Dict:
        """Parse update sheets command."""
        return {
            'action': 'update_sheets',
            'params': {}
        }
