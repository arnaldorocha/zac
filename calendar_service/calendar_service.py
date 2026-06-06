"""
Calendar service for event management.
"""
import logging
from typing import Optional, List
from datetime import datetime

from database.sqlite_manager import SQLiteManager
from database.models import CalendarEvent, EventType

logger = logging.getLogger(__name__)


class CalendarService:
    """Manages calendar events."""
    
    def __init__(self, db_manager: SQLiteManager):
        """
        Initialize calendar service.
        
        Args:
            db_manager: SQLite database manager
        """
        self.db = db_manager
    
    def create_event(
        self,
        title: str,
        start_time: datetime,
        end_time: Optional[datetime] = None,
        description: str = "",
        event_type: EventType = EventType.APPOINTMENT,
        location: str = "",
        reminder_minutes: int = 15
    ) -> CalendarEvent:
        """Create new calendar event."""
        event = CalendarEvent(
            title=title,
            start_time=start_time,
            end_time=end_time,
            description=description,
            event_type=event_type,
            location=location,
            reminder_minutes=reminder_minutes
        )
        
        self.db.add_event(event)
        logger.info(f"Event created: {title}")
        return event
    
    def get_event(self, event_id: int) -> Optional[CalendarEvent]:
        """Get event by ID."""
        return self.db.get_event(event_id)
    
    def get_all_events(self) -> List[CalendarEvent]:
        """Get all events."""
        return self.db.get_all_events()
    
    def get_today_events(self) -> List[CalendarEvent]:
        """Get today's events."""
        today = datetime.now().date()
        events = self.db.get_all_events()
        return [
            event for event in events
            if event.start_time and event.start_time.date() == today
        ]
    
    def get_upcoming_events(self, days: int = 7) -> List[CalendarEvent]:
        """Get upcoming events within N days."""
        today = datetime.now().date()
        events = self.db.get_all_events()
        upcoming = []
        
        for event in events:
            if event.start_time:
                event_date = event.start_time.date()
                days_ahead = (event_date - today).days
                if 0 <= days_ahead < days:
                    upcoming.append(event)
        
        return sorted(upcoming, key=lambda e: e.start_time or datetime.now())
    
    def update_event(
        self,
        event_id: int,
        title: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        description: Optional[str] = None,
        location: Optional[str] = None
    ) -> bool:
        """Update event."""
        event = self.db.get_event(event_id)
        if not event:
            logger.warning(f"Event {event_id} not found")
            return False
        
        if title:
            event.title = title
        if start_time:
            event.start_time = start_time
        if end_time:
            event.end_time = end_time
        if description:
            event.description = description
        if location:
            event.location = location
        
        event.updated_at = datetime.now()
        self.db.update_event(event)
        logger.info(f"Event updated: {event_id}")
        return True
    
    def delete_event(self, event_id: int) -> bool:
        """Delete event."""
        return self.db.delete_event(event_id)
    
    def search_events(self, query: str) -> List[CalendarEvent]:
        """Search events by title or description."""
        all_events = self.db.get_all_events()
        query_lower = query.lower()
        return [
            event for event in all_events
            if query_lower in event.title.lower()
            or query_lower in event.description.lower()
        ]
    
    def get_reminders(self) -> List[CalendarEvent]:
        """Get events that need reminders."""
        now = datetime.now()
        events = self.db.get_all_events()
        reminders = []
        
        for event in events:
            if event.start_time:
                time_until = event.start_time - now
                minutes_until = time_until.total_seconds() / 60
                
                if 0 < minutes_until <= event.reminder_minutes:
                    reminders.append(event)
        
        return reminders
