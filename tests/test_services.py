"""
Service-level tests for Zac Personal Assistant.
"""
import pytest
from datetime import datetime, timedelta

from core.assistant import ZacAssistant
from database.models import TaskPriority, TaskStatus, EventType


@pytest.fixture
def assistant():
    """Create test assistant."""
    return ZacAssistant(db_path="test_zac_services.db")


class TestIntegration:
    """Integration tests."""
    
    def test_full_task_workflow(self, assistant):
        """Test full task workflow."""
        # Create
        task = assistant.tasks.create_task(
            title="Complete Project",
            priority=TaskPriority.HIGH,
            tags=["work", "python"]
        )
        assert task.id is not None
        
        # Read
        retrieved = assistant.tasks.get_task(task.id)
        assert retrieved.title == "Complete Project"
        
        # Update
        assistant.tasks.update_task_priority(task.id, TaskPriority.URGENT)
        updated = assistant.tasks.get_task(task.id)
        assert updated.priority == TaskPriority.URGENT
        
        # Complete
        assistant.tasks.complete_task(task.id)
        completed = assistant.tasks.get_task(task.id)
        assert completed.status == TaskStatus.COMPLETED
        
        # Delete
        assistant.tasks.delete_task(task.id)
        deleted = assistant.tasks.get_task(task.id)
        assert deleted is None
        
        print("✓ Full task workflow completed")
    
    def test_full_event_workflow(self, assistant):
        """Test full event workflow."""
        start = datetime.now() + timedelta(hours=1)
        end = start + timedelta(hours=2)
        
        # Create
        event = assistant.calendar.create_event(
            title="Project Review",
            start_time=start,
            end_time=end,
            location="Room A",
            event_type=EventType.MEETING
        )
        assert event.id is not None
        
        # Read
        retrieved = assistant.calendar.get_event(event.id)
        assert retrieved.title == "Project Review"
        
        # Update
        assistant.calendar.update_event(
            event.id,
            location="Room B"
        )
        updated = assistant.calendar.get_event(event.id)
        assert updated.location == "Room B"
        
        # Delete
        assistant.calendar.delete_event(event.id)
        deleted = assistant.calendar.get_event(event.id)
        assert deleted is None
        
        print("✓ Full event workflow completed")
    
    def test_memory_workflow(self, assistant):
        """Test memory workflow."""
        # Save person
        assistant.memory.save_important_person(
            name="Alice",
            info="CEO of TechCorp"
        )
        
        # Save goal
        assistant.memory.save_goal(
            goal_name="Master AI",
            description="Learn machine learning and LLMs"
        )
        
        # Save preference
        assistant.memory.save_preference(
            preference_name="coffee_time",
            value="09:00"
        )
        
        # Retrieve
        people = assistant.memory.get_important_people()
        assert len(people) > 0
        
        goals = assistant.memory.get_goals()
        assert len(goals) > 0
        
        prefs = assistant.memory.get_preferences()
        assert len(prefs) > 0
        
        print("✓ Memory workflow completed")
    
    def test_command_execution(self, assistant):
        """Test command execution."""
        # Test task command
        result = assistant.process_command(
            "adicionar tarefa aprender Rust"
        )
        assert result is not None
        assert "Tarefa adicionada" in result
        
        # Test memory command
        result = assistant.process_command(
            "lembrar que Maria é minha amiga"
        )
        assert result is not None
        
        print("✓ Command execution completed")
    
    def test_scheduler(self, assistant):
        """Test scheduler."""
        executed = []
        
        def test_callback():
            executed.append(True)
        
        # Schedule in 1 second
        assistant.scheduler.schedule_in(
            task_id="test_task",
            callback=test_callback,
            seconds=1
        )
        
        # Wait for execution
        import time
        time.sleep(2)
        
        assert len(executed) > 0
        print("✓ Scheduler completed")


class TestErrorHandling:
    """Error handling tests."""
    
    def test_invalid_task_id(self, assistant):
        """Test handling invalid task ID."""
        result = assistant.tasks.get_task(99999)
        assert result is None
        print("✓ Invalid task ID handled")
    
    def test_invalid_event_id(self, assistant):
        """Test handling invalid event ID."""
        result = assistant.calendar.get_event(99999)
        assert result is None
        print("✓ Invalid event ID handled")
    
    def test_invalid_memory_key(self, assistant):
        """Test handling invalid memory key."""
        result = assistant.memory.get_memory("nonexistent_key")
        assert result is None
        print("✓ Invalid memory key handled")


class TestPerformance:
    """Performance tests."""
    
    def test_bulk_task_creation(self, assistant):
        """Test creating many tasks."""
        import time
        start = time.time()
        
        for i in range(100):
            assistant.tasks.create_task(f"Task {i}")
        
        elapsed = time.time() - start
        
        tasks = assistant.tasks.get_all_tasks()
        assert len(tasks) >= 100
        
        print(f"✓ Created 100 tasks in {elapsed:.2f}s")
    
    def test_bulk_event_creation(self, assistant):
        """Test creating many events."""
        import time
        start = time.time()
        
        base_time = datetime.now()
        for i in range(50):
            assistant.calendar.create_event(
                title=f"Event {i}",
                start_time=base_time + timedelta(hours=i)
            )
        
        elapsed = time.time() - start
        
        events = assistant.calendar.get_all_events()
        assert len(events) >= 50
        
        print(f"✓ Created 50 events in {elapsed:.2f}s")
    
    def test_search_performance(self, assistant):
        """Test search performance."""
        import time
        
        # Create some tasks
        for i in range(50):
            assistant.tasks.create_task(
                f"Python Task {i}",
                tags=["python", "programming"]
            )
        
        # Search
        start = time.time()
        results = assistant.tasks.search_tasks("Python")
        elapsed = time.time() - start
        
        assert len(results) > 0
        print(f"✓ Searched 50 tasks in {elapsed:.3f}s")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
