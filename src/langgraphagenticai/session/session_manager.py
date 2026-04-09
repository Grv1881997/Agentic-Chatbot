import streamlit as st
import uuid
from typing import Dict, List, Optional
from datetime import datetime


class SessionManager:
    """
    Manages chat sessions with unique IDs for different use cases.
    Each use case (Basic Chatbot, Chatbot With Web) can have multiple independent sessions.
    """
    
    def __init__(self):
        self.session_prefix = {
            "Basic Chatbot": "basic_chatbot",
            "Chatbot With Web": "chatbot_with_web"
        }
    
    def generate_session_id(self) -> str:
        """Generate a unique session ID"""
        return str(uuid.uuid4())[:8]
    
    def get_current_session_id(self, usecase: str) -> str:
        """Get the current active session ID for a use case"""
        session_key = f"{self.session_prefix.get(usecase, 'chatbot')}_current_session"
        if session_key not in st.session_state:
            # Create a new session if none exists
            new_session_id = self.generate_session_id()
            st.session_state[session_key] = new_session_id
            self.initialize_session_history(usecase, new_session_id)
        return st.session_state[session_key]
    
    def set_current_session_id(self, usecase: str, session_id: str):
        """Set the current active session ID for a use case"""
        session_key = f"{self.session_prefix.get(usecase, 'chatbot')}_current_session"
        st.session_state[session_key] = session_id
        # Initialize session if it doesn't exist
        self.initialize_session_history(usecase, session_id)
    
    def get_all_sessions(self, usecase: str) -> Dict[str, Dict]:
        """Get all sessions for a use case with their metadata"""
        sessions_key = f"{self.session_prefix.get(usecase, 'chatbot')}_sessions"
        if sessions_key not in st.session_state:
            st.session_state[sessions_key] = {}
        return st.session_state[sessions_key]
    
    def create_new_session(self, usecase: str) -> str:
        """Create a new session for a use case and return its ID"""
        session_id = self.generate_session_id()
        self.initialize_session_history(usecase, session_id)
        
        # Add to sessions list with metadata
        sessions = self.get_all_sessions(usecase)
        sessions[session_id] = {
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "message_count": 0,
            "last_activity": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Set as current session
        self.set_current_session_id(usecase, session_id)
        
        return session_id
    
    def initialize_session_history(self, usecase: str, session_id: str):
        """Initialize chat history for a specific session"""
        history_key = f"{self.session_prefix.get(usecase, 'chatbot')}_history_{session_id}"
        if history_key not in st.session_state:
            st.session_state[history_key] = []
    
    def get_session_history(self, usecase: str, session_id: str) -> List[Dict]:
        """Get chat history for a specific session"""
        history_key = f"{self.session_prefix.get(usecase, 'chatbot')}_history_{session_id}"
        return st.session_state.get(history_key, [])
    
    def add_message_to_session(self, usecase: str, session_id: str, role: str, content: str):
        """Add a message to a specific session's history"""
        history_key = f"{self.session_prefix.get(usecase, 'chatbot')}_history_{session_id}"
        if history_key not in st.session_state:
            st.session_state[history_key] = []
        
        st.session_state[history_key].append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        # Update session metadata
        sessions = self.get_all_sessions(usecase)
        if session_id in sessions:
            sessions[session_id]["message_count"] = len(st.session_state[history_key])
            sessions[session_id]["last_activity"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def delete_session(self, usecase: str, session_id: str) -> bool:
        """Delete a session and its history"""
        try:
            # Remove history
            history_key = f"{self.session_prefix.get(usecase, 'chatbot')}_history_{session_id}"
            if history_key in st.session_state:
                del st.session_state[history_key]
            
            # Remove from sessions list
            sessions = self.get_all_sessions(usecase)
            if session_id in sessions:
                del sessions[session_id]
            
            # If this was the current session, switch to another or create new
            current_session = self.get_current_session_id(usecase)
            if current_session == session_id:
                if sessions:
                    # Switch to the most recently active session
                    latest_session = max(sessions.keys(), 
                                       key=lambda sid: sessions[sid]["last_activity"])
                    self.set_current_session_id(usecase, latest_session)
                else:
                    # Create a new session if no sessions left
                    self.create_new_session(usecase)
            
            return True
        except Exception as e:
            print(f"Error deleting session {session_id}: {e}")
            return False
    
    def get_session_display_name(self, usecase: str, session_id: str) -> str:
        """Get a display name for a session"""
        sessions = self.get_all_sessions(usecase)
        if session_id in sessions:
            session_info = sessions[session_id]
            return f"Session {session_id[:6]} ({session_info['message_count']} messages)"
        return f"Session {session_id[:6]}"
