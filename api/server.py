"""
FastAPI server for Zac Personal Assistant.
Provides REST API for remote control and integration.
"""
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from core.assistant import ZacAssistant
from database.models import TaskPriority, EventType

logger = logging.getLogger(__name__)

# Initialize assistant
assistant = ZacAssistant()

# Initialize FastAPI
app = FastAPI(
    title="Zac Personal Assistant API",
    description="API for controlling Zac personal assistant",
    version="1.0.0"
)


# Models
class TaskRequest(BaseModel):
    """Task request model."""
    title: str
    description: Optional[str] = ""
    priority: Optional[str] = "medium"
    due_date: Optional[str] = None
    tags: Optional[List[str]] = []


class TaskResponse(BaseModel):
    """Task response model."""
    id: Optional[int]
    title: str
    status: str
    priority: str


class EventRequest(BaseModel):
    """Event request model."""
    title: str
    description: Optional[str] = ""
    start_time: str
    end_time: Optional[str] = None
    location: Optional[str] = ""


class CommandRequest(BaseModel):
    """Command request model."""
    text: str


class ResponseMessage(BaseModel):
    """Response message model."""
    message: str
    success: bool = True


# Health check
@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "online", "assistant": "Zac"}


# Commands
@app.post("/command")
async def execute_command(request: CommandRequest) -> ResponseMessage:
    """Execute a voice command."""
    try:
        result = assistant.process_command(request.text)
        return ResponseMessage(message=result or "Command executed", success=True)
    except Exception as e:
        logger.error(f"Error executing command: {e}")
        return ResponseMessage(message=str(e), success=False)


@app.post("/listen")
async def listen():
    """Listen for voice command."""
    try:
        result = assistant.listen_and_execute()
        return ResponseMessage(message=result or "Listening...", success=True)
    except Exception as e:
        logger.error(f"Error listening: {e}")
        return ResponseMessage(message=str(e), success=False)


# Tasks
@app.post("/tasks")
async def create_task(task: TaskRequest) -> TaskResponse:
    """Create a new task."""
    try:
        priority = TaskPriority(task.priority.lower())
        due_date = None
        if task.due_date:
            due_date = datetime.fromisoformat(task.due_date)
        
        created_task = assistant.tasks.create_task(
            title=task.title,
            description=task.description,
            priority=priority,
            due_date=due_date,
            tags=task.tags
        )
        
        return TaskResponse(
            id=created_task.id,
            title=created_task.title,
            status=created_task.status.value,
            priority=created_task.priority.value
        )
    except Exception as e:
        logger.error(f"Error creating task: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/tasks")
async def get_tasks():
    """Get all tasks."""
    try:
        tasks = assistant.tasks.get_all_tasks()
        return {
            "count": len(tasks),
            "tasks": [
                {
                    "id": t.id,
                    "title": t.title,
                    "status": t.status.value,
                    "priority": t.priority.value,
                    "due_date": t.due_date.isoformat() if t.due_date else None
                }
                for t in tasks
            ]
        }
    except Exception as e:
        logger.error(f"Error getting tasks: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/tasks/today")
async def get_today_tasks():
    """Get today's tasks."""
    try:
        tasks = assistant.tasks.get_today_tasks()
        return {
            "count": len(tasks),
            "tasks": [
                {
                    "id": t.id,
                    "title": t.title,
                    "status": t.status.value,
                    "priority": t.priority.value
                }
                for t in tasks
            ]
        }
    except Exception as e:
        logger.error(f"Error getting today's tasks: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.patch("/tasks/{task_id}/complete")
async def complete_task(task_id: int):
    """Complete a task."""
    try:
        success = assistant.tasks.complete_task(task_id)
        if success:
            return ResponseMessage(message=f"Task {task_id} completed")
        else:
            return ResponseMessage(message=f"Task {task_id} not found", success=False)
    except Exception as e:
        logger.error(f"Error completing task: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    """Delete a task."""
    try:
        success = assistant.tasks.delete_task(task_id)
        if success:
            return ResponseMessage(message=f"Task {task_id} deleted")
        else:
            return ResponseMessage(message=f"Task {task_id} not found", success=False)
    except Exception as e:
        logger.error(f"Error deleting task: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# Calendar
@app.post("/events")
async def create_event(event: EventRequest):
    """Create calendar event."""
    try:
        start_time = datetime.fromisoformat(event.start_time)
        end_time = None
        if event.end_time:
            end_time = datetime.fromisoformat(event.end_time)
        
        created_event = assistant.calendar.create_event(
            title=event.title,
            start_time=start_time,
            end_time=end_time,
            description=event.description,
            location=event.location
        )
        
        return {
            "id": created_event.id,
            "title": created_event.title,
            "start_time": created_event.start_time.isoformat()
        }
    except Exception as e:
        logger.error(f"Error creating event: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/events")
async def get_events():
    """Get all events."""
    try:
        events = assistant.calendar.get_all_events()
        return {
            "count": len(events),
            "events": [
                {
                    "id": e.id,
                    "title": e.title,
                    "start_time": e.start_time.isoformat() if e.start_time else None,
                    "location": e.location
                }
                for e in events
            ]
        }
    except Exception as e:
        logger.error(f"Error getting events: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/events/today")
async def get_today_events():
    """Get today's events."""
    try:
        events = assistant.calendar.get_today_events()
        return {
            "count": len(events),
            "events": [
                {
                    "id": e.id,
                    "title": e.title,
                    "start_time": e.start_time.isoformat() if e.start_time else None
                }
                for e in events
            ]
        }
    except Exception as e:
        logger.error(f"Error getting today's events: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# Memory
@app.post("/memory")
async def save_memory(key: str, value: str, category: str = "general"):
    """Save memory entry."""
    try:
        entry = assistant.memory.save_memory(key, value, category)
        return ResponseMessage(message=f"Memory saved: {key}")
    except Exception as e:
        logger.error(f"Error saving memory: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/memory/{key}")
async def get_memory(key: str):
    """Get memory entry."""
    try:
        entry = assistant.memory.get_memory(key)
        if entry:
            return {
                "key": entry.key,
                "value": entry.value,
                "category": entry.category
            }
        else:
            raise HTTPException(status_code=404, detail="Memory entry not found")
    except Exception as e:
        logger.error(f"Error getting memory: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/memory")
async def list_memories(category: Optional[str] = None):
    """List memory entries."""
    try:
        if category:
            entries = assistant.memory.get_memories_by_category(category)
        else:
            entries = assistant.memory.get_all_memories()
        
        return {
            "count": len(entries),
            "entries": [
                {
                    "key": e.key,
                    "value": e.value,
                    "category": e.category
                }
                for e in entries
            ]
        }
    except Exception as e:
        logger.error(f"Error listing memories: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# Browser
@app.post("/browser/open")
async def open_browser(url: Optional[str] = None):
    """Open browser."""
    try:
        assistant.browser.open_browser(url)
        return ResponseMessage(message="Browser opened")
    except Exception as e:
        logger.error(f"Error opening browser: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/browser/navigate")
async def navigate(url: str):
    """Navigate to URL."""
    try:
        assistant.browser.navigate(url)
        return ResponseMessage(message=f"Navigating to {url}")
    except Exception as e:
        logger.error(f"Error navigating: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/browser/close")
async def close_browser():
    """Close browser."""
    try:
        assistant.browser.close_browser()
        return ResponseMessage(message="Browser closed")
    except Exception as e:
        logger.error(f"Error closing browser: {e}")
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
