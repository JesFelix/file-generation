from typing import Union

from fastmcp import FastMCP
from .create_file import FileType

mcp = FastMCP("My MCP Server")

@mcp.tool
@mcp.description("测试工具")
def greet(name: str) -> str:
    return f"Hello, {name}!"


@mcp.tool
def create_file(file_type: FileType, file_name: str, file_content: Union[str, int], path: str):
    pass







