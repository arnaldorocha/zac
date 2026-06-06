"""
Main Zac Personal Assistant - orchestrates all services.
"""
import logging
from typing import Optional
from datetime import datetime

from voice.speech_to_text import SpeechToText
from voice.text_to_speech import TextToSpeech
from browser.browser_service import BrowserAutomationService
from sheets.google_sheets_service import GoogleSheetsService
from tasks.task_service import TaskService
from calendar_service.calendar_service import CalendarService
from memory.memory_service import MemoryService
from database.sqlite_manager import SQLiteManager
from database.models import TaskPriority, EventType
from core.command_router import CommandRouter, CommandType
from core.scheduler import Scheduler

logger = logging.getLogger(__name__)


class ZacAssistant:
    """Zac Personal Assistant - main orchestrator."""
    
    def __init__(self, db_path: str = "zac.db"):
        """Initialize Zac assistant."""
        logger.info("Initializing Zac Personal Assistant...")
        
        # Initialize database
        self.db = SQLiteManager(db_path=db_path)
        
        # Initialize services
        self.tasks = TaskService(self.db)
        self.calendar = CalendarService(self.db)
        self.memory = MemoryService(self.db)
        
        # Initialize voice
        self.tts = TextToSpeech()
        self.stt = SpeechToText()
        
        # Initialize browser
        self.browser = BrowserAutomationService()
        
        # Initialize sheets
        self.sheets = GoogleSheetsService()
        
        # Initialize command router
        self.router = CommandRouter()
        self._setup_handlers()
        
        # Initialize scheduler
        self.scheduler = Scheduler()
        self.scheduler.start()
        
        logger.info("Zac Assistant initialized successfully")
    
    def _setup_handlers(self) -> None:
        """Setup command handlers."""
        # Browser handlers
        self.router.register_handler(
            CommandType.BROWSER, "open_browser", self.handle_open_browser
        )
        self.router.register_handler(
            CommandType.BROWSER, "navigate", self.handle_navigate
        )
        
        # Task handlers
        self.router.register_handler(
            CommandType.TASK, "add_task", self.handle_add_task
        )
        self.router.register_handler(
            CommandType.TASK, "get_tasks", self.handle_get_tasks
        )
        self.router.register_handler(
            CommandType.TASK, "complete_task", self.handle_complete_task
        )
        
        # Calendar handlers
        self.router.register_handler(
            CommandType.CALENDAR, "add_event", self.handle_add_event
        )
        self.router.register_handler(
            CommandType.CALENDAR, "get_agenda", self.handle_get_agenda
        )
        
        # Memory handlers
        self.router.register_handler(
            CommandType.MEMORY, "remember", self.handle_remember
        )
        
        # Sheets handlers
        self.router.register_handler(
            CommandType.SHEETS, "log_expense", self.handle_log_expense
        )
        self.router.register_handler(
            CommandType.SHEETS, "log_study", self.handle_log_study
        )
    
    def listen_and_execute(self) -> Optional[str]:
        """Listen for voice command and execute."""
        logger.info("Waiting for voice command...")
        self.tts.speak("Estou ouvindo...")
        
        # Listen for command
        command_text = self.stt.listen(timeout=10)
        if not command_text:
            self.tts.speak("Desculpe, não consegui ouvir sua voz. Tente novamente.")
            return None
        
        logger.info(f"Voice command received: {command_text}")
        
        # Parse and execute
        return self.process_command(command_text)
    
    def process_command(self, command_text: str) -> Optional[str]:
        """Process text command."""
        # Parse command
        command = self.router.parse_command(command_text)
        
        # Execute command
        result = self.router.execute(command)
        
        if result:
            logger.info(f"Command result: {result}")
            self.tts.speak(result)
        
        return result
    
    # Browser handlers
    def handle_open_browser(self, params: dict) -> str:
        """Handle open browser command."""
        browser_name = params.get('browser', 'chrome')
        self.browser.open_browser()
        self.tts.speak(f"Abrindo {browser_name}")
        return f"{browser_name} aberto com sucesso"
    
    def handle_navigate(self, params: dict) -> str:
        """Handle navigate command."""
        url = params.get('url', '')
        if url:
            if not url.startswith('http'):
                url = f"https://google.com/search?q={url}"
            self.browser.navigate(url)
            return f"Navegando para {url}"
        return "URL não especificada"
    
    # Task handlers
    def handle_add_task(self, params: dict) -> str:
        """Handle add task command."""
        title = params.get('title', '')
        when = params.get('when', '')
        
        if not title:
            return "Título da tarefa não especificado"
        
        # Simple due date parsing
        due_date = None
        if 'amanhã' in when:
            from datetime import timedelta
            due_date = datetime.now() + timedelta(days=1)
        elif 'hoje' in when:
            due_date = datetime.now()
        
        task = self.tasks.create_task(title, due_date=due_date)
        return f"Tarefa adicionada: {title}"
    
    def handle_get_tasks(self, params: dict) -> str:
        """Handle get tasks command."""
        filter_type = params.get('filter', 'today')
        
        if filter_type == 'today':
            tasks = self.tasks.get_today_tasks()
            if not tasks:
                return "Nenhuma tarefa para hoje"
        else:
            tasks = self.tasks.get_pending_tasks()
        
        if not tasks:
            return "Nenhuma tarefa pendente"
        
        response = f"Você tem {len(tasks)} tarefas:\n"
        for task in tasks[:5]:  # Limit to 5 tasks
            response += f"- {task.title}\n"
        
        return response
    
    def handle_complete_task(self, params: dict) -> str:
        """Handle complete task command."""
        task_name = params.get('task_name', '')
        
        # Search for task
        tasks = self.tasks.search_tasks(task_name)
        if not tasks:
            return f"Tarefa '{task_name}' não encontrada"
        
        task = tasks[0]
        self.tasks.complete_task(task.id)
        return f"Tarefa concluída: {task.title}"
    
    # Calendar handlers
    def handle_add_event(self, params: dict) -> str:
        """Handle add event command."""
        title = params.get('title', '')
        time_str = params.get('time', '')
        
        if not title:
            return "Título do compromisso não especificado"
        
        # Simple time parsing
        start_time = datetime.now()
        if 'amanhã' in time_str:
            from datetime import timedelta
            start_time += timedelta(days=1)
        
        event = self.calendar.create_event(
            title=title,
            start_time=start_time,
            event_type=EventType.APPOINTMENT
        )
        return f"Compromisso adicionado: {title}"
    
    def handle_get_agenda(self, params: dict) -> str:
        """Handle get agenda command."""
        events = self.calendar.get_today_events()
        
        if not events:
            return "Nenhum compromisso para hoje"
        
        response = f"Você tem {len(events)} compromissos hoje:\n"
        for event in events:
            time_str = event.start_time.strftime("%H:%M") if event.start_time else "Sem horário"
            response += f"- {event.title} às {time_str}\n"
        
        return response
    
    # Memory handlers
    def handle_remember(self, params: dict) -> str:
        """Handle remember command."""
        info = params.get('info', '')
        
        if not info:
            return "Informação não especificada"
        
        self.memory.save_useful_info(
            topic=info[:30],  # Use first 30 chars as topic
            info=info
        )
        return f"Memória salva: {info[:50]}"
    
    # Sheets handlers
    def handle_log_expense(self, params: dict) -> str:
        """Handle log expense command."""
        amount = params.get('amount', '0')
        category = params.get('category', 'outro')
        
        try:
            # In a real scenario, would update Google Sheets here
            # For now, just log locally
            self.memory.save_memory(
                key=f"expense_{datetime.now().timestamp()}",
                value=f"R${amount} - {category}",
                category="gastos"
            )
            return f"Gasto registrado: R${amount} em {category}"
        except Exception as e:
            return f"Erro ao registrar gasto: {str(e)}"
    
    def handle_log_study(self, params: dict) -> str:
        """Handle log study command."""
        discipline = params.get('discipline', '')
        hours = params.get('hours', '1')
        
        try:
            self.memory.save_memory(
                key=f"study_{datetime.now().timestamp()}",
                value=f"{discipline} - {hours}h",
                category="estudos"
            )
            return f"Estudo registrado: {hours}h de {discipline}"
        except Exception as e:
            return f"Erro ao registrar estudo: {str(e)}"
    
    def shutdown(self) -> None:
        """Shutdown assistant."""
        logger.info("Shutting down Zac Assistant...")
        
        self.scheduler.stop()
        self.browser.close_browser()
        self.stt.close()
        
        logger.info("Zac Assistant shutdown complete")
