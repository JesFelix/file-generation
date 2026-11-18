

# ========================================= 工具 =========================================
import string
import random

def random_str(length: int = 8) -> str:
    """
    description: 生成随机字符串
    params:
        - length: 字符串长度
    return str
    """
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k = length))


# ========================================= 服务器 =========================================

# from .server import mcp

from .create_file import CreateFile, FileType

def main() -> None:
    # mcp.run()
    create_file = CreateFile(FileType.DOCX, "test.docx", 0, "./test.docx")
    create_file.create_docx()