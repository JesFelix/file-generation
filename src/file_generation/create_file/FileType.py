

from enum import Enum

class FileType(Enum):

    DOC = {"name": "doc", "method": "create_docx"}
    DOCX = {"name": "docx", "method": "create_docx"}
    XLS = {"name": "xls", "method": "create_xls"}
    XLSX = {"name": "xlsx", "method": "create_xlsx"}
    PDF = {"name": "pdf", "method": "create_pdf"}
    CSV = {"name": "csv", "method": "create_csv"}
    TXT = {"name": "txt", "method": "create_txt"}
    JSON = {"name": "json", "method": "create_json"}
    XML = {"name": "xml", "method": "create_xml"}
    HTML = {"name": "html", "method": "create_html"}

    @classmethod
    def find_by_name(cls, name: str) -> "FileType":
        for member in cls:
            if member.value.get("name") == name:
                return member

        return None