import requests

class MCPClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def call_tool(self, tool, args):
        res = requests.post(
            f"{self.base_url}/tools/{tool}",
            json=args
        )
        return res.json()