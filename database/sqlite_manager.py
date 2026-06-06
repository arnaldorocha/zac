"""
SQLite database manager for Zac.
"""
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional, List
import logging

from database.models import (
    Task, TaskStatus, TaskPriority,
    CalendarEvent, EventType,
    MemoryEntry
)

logger = logging.getLogger(__name__)


class SQLiteManager:
    """Manages SQLite database operations."""
    
    def __init__(self, db_path: str = "zac.db"):
        """Initialize database manager."""
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_database()
    
    def _init_database(self) -> None:
        """Initialize database tables."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Tasks table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    status TEXT NOT NULL DEFAULT 'todo',
                    priority TEXT NOT NULL DEFAULT 'medium',
                    due_date TIMESTAMP,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    tags TEXT
                )
            """)
            
            # Calendar events table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS calendar_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    event_type TEXT NOT NULL DEFAULT 'appointment',
                    start_time TIMESTAMP NOT NULL,
                    end_time TIMESTAMP,
                    location TEXT,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    reminder_minutes INTEGER DEFAULT 15
                )
            """)
            
            # Memory entries table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS memory_entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key TEXT NOT NULL UNIQUE,
                    value TEXT NOT NULL,
                    category TEXT,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()
            logger.info(f"Database initialized at {self.db_path}")
    
    # Task methods
    def add_task(self, task: Task) -> Task:
        """Add a new task."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            tags_str = ",".join(task.tags) if task.tags else ""
            
            cursor.execute("""
                INSERT INTO tasks (title, description, status, priority, due_date, tags)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (task.title, task.description, task.status.value, task.priority.value,
                  task.due_date, tags_str))
            
            task.id = cursor.lastrowid
            conn.commit()
            logger.info(f"Task added: {task.title} (ID: {task.id})")
        
        return task
    
    def get_task(self, task_id: int) -> Optional[Task]:
        """Get a task by ID."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
            row = cursor.fetchone()
            
            if row:
                return self._row_to_task(row)
        return None
    
    def get_all_tasks(self) -> List[Task]:
        """Get all tasks."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks ORDER BY due_date ASC")
            rows = cursor.fetchall()
            return [self._row_to_task(row) for row in rows]
    
    def get_tasks_by_status(self, status: TaskStatus) -> List[Task]:
        """Get tasks by status."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM tasks WHERE status = ? ORDER BY due_date ASC",
                (status.value,)
            )
            rows = cursor.fetchall()
            return [self._row_to_task(row) for row in rows]
    
    def update_task(self, task: Task) -> bool:
        """Update a task."""
        if not task.id:
            logger.warning("Cannot update task without ID")
            return False
        
        task.updated_at = datetime.now()
        tags_str = ",".join(task.tags) if task.tags else ""
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE tasks 
                SET title = ?, description = ?, status = ?, priority = ?, 
                    due_date = ?, tags = ?, updated_at = ?
                WHERE id = ?
            """, (task.title, task.description, task.status.value, task.priority.value,
                  task.due_date, tags_str, task.updated_at, task.id))
            
            conn.commit()
            logger.info(f"Task updated: {task.id}")
        
        return cursor.rowcount > 0
    
    def delete_task(self, task_id: int) -> bool:
        """Delete a task."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            conn.commit()
            logger.info(f"Task deleted: {task_id}")
        
        return cursor.rowcount > 0
    
    def _row_to_task(self, row: tuple) -> Task:
        """Convert database row to Task object."""
        task = Task(
            id=row[0],
            title=row[1],
            description=row[2],
            status=TaskStatus(row[3]),
            priority=TaskPriority(row[4]),
            due_date=datetime.fromisoformat(row[5]) if row[5] else None,
            created_at=datetime.fromisoformat(row[6]),
            updated_at=datetime.fromisoformat(row[7]),
            tags=row[8].split(",") if row[8] else []
        )
        return task
    
    # Calendar methods
    def add_event(self, event: CalendarEvent) -> CalendarEvent:
        """Add a calendar event."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO calendar_events 
                (title, description, event_type, start_time, end_time, location, reminder_minutes)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (event.title, event.description, event.event_type.value,
                  event.start_time, event.end_time, event.location, event.reminder_minutes))
            
            event.id = cursor.lastrowid
            conn.commit()
            logger.info(f"Event added: {event.title} (ID: {event.id})")
        
        return event
    
    def get_event(self, event_id: int) -> Optional[CalendarEvent]:
        """Get an event by ID."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM calendar_events WHERE id = ?", (event_id,))
            row = cursor.fetchone()
            
            if row:
                return self._row_to_event(row)
        return None
    
    def get_all_events(self) -> List[CalendarEvent]:
        """Get all events."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM calendar_events ORDER BY start_time ASC")
            rows = cursor.fetchall()
            return [self._row_to_event(row) for row in rows]
    
    def get_events_by_date(self, date: datetime) -> List[CalendarEvent]:
        """Get events for a specific date."""
        date_str = date.strftime("%Y-%m-%d")
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM calendar_events 
                WHERE DATE(start_time) = ?
                ORDER BY start_time ASC
            """, (date_str,))
            rows = cursor.fetchall()
            return [self._row_to_event(row) for row in rows]
    
    def update_event(self, event: CalendarEvent) -> bool:
        """Update a calendar event."""
        if not event.id:
            logger.warning("Cannot update event without ID")
            return False
        
        event.updated_at = datetime.now()
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE calendar_events 
                SET title = ?, description = ?, event_type = ?, start_time = ?,
                    end_time = ?, location = ?, reminder_minutes = ?, updated_at = ?
                WHERE id = ?
            """, (event.title, event.description, event.event_type.value,
                  event.start_time, event.end_time, event.location,
                  event.reminder_minutes, event.updated_at, event.id))
            
            conn.commit()
            logger.info(f"Event updated: {event.id}")
        
        return cursor.rowcount > 0
    
    def delete_event(self, event_id: int) -> bool:
        """Delete a calendar event."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM calendar_events WHERE id = ?", (event_id,))
            conn.commit()
            logger.info(f"Event deleted: {event_id}")
        
        return cursor.rowcount > 0
    
    def _row_to_event(self, row: tuple) -> CalendarEvent:
        """Convert database row to CalendarEvent object."""
        event = CalendarEvent(
            id=row[0],
            title=row[1],
            description=row[2],
            event_type=EventType(row[3]),
            start_time=datetime.fromisoformat(row[4]) if row[4] else None,
            end_time=datetime.fromisoformat(row[5]) if row[5] else None,
            location=row[6],
            created_at=datetime.fromisoformat(row[7]),
            updated_at=datetime.fromisoformat(row[8]),
            reminder_minutes=row[9]
        )
        return event
    
    # Memory methods
    def add_memory(self, entry: MemoryEntry) -> MemoryEntry:
        """Add a memory entry."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO memory_entries (key, value, category)
                VALUES (?, ?, ?)
            """, (entry.key, entry.value, entry.category))
            
            conn.commit()
            logger.info(f"Memory added: {entry.key}")
        
        return entry
    
    def get_memory(self, key: str) -> Optional[MemoryEntry]:
        """Get a memory entry by key."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM memory_entries WHERE key = ?", (key,))
            row = cursor.fetchone()
            
            if row:
                return self._row_to_memory(row)
        return None
    
    def get_all_memories(self) -> List[MemoryEntry]:
        """Get all memory entries."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM memory_entries ORDER BY category, key ASC")
            rows = cursor.fetchall()
            return [self._row_to_memory(row) for row in rows]
    
    def get_memories_by_category(self, category: str) -> List[MemoryEntry]:
        """Get memories by category."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM memory_entries WHERE category = ? ORDER BY key ASC",
                (category,)
            )
            rows = cursor.fetchall()
            return [self._row_to_memory(row) for row in rows]
    
    def delete_memory(self, key: str) -> bool:
        """Delete a memory entry."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM memory_entries WHERE key = ?", (key,))
            conn.commit()
            logger.info(f"Memory deleted: {key}")
        
        return cursor.rowcount > 0
    
    def _row_to_memory(self, row: tuple) -> MemoryEntry:
        """Convert database row to MemoryEntry object."""
        entry = MemoryEntry(
            id=row[0],
            key=row[1],
            value=row[2],
            category=row[3],
            created_at=datetime.fromisoformat(row[4]),
            updated_at=datetime.fromisoformat(row[5])
        )
        return entry
