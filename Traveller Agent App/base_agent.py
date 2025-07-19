import google.generativeai as genai
import asyncio
import json
from typing import Dict, Any, Optional, List
from abc import ABC, abstractmethod
from datetime import datetime

from config import Config
from models import AgentResponse

class BaseAgent(ABC):
    """Base class for all travel agents with common functionality"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.model = None
        self.tools = []
        self.conversation_history = []
        
        # Initialize Gemini API
        if Config.GEMINI_API_KEY:
            genai.configure(api_key=Config.GEMINI_API_KEY)
            self.model = genai.GenerativeModel(Config.GEMINI_MODEL)
        else:
            print(f"Warning: {name} agent initialized without Gemini API key")
    
    def add_tool(self, tool: Dict[str, Any]):
        """Add a tool to the agent's toolkit"""
        self.tools.append(tool)
    
    def add_to_history(self, role: str, content: str):
        """Add a message to the conversation history"""
        self.conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
    
    async def call_gemini(self, prompt: str, context: Optional[str] = None) -> str:
        """Make a call to the Gemini API"""
        if not self.model:
            return f"Mock response from {self.name}: {prompt}"
        
        try:
            full_prompt = self._build_prompt(prompt, context)
            response = await asyncio.to_thread(
                self.model.generate_content,
                full_prompt
            )
            return response.text
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            return f"Error: Unable to process request - {str(e)}"
    
    def _build_prompt(self, prompt: str, context: Optional[str] = None) -> str:
        """Build a comprehensive prompt with context and tools"""
        system_prompt = f"""You are {self.name}, a specialized travel agent with the following description: {self.description}

Your role is to help users with their travel needs by providing accurate, helpful, and personalized recommendations.

Available tools: {json.dumps(self.tools, indent=2) if self.tools else 'None'}

Please respond in a helpful, professional manner. If you need to use tools, specify which tool and provide the necessary parameters.
"""
        
        if context:
            system_prompt += f"\nContext: {context}\n"
        
        if self.conversation_history:
            system_prompt += "\nConversation History:\n"
            for msg in self.conversation_history[-5:]:  # Last 5 messages
                system_prompt += f"{msg['role']}: {msg['content']}\n"
        
        return f"{system_prompt}\n\nUser Request: {prompt}\n\nResponse:"
    
    def create_response(self, success: bool, message: str, data: Optional[Any] = None) -> AgentResponse:
        """Create a standardized agent response"""
        return AgentResponse(
            success=success,
            message=message,
            data=data,
            agent_name=self.name
        )
    
    @abstractmethod
    async def process_request(self, request: Any) -> AgentResponse:
        """Process a request and return a response - to be implemented by subclasses"""
        pass
    
    def get_agent_info(self) -> Dict[str, Any]:
        """Get information about this agent"""
        return {
            "name": self.name,
            "description": self.description,
            "tools": [tool.get("name", "Unknown") for tool in self.tools],
            "conversation_history_length": len(self.conversation_history)
        } 