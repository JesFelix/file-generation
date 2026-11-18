"""
description: 狗屁不同内容生成器
"""

def read_json_file(fileName=""):
    import json
    if fileName!='':
        strList = fileName.split(".")
        if strList[len(strList)-1].lower() == "json":
            with open(fileName,mode='r',encoding="utf-8") as file:
                return json.loads(file.read())

from .article_generation import article_generation

__all__ = ["article_generation"]
