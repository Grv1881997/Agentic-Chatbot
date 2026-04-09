import streamlit as st
import json
from src.langgraphagenticai.session.session_manager import SessionManager

class DisplayMessageHistory:
    def __init__(self,usecase):
        self.usecase= usecase
        self.session_manager=SessionManager()
    
    def retrive_message_history(self):
        current_session_id = self.session_manager.get_current_session_id(self.usecase)
        print("Current Session ID:", current_session_id)
        
        # Get and display the current session history
        session_history = self.session_manager.get_session_history(self.usecase, current_session_id)
        print("Session History:", session_history)
        self._display_session_history(session_history)

    def _display_session_history(self, session_history):
        """
        Display the session history
        """
        for chat in session_history:
            if chat["role"] == "user":
                with st.chat_message("user"):
                    st.write(chat["content"])
            elif chat["role"] == "assistant":
                with st.chat_message("assistant"):
                    st.write(chat["content"])
            elif chat["role"] == "tool":
                print("Tool message:", chat["content"])
                with st.chat_message("ai"):
                    st.markdown(chat["content"], unsafe_allow_html=True)

