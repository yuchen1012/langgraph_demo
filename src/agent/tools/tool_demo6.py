from itertools import chain

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool, BaseTool
from pydantic import BaseModel, Field


class SearchToolArgs(BaseModel):
    query: str = Field(description="The query to search for")

class MySearchTool(BaseTool):
    name:str = "search_tool"
    description:str = "A search tool that searches the web for information. Use this tool when you need to find information that is not available in the knowledge base."
    args_schema:type[BaseModel] = SearchToolArgs
    return_direct:bool = False

    def _run(self, query: str) -> str:
        return f"Search results for '{query}': [list of search results]"

my_search_tool = MySearchTool()
print(my_search_tool.name)