from langchain_community.vectorstores.oraclevs import log_level

from mcp_server.tool_server import server

if __name__ == '__main__':
    server.run(
        transport='streamable-http',
        host='127.0.0.1',
        port=3002,
        log_level = 'debug',
        path='/streamable',
    )