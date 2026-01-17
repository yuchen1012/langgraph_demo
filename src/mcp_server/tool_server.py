from fastmcp import FastMCP
import requests
server = FastMCP(name='jared_mcp', instructions="Jared's MCP Server by Python")

@server.tool()
def search_api(query: str) -> str:
    """Searches the web for the given query using the SearchAPI.io API."""
    url = "https://www.searchapi.io/api/v1/search"
    params = {
      "engine": "google_ai_mode",
      "q": query,
      "api_key": "e3sV9m6HGuV6srG5gbwSMcBZ"
    }

    response = requests.get(url, params=params)
    print(response.text)
    return response.text

@server.tool()
def say_hello(username:str) -> str:
    """Says hello to the given username."""
    return f"Hello, {username}!"

@server.prompt
def ask_about_topic(topic:str) -> str:
    """生成请求解释特定主题的用户消息模板."""
    return f"请解释一下'{topic}'这个概念。"

@server.resource("resource://config")
def get_config() -> dict:
    """以json格式返回应用配置."""
    return {
        "theme": "dark",
        "version": "1.0.0",
        "author": "Jared",
        "features": ["search","hello", "ask"]
    }