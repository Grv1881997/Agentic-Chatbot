import streamlit as st
import os
from src.langgraphagenticai.graph.graph_builder import GraphBuilder
from src.langgraphagenticai.ui.streamlitui.display_result import DisplayResultStreamlit
from src.langgraphagenticai.ui.streamlitui.displaymessagehistory import DisplayMessageHistory

from src.langgraphagenticai.ui.uiconfigfile import Config

class LoadStreamlitUI:
    def __init__(self):
        self.config=Config()
        self.user_controls={}

    def load_streamlit_ui(self):
        st.set_page_config(page_title= "🤖 " + self.config.get_page_title(), layout="wide")
        st.header("🤖 " + self.config.get_page_title())
        st.session_state.timeframe = ''
        st.session_state.IsFetchButtonClicked = False


        with st.sidebar:
            # Get options from config
            llm_options = self.config.get_llm_options()
            usecase_options = self.config.get_usecase_options()

            # LLM selection
            self.user_controls["selected_llm"] = st.selectbox("Select LLM", llm_options)

            if self.user_controls["selected_llm"] == 'Groq':
                # Model selection
                model_options = self.config.get_groq_model_options()
                self.user_controls["selected_groq_model"] = st.selectbox("Select Model", model_options)
                self.user_controls["GROQ_API_KEY"] = st.session_state["GROQ_API_KEY"]= self.config.get_groq_key() #st.text_input("API Key",type="password")
                # Validate API key
                if not self.user_controls["GROQ_API_KEY"]:
                    st.warning("⚠️ Please enter your GROQ API key to proceed. Don't have? refer : https://console.groq.com/keys ")
            
            ## USecase selection
            self.user_controls["selected_usecase"]=st.selectbox("Select Usecases",usecase_options)

            if self.user_controls["selected_usecase"] =="Chatbot With Web" or self.user_controls["selected_usecase"] =="AI News" :
                os.environ["TAVILY_API_KEY"]=self.user_controls["TAVILY_API_KEY"]=st.session_state["TAVILY_API_KEY"]=self.config.get_tavily_key() #st.text_input("TAVILY API KEY",type="password")

                # Validate API key
                if not self.user_controls["TAVILY_API_KEY"]:
                    st.warning("⚠️ Please enter your TAVILY_API_KEY key to proceed. Don't have? refer : https://app.tavily.com/home")

            if self.user_controls['selected_usecase']=="AI News":
                st.subheader("📰 AI News Explorer ")
                
                with st.sidebar:
                    time_frame = st.selectbox(
                        "📅 Select Time Frame",
                        ["Daily", "Weekly", "Monthly"],
                        index=0
                    )
                if st.button("🔍 Fetch Latest AI News", use_container_width=True):
                    st.session_state.IsFetchButtonClicked = True
                    st.session_state.timeframe = time_frame

        if self.user_controls["selected_usecase"] =="Basic Chatbot":
            # Call the main logic to retrieve and display message history for Chatbot With Web use case
            DisplayMessageHistory("Basic Chatbot").retrive_message_history()
            # Call the main logic to set up the graph and display the result
            # graph_builder = GraphBuilder(self.user_controls["selected_llm"])
            # graph = graph_builder.setup_graph("Basic Chatbot")
            # DisplayResultStreamlit("Basic Chatbot", graph, "").display_result_on_ui()

        elif self.user_controls["selected_usecase"] =="Chatbot With Web":
            # Call the main logic to retrieve and display message history for Chatbot With Web use case
            DisplayMessageHistory("Chatbot With Web").retrive_message_history()

        return self.user_controls