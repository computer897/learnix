"""
Chat History Management for Learnix
Stores and retrieves conversation history with timestamps
"""
import json
import os
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class ChatHistory:
    """Manages chat history storage and retrieval."""
    
    def __init__(self, storage_dir: Path):
        self.storage_dir = storage_dir
        self.storage_dir.mkdir(exist_ok=True)
        self.history_file = self.storage_dir / "chat_history.json"
        self.max_messages = 50  # Store last 50 messages per session
        self._ensure_history_file()
    
    def _ensure_history_file(self):
        """Create history file if it doesn't exist."""
        if not self.history_file.exists():
            self._save_history([])
    
    def _load_history(self) -> List[Dict]:
        """Load chat history from file."""
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading chat history: {e}")
            return []
    
    def _save_history(self, history: List[Dict]):
        """Save chat history to file."""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error saving chat history: {e}")
    
    def add_message(self, question: str, answer: str, sources: Optional[List[str]] = None) -> Dict:
        """Add a new Q&A pair to history."""
        message = {
            "id": f"msg_{datetime.now().timestamp()}",
            "timestamp": datetime.now().isoformat(),
            "question": question,
            "answer": answer,
            "sources": sources or []
        }
        
        history = self._load_history()
        history.append(message)
        
        # Keep only last N messages
        if len(history) > self.max_messages:
            history = history[-self.max_messages:]
        
        self._save_history(history)
        logger.info(f"Added message to history: {message['id']}")
        return message
    
    def get_history(self, limit: int = 20) -> List[Dict]:
        """Get recent chat history (limited to last N messages)."""
        history = self._load_history()
        return history[-limit:] if limit else history
    
    def clear_history(self) -> bool:
        """Clear all chat history."""
        try:
            self._save_history([])
            logger.info("Chat history cleared")
            return True
        except Exception as e:
            logger.error(f"Error clearing chat history: {e}")
            return False
    
    def get_message_by_id(self, message_id: str) -> Optional[Dict]:
        """Get a specific message by ID."""
        history = self._load_history()
        for msg in history:
            if msg.get("id") == message_id:
                return msg
        return None
    
    def delete_message(self, message_id: str) -> bool:
        """Delete a specific message from history."""
        try:
            history = self._load_history()
            history = [msg for msg in history if msg.get("id") != message_id]
            self._save_history(history)
            logger.info(f"Deleted message: {message_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting message: {e}")
            return False
    
    def get_stats(self) -> Dict:
        """Get statistics about chat history."""
        history = self._load_history()
        return {
            "total_messages": len(history),
            "oldest_message": history[0]["timestamp"] if history else None,
            "newest_message": history[-1]["timestamp"] if history else None
        }
