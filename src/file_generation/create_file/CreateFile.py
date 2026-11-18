
import os
import string
import random
from typing import Union

from docx import Document

from .FileType import FileType
from ..bullshit_generator import article_generation

class CreateFile:

    @staticmethod
    def random_str(length: int = 8) -> str:
        """
        description: 生成随机字符串
        params:
            - length: 字符串长度
        return str
        """
        chars = string.ascii_letters + string.digits
        return ''.join(random.choices(chars, k = length))

    def __init__(
        self,
        path: str,
        file_name: str | None = None,
        file_type: FileType | None = None,
        file_content: Union[str, int] | None = None
    ) -> None:
        """
        description: 创建文件
        params:
            - file_type: 文件类型
            - file_name: 文件名
            - file_content: 文件内容；str 表示文件内容，int 表示文件大小（单位：KB）
            - path: 文件路径
        """
        self.file_type = FileType.TXT if file_type is None else file_type

        self.file_content = file_content
        if file_content is None:
            self.file_content = article_generation()
        if isinstance(file_content, int):
            if file_content < 0:
                self.file_content = 0
            elif file_content > 2097152:
                self.file_content = 2097152

        self.file_name = file_name
        if file_name is None:
            self.file_name = CreateFile.random_str()
        
        # 确保路径存在
        self.path = path
        if path is None:
            raise ValueError("path is None")
        os.makedirs(self.path, exist_ok=True)

    def create_docx(self) -> None:
        """
        description: 创建 docx、doc 文件
        file_content:
            - str: 按行写入段落
            - int: 生成指定 KB 大小的文件，内容使用填充文本
        """
        if isinstance(self.file_content, int):
            # int 表示目标文件大小（KB）。先按固定大小生成 UTF-8 文本，
            # 再将文本放入合法的 DOCX 文档中保存。
            target_size = self.file_content * 1024
            os.makedirs(self.path, exist_ok=True)
            txt_path = os.path.join(self.path, self.file_name)
            if not txt_path.lower().endswith(".txt"):
                txt_path += ".txt"
            docx_name = os.path.splitext(self.file_name)[0] + "." + self.file_type.value["name"]
            docx_path = os.path.join(self.path, docx_name)

            text = "固定大小内容"
            encoded = text.encode("utf-8")
            content = (encoded * ((target_size + len(encoded) - 1) // len(encoded)))[:target_size]
            with open(txt_path, "wb") as txt_file:
                txt_file.write(content)

            document = Document()
            document.add_paragraph(content.decode("utf-8", errors="ignore"))
            document.save(docx_path)
            os.replace(txt_path, docx_path)
            return self.path

        if isinstance(self.file_content, str):
            document = Document()
            for line in self.file_content.splitlines() or [""]:
                document.add_paragraph(line)
            os.makedirs(self.path, exist_ok=True)
            docx_name = self.file_name
            if not docx_name.lower().endswith("." + self.file_type.value["name"]):
                docx_name += "." + self.file_type.value["name"]
            document.save(os.path.join(self.path, docx_name))
            return self.path

        raise TypeError("file_content must be str or int")


    def create_txt(self) -> str:
        """
        description: 创建 txt 文件
        file_content:
            - str: 按行写入段落
            - int: 生成指定 KB 大小的文件，内容使用填充文本
        """

        if not self.file_name.lower().endswith("." + self.file_type.value["name"]):
            self.file_name += "." + self.file_type.value["name"]
        file_path = os.path.join(self.path, self.file_name)

        if isinstance(self.file_content, int):
            size_bytes = self.file_content * 1024
            chunk = article_generation().encode("utf-8") * 1024

            with open(file_path, "wb") as output_file:
                remaining = size_bytes
                while remaining:
                    write_size = min(len(chunk), remaining)
                    output_file.write(chunk[:write_size])
                    remaining -= write_size

            return self.path

        else:
            with open(file_path, "w", encoding="utf-8", newline="") as output_file:
                output_file.write(self.file_content)
            return self.path