from langgraph.prebuilt import ToolNode
from src.langgraphagenticai.tools.search_tool import get_tavily_tools
from src.langgraphagenticai.tools.youtube_tool import get_youtube_tools

def get_tools():
    """
    Return the list of tools to be used in the chatbot
    """
    return [
        *get_youtube_tools(),
        *get_tavily_tools()
    ]

def create_tool_node(tools):
    """
    creates and returns a tool node for the graph
    """
    return ToolNode(tools=tools)

