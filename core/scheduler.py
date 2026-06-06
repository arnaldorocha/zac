"""
Scheduler for managing reminders and scheduled tasks.
"""
import logging
import threading
from typing import Callable, Optional, Dict, List
from datetime import datetime, timedelta
import time

logger = logging.getLogger(__name__)


class ScheduledTask:
    """A scheduled task."""
    
    def __init__(
        self,
        task_id: str,
        callback: Callable,
        run_at: datetime,
        recurring: bool = False,
        interval: Optional[timedelta] = None
    ):
        self.id = task_id
        self.callback = callback
        self.run_at = run_at
        self.recurring = recurring
        self.interval = interval
        self.active = True


class Scheduler:
    """Manages scheduled tasks and reminders."""
    
    def __init__(self, check_interval: int = 60):
        """
        Initialize scheduler.
        
        Args:
            check_interval: Check for scheduled tasks every N seconds
        """
        self.check_interval = check_interval
        self.tasks: Dict[str, ScheduledTask] = {}
        self.thread: Optional[threading.Thread] = None
        self.running = False
    
    def start(self) -> None:
        """Start scheduler."""
        if self.running:
            logger.warning("Scheduler already running")
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
        logger.info("Scheduler started")
    
    def stop(self) -> None:
        """Stop scheduler."""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        logger.info("Scheduler stopped")
    
    def _run(self) -> None:
        """Scheduler main loop."""
        while self.running:
            try:
                self._check_tasks()
                time.sleep(self.check_interval)
            except Exception as e:
                logger.error(f"Error in scheduler loop: {e}")
    
    def _check_tasks(self) -> None:
        """Check and execute scheduled tasks."""
        now = datetime.now()
        tasks_to_remove = []
        
        for task_id, task in self.tasks.items():
            if not task.active:
                continue
            
            if task.run_at <= now:
                try:
                    # Execute callback
                    task.callback()
                    logger.info(f"Task executed: {task_id}")
                    
                    # Handle recurring tasks
                    if task.recurring and task.interval:
                        task.run_at = now + task.interval
                    else:
                        tasks_to_remove.append(task_id)
                        
                except Exception as e:
                    logger.error(f"Error executing task {task_id}: {e}")
                    tasks_to_remove.append(task_id)
        
        # Remove completed non-recurring tasks
        for task_id in tasks_to_remove:
            del self.tasks[task_id]
    
    def schedule_once(
        self,
        task_id: str,
        callback: Callable,
        run_at: datetime
    ) -> None:
        """Schedule a one-time task."""
        task = ScheduledTask(
            task_id=task_id,
            callback=callback,
            run_at=run_at,
            recurring=False
        )
        self.tasks[task_id] = task
        logger.info(f"Task scheduled: {task_id} at {run_at}")
    
    def schedule_recurring(
        self,
        task_id: str,
        callback: Callable,
        start_at: datetime,
        interval: timedelta
    ) -> None:
        """Schedule a recurring task."""
        task = ScheduledTask(
            task_id=task_id,
            callback=callback,
            run_at=start_at,
            recurring=True,
            interval=interval
        )
        self.tasks[task_id] = task
        logger.info(f"Recurring task scheduled: {task_id} every {interval}")
    
    def schedule_in(
        self,
        task_id: str,
        callback: Callable,
        seconds: int
    ) -> None:
        """Schedule a task to run after N seconds."""
        run_at = datetime.now() + timedelta(seconds=seconds)
        self.schedule_once(task_id, callback, run_at)
    
    def schedule_at_time(
        self,
        task_id: str,
        callback: Callable,
        hour: int,
        minute: int
    ) -> None:
        """Schedule a task to run at specific time today."""
        now = datetime.now()
        run_at = now.replace(hour=hour, minute=minute, second=0)
        
        # If time already passed, schedule for tomorrow
        if run_at < now:
            run_at += timedelta(days=1)
        
        self.schedule_once(task_id, callback, run_at)
    
    def cancel_task(self, task_id: str) -> bool:
        """Cancel a scheduled task."""
        if task_id in self.tasks:
            del self.tasks[task_id]
            logger.info(f"Task cancelled: {task_id}")
            return True
        return False
    
    def get_tasks(self) -> List[ScheduledTask]:
        """Get all scheduled tasks."""
        return list(self.tasks.values())
    
    def get_pending_tasks(self) -> List[ScheduledTask]:
        """Get tasks that are pending execution."""
        now = datetime.now()
        return [task for task in self.tasks.values() if task.run_at <= now]
