"""
Memory service for personal knowledge management.
"""
import logging
from typing import Optional, List
from datetime import datetime

from database.sqlite_manager import SQLiteManager
from database.models import MemoryEntry

logger = logging.getLogger(__name__)


class MemoryService:
    """Manages personal memories and knowledge."""
    
    def __init__(self, db_manager: SQLiteManager):
        """
        Initialize memory service.
        
        Args:
            db_manager: SQLite database manager
        """
        self.db = db_manager
    
    def save_memory(
        self,
        key: str,
        value: str,
        category: str = "general"
    ) -> MemoryEntry:
        """Save a memory entry."""
        entry = MemoryEntry(
            key=key,
            value=value,
            category=category
        )
        
        self.db.add_memory(entry)
        logger.info(f"Memory saved: {key}")
        return entry
    
    def get_memory(self, key: str) -> Optional[MemoryEntry]:
        """Get memory by key."""
        return self.db.get_memory(key)
    
    def get_memory_value(self, key: str) -> Optional[str]:
        """Get memory value by key."""
        entry = self.db.get_memory(key)
        return entry.value if entry else None
    
    def get_all_memories(self) -> List[MemoryEntry]:
        """Get all memories."""
        return self.db.get_all_memories()
    
    def get_memories_by_category(self, category: str) -> List[MemoryEntry]:
        """Get memories by category."""
        return self.db.get_memories_by_category(category)
    
    def save_important_person(self, name: str, info: str) -> MemoryEntry:
        """Save important person information."""
        return self.save_memory(
            key=f"person_{name.lower()}",
            value=info,
            category="pessoas"
        )
    
    def save_goal(self, goal_name: str, description: str) -> MemoryEntry:
        """Save a goal."""
        return self.save_memory(
            key=f"goal_{goal_name.lower()}",
            value=description,
            category="metas"
        )
    
    def save_preference(self, preference_name: str, value: str) -> MemoryEntry:
        """Save a preference."""
        return self.save_memory(
            key=f"pref_{preference_name.lower()}",
            value=value,
            category="preferências"
        )
    
    def save_useful_info(self, topic: str, info: str) -> MemoryEntry:
        """Save useful information."""
        return self.save_memory(
            key=f"info_{topic.lower()}",
            value=info,
            category="informações"
        )
    
    def get_important_people(self) -> List[MemoryEntry]:
        """Get all important people."""
        return self.get_memories_by_category("pessoas")
    
    def get_goals(self) -> List[MemoryEntry]:
        """Get all goals."""
        return self.get_memories_by_category("metas")
    
    def get_preferences(self) -> List[MemoryEntry]:
        """Get all preferences."""
        return self.get_memories_by_category("preferências")
    
    def get_useful_info(self) -> List[MemoryEntry]:
        """Get all useful information."""
        return self.get_memories_by_category("informações")
    
    def update_memory(self, key: str, value: str) -> Optional[MemoryEntry]:
        """Update memory value."""
        entry = self.db.get_memory(key)
        if not entry:
            logger.warning(f"Memory key not found: {key}")
            return None
        
        entry.value = value
        entry.updated_at = datetime.now()
        self.db.add_memory(entry)
        logger.info(f"Memory updated: {key}")
        return entry
    
    def delete_memory(self, key: str) -> bool:
        """Delete memory entry."""
        return self.db.delete_memory(key)
    
    def search_memory(self, query: str) -> List[MemoryEntry]:
        """Search memories."""
        all_memories = self.get_all_memories()
        query_lower = query.lower()
        return [
            entry for entry in all_memories
            if query_lower in entry.key.lower()
            or query_lower in entry.value.lower()
        ]
