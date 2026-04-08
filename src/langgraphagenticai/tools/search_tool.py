from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import ToolNode

def get_tools():
    """
    Return the list of tools to be used in the chatbot
    """
    tool = [TavilySearchResults(max_results=2)]
    print("Tools loaded:", tool)
    return tool

def get_tavily_tools():
    """
    Return the list of tools to be used in the chatbot for tavily search
    """
    tools=[TavilySearchResults(max_results=2)]
    return tools

def create_tool_node(tools):
    """
    creates and returns a tool node for the graph
    """
    return ToolNode(tools=tools)

