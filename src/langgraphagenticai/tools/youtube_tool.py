from langchain_core.tools import tool
from src.mcp_client.mcp_client import MCPClient
#from mcp_client import MCPClient

mcp = MCPClient("http://localhost:8001")

@tool
def search_youtube(query: str):
    """
    Use this tool when the user asks for YouTube videos, tutorials,
    music, or anything that requires video content.
    Returns title, URL, and channel name.
    """
    data = mcp.call_tool("search_youtube", {"query": query})
    videos = data.get("videos", [])
        
    if not videos:
        return "No videos found."

    formatted = "Here are some YouTube videos:\n\n"

    for i, video in enumerate(videos, 1):
        formatted += (
            f"{i}. {video['title']}\n"
            f"   Channel: {video['channel']}\n"
            f"   Link: {video['url']}\n\n"
        )
    print(formatted)
    return formatted

def get_youtube_tools():
    """
    Return the list of tools to be used in the chatbot for youtube search
    """
    return [search_youtube]