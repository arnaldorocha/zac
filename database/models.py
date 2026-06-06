"""
Database models for Zac Personal Assistant.
"""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class TaskStatus(str, Enum):
    """Task status enumeration."""
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class TaskPriority(str, Enum):
    """Task priority enumeration."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class EventType(str, Enum):
    """Event type enumeration."""
    APPOINTMENT = "appointment"
    REMINDER = "reminder"
    MEETING = "meeting"
    DEADLINE = "deadline"
    BIRTHDAY = "birthday"
    OTHER = "other"


@dataclass
class Task:
    """Task data model."""
    id: Optional[int] = None
    title: str = ""
    description: str = ""
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    tags: list[str] = field(default_factory=list)


@dataclass
class CalendarEvent:
    """Calendar event data model."""
    id: Optional[int] = None
    title: str = ""
    description: str = ""
    event_type: EventType = EventType.APPOINTMENT
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    location: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    reminder_minutes: int = 15


@dataclass
class MemoryEntry:
    """Memory entry data model."""
    id: Optional[int] = None
    key: str = ""
    value: str = ""
    category: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass
class ExpenseRecord:
    """Expense record for Google Sheets integration."""
    date: datetime
    category: str
    description: str
    amount: float


@dataclass
class StudyRecord:
    """Study record for Google Sheets integration."""
    date: datetime
    discipline: str
    hours: float


@dataclass
class GoalRecord:
    """Goal record for Google Sheets integration."""
    date: datetime
    goal: str
    status: str
