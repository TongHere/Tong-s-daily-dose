import openai
import logging
import os
from typing import Tuple, List, Dict, Optional

logger = logging.getLogger(__name__)

class TongChatbot:
    """A chatbot class that handles OpenAI API interactions for Tong's blog."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        """
        Initialize the chatbot.
        
        Args:
            api_key: OpenAI API key (optional, falls back to env variable)
            model: OpenAI model to use
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.model = model
        self.system_prompt = "You are a helpful assistant for TongHere blog. Keep responses concise and friendly."
        
        if self.api_key:
            openai.api_key = self.api_key
    
    def get_response(self, user_message: str, conversation: List[Dict[str, str]] = None) -> Tuple[Optional[str], Optional[str]]:
        """
        Get a response from OpenAI API.
        
        Args:
            user_message: The user's input message
            conversation: List of previous messages [{'role': 'user'/'assistant', 'content': str}]
            
        Returns:
            Tuple of (assistant_message, error). If error is None, assistant_message contains the response.
        """
        if not self.api_key:
            return None, "OpenAI API key not configured"
        
        if not user_message.strip():
            return None, "Empty message provided"
        
        conversation = conversation or []
        
        try:
            # Build messages for OpenAI
            messages = [{"role": m["role"], "content": m["content"]} for m in conversation]
            messages.append({"role": "user", "content": user_message})
            
            logger.info(f"Processing chat message: {user_message[:50]}...")
            
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    *messages
                ],
                max_tokens=150,
                temperature=0.7,
                timeout=10
            )
            
            assistant_message = response.choices[0].message.content if response.choices else None
            
            if assistant_message:
                logger.info(f"OpenAI response: {assistant_message}")
                return assistant_message, None
            else:
                logger.error("No response from OpenAI API")
                return None, "No response from OpenAI API"
                
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            return None, f"OpenAI API error: {str(e)}"
    
    def is_configured(self) -> bool:
        """Check if the chatbot is properly configured."""
        return bool(self.api_key)

# Global chatbot instance
chatbot = TongChatbot()

def get_chat_response(user_message: str, conversation: List[Dict[str, str]] = None) -> Tuple[Optional[str], Optional[str]]:
    """
    Convenience function to get a chat response.
    
    Args:
        user_message: The user's input message
        conversation: List of previous messages
        
    Returns:
        Tuple of (assistant_message, error)
    """
    return chatbot.get_response(user_message, conversation)

def is_chatbot_configured() -> bool:
    """Check if the chatbot is properly configured."""
    return chatbot.is_configured() 