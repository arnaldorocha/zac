"""
Task service for task management.
"""
import logging
from typing import Optional, List
from datetime import datetime

from database.sqlite_manager import SQLiteManager
from database.models import Task, TaskStatus, TaskPriority

logger = logging.getLogger(__name__)


class TaskService:
    """Manages tasks."""
    
    def __init__(self, db_manager: SQLiteManager):
        """
        Initialize task service.
        
        Args:
            db_manager: SQLite database manager
        """
        self.db = db_manager
    
    def create_task(
        self,
        title: str,
        description: str = "",
        priority: TaskPriority = TaskPriority.MEDIUM,
        due_date: Optional[datetime] = None,
        tags: Optional[List[str]] = None
    ) -> Task:
        """Create new task."""
        task = Task(
            title=title,
            description=description,
            priority=priority,
            due_date=due_date,
            tags=tags or []
        )
        
        self.db.add_task(task)
        logger.info(f"Task created: {title}")
        return task
    
    def get_task(self, task_id: int) -> Optional[Task]:
        """Get task by ID."""
        return self.db.get_task(task_id)
    
    def get_all_tasks(self) -> List[Task]:
        """Get all tasks."""
        return self.db.get_all_tasks()
    
    def get_today_tasks(self) -> List[Task]:
        """Get today's tasks."""
        today = datetime.now().date()
        tasks = self.db.get_all_tasks()
        return [
            task for task in tasks
            if task.due_date and task.due_date.date() == today
            and task.status != TaskStatus.COMPLETED
        ]
    
    def get_pending_tasks(self) -> List[Task]:
        """Get pending tasks."""
        return self.db.get_tasks_by_status(TaskStatus.TODO)
    
    def complete_task(self, task_id: int) -> bool:
        """Mark task as completed."""
        task = self.db.get_task(task_id)
        if not task:
            logger.warning(f"Task {task_id} not found")
            return False
        
        task.status = TaskStatus.COMPLETED
        task.updated_at = datetime.now()
        self.db.update_task(task)
        logger.info(f"Task completed: {task_id}")
        return True
    
    def update_task_priority(self, task_id: int, priority: TaskPriority) -> bool:
        """Update task priority."""
        task = self.db.get_task(task_id)
        if not task:
            logger.warning(f"Task {task_id} not found")
            return False
        
        task.priority = priority
        task.updated_at = datetime.now()
        self.db.update_task(task)
        logger.info(f"Task priority updated: {task_id}")
        return True
    
    def add_tag(self, task_id: int, tag: str) -> bool:
        """Add tag to task."""
        task = self.db.get_task(task_id)
        if not task:
            logger.warning(f"Task {task_id} not found")
            return False
        
        if tag not in task.tags:
            task.tags.append(tag)
            task.updated_at = datetime.now()
            self.db.update_task(task)
            logger.info(f"Tag added to task {task_id}: {tag}")
        
        return True
    
    def delete_task(self, task_id: int) -> bool:
        """Delete task."""
        return self.db.delete_task(task_id)
    
    def get_tasks_by_tag(self, tag: str) -> List[Task]:
        """Get tasks by tag."""
        all_tasks = self.db.get_all_tasks()
        return [task for task in all_tasks if tag in task.tags]
    
    def get_high_priority_tasks(self) -> List[Task]:
        """Get high priority tasks."""
        all_tasks = self.db.get_all_tasks()
        return [
            task for task in all_tasks
            if task.priority in (TaskPriority.HIGH, TaskPriority.URGENT)
            and task.status != TaskStatus.COMPLETED
        ]
    
    def search_tasks(self, query: str) -> List[Task]:
        """Search tasks by title or description."""
        all_tasks = self.db.get_all_tasks()
        query_lower = query.lower()
        return [
            task for task in all_tasks
            if query_lower in task.title.lower()
            or query_lower in task.description.lower()
        ]
