"""
Basic tests for Zac Personal Assistant.
"""
import pytest
import logging
from datetime import datetime, timedelta

from core.assistant import ZacAssistant
from database.sqlite_manager import SQLiteManager
from database.models import Task, TaskStatus, TaskPriority, CalendarEvent, EventType

logger = logging.getLogger(__name__)


@pytest.fixture
def assistant():
    """Create test assistant."""
    return ZacAssistant(db_path="test_zac.db")


@pytest.fixture
def db_manager():
    """Create test database."""
    return SQLiteManager(db_path="test_zac.db")


class TestDatabase:
    """Database tests."""
    
    def test_sqlite_initialization(self, db_manager):
        """Test database initialization."""
        assert db_manager.db_path.exists()
        logger.info("✓ Database initialized")
    
    def test_add_task(self, db_manager):
        """Test adding task."""
        task = Task(title="Test Task")
        added = db_manager.add_task(task)
        assert added.id is not None
        logger.info(f"✓ Task added: {added.id}")
    
    def test_get_task(self, db_manager):
        """Test getting task."""
        task = Task(title="Test Task 2")
        added = db_manager.add_task(task)
        retrieved = db_manager.get_task(added.id)
        assert retrieved.title == "Test Task 2"
        logger.info(f"✓ Task retrieved: {retrieved.title}")
    
    def test_update_task(self, db_manager):
        """Test updating task."""
        task = Task(title="Original")
        added = db_manager.add_task(task)
        added.title = "Updated"
        db_manager.update_task(added)
        retrieved = db_manager.get_task(added.id)
        assert retrieved.title == "Updated"
        logger.info("✓ Task updated")
    
    def test_delete_task(self, db_manager):
        """Test deleting task."""
        task = Task(title="To Delete")
        added = db_manager.add_task(task)
        db_manager.delete_task(added.id)
        retrieved = db_manager.get_task(added.id)
        assert retrieved is None
        logger.info("✓ Task deleted")


class TestTaskService:
    """Task service tests."""
    
    def test_create_task(self, assistant):
        """Test creating task."""
        task = assistant.tasks.create_task(
            title="Learn Python",
            priority=TaskPriority.HIGH
        )
        assert task.title == "Learn Python"
        assert task.priority == TaskPriority.HIGH
        logger.info(f"✓ Task created: {task.title}")
    
    def test_get_today_tasks(self, assistant):
        """Test getting today's tasks."""
        today = datetime.now()
        assistant.tasks.create_task(
            title="Today Task",
            due_date=today
        )
        tasks = assistant.tasks.get_today_tasks()
        assert len(tasks) > 0
        logger.info(f"✓ Retrieved {len(tasks)} today's tasks")
    
    def test_complete_task(self, assistant):
        """Test completing task."""
        task = assistant.tasks.create_task(title="Complete Me")
        success = assistant.tasks.complete_task(task.id)
        assert success
        completed = assistant.tasks.get_task(task.id)
        assert completed.status == TaskStatus.COMPLETED
        logger.info("✓ Task completed")
    
    def test_search_tasks(self, assistant):
        """Test searching tasks."""
        assistant.tasks.create_task(title="Python Programming")
        results = assistant.tasks.search_tasks("Python")
        assert len(results) > 0
        logger.info(f"✓ Search found {len(results)} tasks")


class TestCalendarService:
    """Calendar service tests."""
    
    def test_create_event(self, assistant):
        """Test creating event."""
        start = datetime.now() + timedelta(hours=1)
        event = assistant.calendar.create_event(
            title="Meeting",
            start_time=start,
            event_type=EventType.MEETING
        )
        assert event.title == "Meeting"
        logger.info(f"✓ Event created: {event.title}")
    
    def test_get_today_events(self, assistant):
        """Test getting today's events."""
        now = datetime.now()
        assistant.calendar.create_event(
            title="Today Event",
            start_time=now
        )
        events = assistant.calendar.get_today_events()
        assert len(events) > 0
        logger.info(f"✓ Retrieved {len(events)} today's events")
    
    def test_get_upcoming_events(self, assistant):
        """Test getting upcoming events."""
        tomorrow = datetime.now() + timedelta(days=1)
        assistant.calendar.create_event(
            title="Future Event",
            start_time=tomorrow
        )
        events = assistant.calendar.get_upcoming_events(days=7)
        assert len(events) > 0
        logger.info(f"✓ Retrieved {len(events)} upcoming events")


class TestMemoryService:
    """Memory service tests."""
    
    def test_save_memory(self, assistant):
        """Test saving memory."""
        entry = assistant.memory.save_memory(
            key="test_key",
            value="test_value",
            category="test"
        )
        assert entry.key == "test_key"
        logger.info(f"✓ Memory saved: {entry.key}")
    
    def test_get_memory(self, assistant):
        """Test getting memory."""
        assistant.memory.save_memory(
            key="test_key2",
            value="test_value2"
        )
        entry = assistant.memory.get_memory("test_key2")
        assert entry.value == "test_value2"
        logger.info(f"✓ Memory retrieved: {entry.value}")
    
    def test_save_important_person(self, assistant):
        """Test saving important person."""
        entry = assistant.memory.save_important_person(
            name="John Doe",
            info="Colega de trabalho"
        )
        assert entry.category == "pessoas"
        logger.info(f"✓ Important person saved")
    
    def test_save_goal(self, assistant):
        """Test saving goal."""
        entry = assistant.memory.save_goal(
            goal_name="Learning Python",
            description="Master Python programming"
        )
        assert entry.category == "metas"
        logger.info(f"✓ Goal saved")


class TestCommandRouter:
    """Command router tests."""
    
    def test_parse_add_task_command(self, assistant):
        """Test parsing add task command."""
        command = assistant.router.parse_command(
            "adicionar tarefa estudar Python amanhã"
        )
        assert command.action == "add_task"
        logger.info(f"✓ Command parsed: {command.action}")
    
    def test_parse_get_tasks_command(self, assistant):
        """Test parsing get tasks command."""
        command = assistant.router.parse_command(
            "quais são minhas tarefas de hoje"
        )
        assert command.action == "get_tasks"
        logger.info(f"✓ Command parsed: {command.action}")
    
    def test_parse_open_browser_command(self, assistant):
        """Test parsing open browser command."""
        command = assistant.router.parse_command(
            "abrir chrome"
        )
        assert command.action == "open_browser"
        logger.info(f"✓ Command parsed: {command.action}")
    
    def test_parse_remember_command(self, assistant):
        """Test parsing remember command."""
        command = assistant.router.parse_command(
            "lembrar que João é meu colega"
        )
        assert command.action == "remember"
        logger.info(f"✓ Command parsed: {command.action}")


def run_all_tests():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("RODANDO TESTES DO ZAC")
    print("=" * 60 + "\n")
    
    pytest.main([__file__, "-v", "--tb=short"])
    
    print("\n" + "=" * 60)
    print("TESTES COMPLETOS")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    run_all_tests()
