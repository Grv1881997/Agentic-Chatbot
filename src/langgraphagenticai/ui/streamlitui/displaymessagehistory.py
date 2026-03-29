import streamlit as st
import json


class DisplayMessageHistory:
    def __init__(self,usecase):
        self.usecase= usecase
    
    def retrive_message_history(self):
        print(" **Usecase Selected:", self.usecase)
        if self.usecase =="Basic Chatbot":
            if "basic_chatbot_history" not in st.session_state:
                st.session_state["basic_chatbot_history"] = []

            # Display the Basic Chatbot history
            for chat in st.session_state["basic_chatbot_history"]:
                if chat["role"] == "user":
                    with st.chat_message("user"):
                        st.write(chat["content"])
                elif chat["role"] == "assistant":
                    with st.chat_message("assistant"):
                        st.write(chat["content"])

        elif self.usecase=="Chatbot With Web":
            if "chatbot_with_web_history" not in st.session_state:
                st.session_state["chatbot_with_web_history"] = []

            # Display the Chatbot With Web history
            for chat in st.session_state["chatbot_with_web_history"]:
                if chat["role"] == "user":
                    with st.chat_message("user"):
                        st.write(chat["content"])
                elif chat["role"] == "assistant":
                    with st.chat_message("assistant"):
                        st.write(chat["content"])
                elif chat["role"] == "tool":
                    with st.chat_message("ai"):
                        st.write("Tool Call Start")
                        st.write(chat["content"])
                        st.write("Tool Call End")
