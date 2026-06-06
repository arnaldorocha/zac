"""
Interface definitions for future Zac extensions.
These are prepared for future integrations with AI, Vision, and Plugins.
Not implemented yet - reserved for v2.0+
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from dataclasses import dataclass


@dataclass
class LLMResponse:
    """Response from LLM."""
    content: str
    tokens: int
    model: str


class LLMService(ABC):
    """
    Interface for Language Model integration.
    
    Future implementations:
    - OllamaService (local, free)
    - QwenService
    - GemmaService
    - LlamaService
    """
    
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> LLMResponse:
        """Generate text from prompt."""
        pass
    
    @abstractmethod
    def chat(self, messages: List[Dict], **kwargs) -> LLMResponse:
        """Chat with model."""
        pass
    
    @abstractmethod
    def embed(self, text: str) -> List[float]:
        """Generate embeddings."""
        pass


@dataclass
class VisionResult:
    """Vision analysis result."""
    objects: List[Dict]
    text: str
    confidence: float


class VisionService(ABC):
    """
    Interface for Computer Vision.
    
    Future implementations:
    - OpenCVService
    - YOLOService
    - TensorFlowService
    """
    
    @abstractmethod
    def detect_objects(self, image_path: str) -> VisionResult:
        """Detect objects in image."""
        pass
    
    @abstractmethod
    def extract_text(self, image_path: str) -> str:
        """Extract text from image (OCR)."""
        pass
    
    @abstractmethod
    def face_recognition(self, image_path: str) -> List[Dict]:
        """Recognize faces in image."""
        pass


@dataclass
class AgentTask:
    """Task for an agent to execute."""
    goal: str
    context: Dict[str, Any]
    tools: List[str]


@dataclass
class AgentResult:
    """Result from agent execution."""
    success: bool
    output: Any
    reasoning: str
    steps: List[str]


class AgentService(ABC):
    """
    Interface for AI Agents.
    
    Future implementations:
    - ReActAgent
    - CoTAgent
    - ToolUsingAgent
    - MultiStepAgent
    """
    
    @abstractmethod
    def execute(self, task: AgentTask) -> AgentResult:
        """Execute a task."""
        pass
    
    @abstractmethod
    def add_tool(self, name: str, description: str, callable_func) -> None:
        """Add a tool the agent can use."""
        pass
    
    @abstractmethod
    def plan(self, goal: str) -> List[str]:
        """Create a plan to achieve goal."""
        pass


class PluginService(ABC):
    """
    Interface for Plugin System.
    
    Future implementations:
    - PluginManager
    - PluginRegistry
    - PluginLoader
    """
    
    @abstractmethod
    def load_plugin(self, plugin_path: str) -> None:
        """Load a plugin."""
        pass
    
    @abstractmethod
    def execute_plugin(self, plugin_name: str, **kwargs) -> Any:
        """Execute plugin function."""
        pass
    
    @abstractmethod
    def list_plugins(self) -> List[str]:
        """List loaded plugins."""
        pass


class MemoryService(ABC):
    """
    Interface for Advanced Memory.
    
    Current implementation: SQLiteMemory
    Future implementations:
    - VectorMemory (embeddings)
    - GraphMemory (knowledge graphs)
    - HybridMemory (combined)
    """
    
    @abstractmethod
    def store(self, key: str, value: Any, metadata: Dict = None) -> None:
        """Store in memory."""
        pass
    
    @abstractmethod
    def retrieve(self, key: str) -> Optional[Any]:
        """Retrieve from memory."""
        pass
    
    @abstractmethod
    def search(self, query: str, top_k: int = 5) -> List[tuple]:
        """Search memory (semantic or keyword)."""
        pass


# Example usage (for v2.0):
"""
from core.interfaces import LLMService, VisionService, AgentService

class ZacAssistantV2(ZacAssistant):
    def __init__(self):
        super().__init__()
        
        # Add LLM
        self.llm = OllamaService(model="llama2")
        
        # Add Vision
        self.vision = OpenCVService()
        
        # Add Agent
        self.agent = ReActAgent(llm=self.llm)
        self.agent.add_tool("tasks", "Manage tasks", self.tasks.create_task)
        self.agent.add_tool("calendar", "Manage calendar", self.calendar.create_event)
        
        # Add Plugin system
        self.plugins = PluginManager()
        self.plugins.load_plugin("custom_weather.py")
    
    def process_complex_command(self, text: str):
        # Use LLM to understand
        understanding = self.llm.chat([
            {"role": "system", "content": "You are Zac assistant"},
            {"role": "user", "content": text}
        ])
        
        # Create agent task
        task = AgentTask(
            goal=understanding.content,
            context={"user_input": text},
            tools=["tasks", "calendar", "browser"]
        )
        
        # Execute with agent
        result = self.agent.execute(task)
        return result.output
"""
