from src.langgraphagenticai.state.state import State
from langchain_core.messages import SystemMessage

class ChatbotWithToolNode:
    """
    Chatbot logic enhanced with tool integration.
    """
    def __init__(self,model):
        self.llm = model

    def process(self, state: State) -> dict:
        """
        Processes the input state and generates a response with tool integration.
        """
        user_input = state["messages"][-1] if state["messages"] else ""
        llm_response = self.llm.invoke([{"role": "user", "content": user_input}])

        # Simulate tool-specific logic
        tools_response = f"Tool integration for: '{user_input}'"

        return {"messages": [llm_response, tools_response]}
    

    def create_chatbot(self, tools):
        """
        Returns a chatbot node function.
        """
        llm_with_tools = self.llm.bind_tools(tools, tool_choice="auto")

        def chatbot_node(state: State):
            """
            Chatbot logic for processing the input state and returning a response.
            """
            #return {"messages": [llm_with_tools.invoke(state["messages"])]}
            messages = state["messages"]

            system_msg = SystemMessage(content="""
                You are an AI assistant.

                You MUST ONLY use the following tools:
                - tavily_search_results_json
                - youtube_search

                Do NOT call any other tools like brave_search or browser.search.
                """)
            return {
                "messages": [
                    llm_with_tools.invoke([system_msg] + messages)
                ]
            }
        return chatbot_node

