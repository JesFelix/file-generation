import os
from io import BytesIO
from typing import Union

from docx import Document

from .FileType import FileType
from ..bullshit_generator import article_generation

class CreateFile:

    def __init__(
        self,
        file_type: FileType,
        file_name: str,
        file_content: Union[str, int],
        path: str,
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

        if file_content is None:
            self.file_content = article_generation()
        if isinstance(file_content, int):
            if file_content < 1024:
                self.file_content = 1024
            elif file_content > 2097152:
                self.file_content = 2097152
        self.file_content = file_content

        if file_name is None:
            raise ValueError("file_name is None")
        if path is None:
            raise ValueError("path is None")
        self.file_name = file_name
        self.path = path

    def create_docx(self) -> None:
        """
        description: 创建 docx 文件
        file_content:
            - str: 按行写入段落
            - int: 生成指定 KB 大小的文件，内容使用填充文本
        """
        docx = Document()
        if isinstance(self.file_content, int):
            # 通过追加段落来增加文件大小
            tmp_content = article_generation()
            tmp_size = len(tmp_content.encode('utf-8'))

            if tmp_size < self.file_content * 1024:
                tmp_poor = self.file_content * 1024 - tmp_size
                print(f"文件大小小于目标大小，需要补充 {tmp_poor} 字节")

            if  tmp_size > self.file_content * 1024:
                tmp_content = tmp_content[:self.file_content * 1024]
                print(f"文件大小超过目标大小，已截断 {tmp_size - self.file_content * 1024} 字节")

            docx.add_paragraph(tmp_content)
            docx.save(self.path)
            
            return self.path
        else:
            return self.path


