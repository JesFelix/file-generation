# from .server import mcp

from .create_file import CreateFile, FileType

def main() -> None:
    # mcp.run()
    create_file = CreateFile(file_type=FileType.DOCX, file_content=12, path="./test")
    create_method = getattr(create_file, create_file.file_type.value["method"])
    create_method()
