import google.generativeai as genai
from typing import List, Dict, Any
import config

class GeminiClient:
    def __init__(self):
        """Initialize the Gemini client with API key."""
        if not config.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=config.GEMINI_API_KEY)
        # Try different model names for compatibility
        try:
            self.model = genai.GenerativeModel('gemini-pro')
        except Exception:
            try:
                self.model = genai.GenerativeModel('gemini-1.5-pro')
            except Exception:
                self.model = genai.GenerativeModel('gemini-1.0-pro')
    
    def generate_response(self, prompt: str, context: str = "") -> str:
        """
        Generate a response using Gemini API.
        
        Args:
            prompt: The main prompt/question
            context: Additional context or system instructions
            
        Returns:
            Generated response as string
        """
        try:
            full_prompt = f"{context}\n\n{prompt}" if context else prompt
            response = self.model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def generate_structured_response(self, prompt: str, context: str = "", 
                                   response_format: str = "text") -> Dict[str, Any]:
        """
        Generate a structured response with specific formatting.
        
        Args:
            prompt: The main prompt/question
            context: Additional context
            response_format: Expected format (json, list, etc.)
            
        Returns:
            Structured response as dictionary
        """
        try:
            format_instruction = ""
            if response_format == "json":
                format_instruction = "\n\nPlease respond in valid JSON format."
            elif response_format == "list":
                format_instruction = "\n\nPlease respond with a clear list format."
            
            full_prompt = f"{context}{format_instruction}\n\n{prompt}"
            response = self.model.generate_content(full_prompt)
            
            return {
                "success": True,
                "response": response.text,
                "format": response_format
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "response": ""
            }
    
    def chat_conversation(self, messages: List[Dict[str, str]]) -> str:
        """
        Handle a conversation with multiple messages.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            
        Returns:
            Generated response as string
        """
        try:
            chat = self.model.start_chat(history=[])
            
            for message in messages:
                if message['role'] == 'user':
                    response = chat.send_message(message['content'])
            
            return response.text
        except Exception as e:
            return f"Error in chat conversation: {str(e)}" 