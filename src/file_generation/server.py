"""MCP 服务入口：生成测试文件。"""

from pathlib import Path
from typing import Annotated, Literal

from fastmcp import FastMCP
from fastmcp.exceptions import ToolError
from mcp.types import ToolAnnotations
from pydantic import BaseModel, Field

from .create_file import CreateFile, FileType

FileTypeName = Literal["txt", "docx", "doc"]

mcp = FastMCP(
    name="file-generation",
    instructions=(
        "用于生成测试用的文件。调用 create_file 时需要提供输出目录（推荐绝对路径），"
        "可选指定文件类型、文件名和内容。支持的类型：txt、docx、doc。"
        "只想生成一个占位文件时，只传 path 即可。"
    ),
)


class CreateFileResult(BaseModel):
    """create_file 的成功返回值。"""

    status: Literal["success"] = "success"
    message: str = Field(description="结果说明，包含实际文件大小和是否覆盖了同名文件")
    file_path: str = Field(description="生成文件的绝对路径")
    file_name: str = Field(description="生成文件的文件名（含扩展名）")
    file_type: str = Field(description="实际使用的文件类型")
    size_bytes: int = Field(description="生成文件的实际大小（字节）")
    overwritten: bool = Field(description="是否覆盖了已存在的同名文件")


def _format_size(size_bytes: int) -> str:
    """把字节数格式化为便于阅读的大小。"""
    if size_bytes < 1024:
        return f"{size_bytes} 字节"
    if size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    return f"{size_bytes / 1024 / 1024:.2f} MB"


@mcp.tool(
    name="create_file",
    title="创建测试文件",
    annotations=ToolAnnotations(
        title="创建测试文件",
        read_only_hint=False,
        destructive_hint=True,
        idempotent_hint=False,
        open_world_hint=False,
    ),
)
def create_file(
    path: Annotated[
        str,
        Field(
            description=(
                "输出目录，例如 D:/tmp 或 ./output；也可以是完整文件路径，"
                "例如 D:/tmp/report.docx（此时会自动推断文件类型）。"
                "目录不存在会自动创建，建议使用绝对路径。"
            )
        ),
    ],
    file_type: Annotated[
        FileTypeName | None,
        Field(
            description=(
                "文件类型：txt（默认）、docx、doc。"
                "如果 path 已带扩展名（如 .docx）可以省略；两者冲突时会报错。"
            )
        ),
    ] = None,
    file_name: Annotated[
        str | None,
        Field(
            description=(
                "文件名，可省略扩展名，会自动补全；不能包含路径分隔符或 <>:\"|?* 等字符。"
                "省略或传空字符串时使用 8 位随机文件名。"
            )
        ),
    ] = None,
    file_content: Annotated[
        str | int | None,
        Field(
            description=(
                "文件内容。传 str 时直接写入文本（docx 按行分段）；"
                "传 int 时表示目标大小，单位 KB（0-20480），"
                "其中 txt 精确、docx/doc 为近似文本量；"
                "省略时写入自动生成的随机中文文章。"
            )
        ),
    ] = None,
) -> CreateFileResult:
    """创建测试文件（txt / docx / doc），返回生成文件的绝对路径。

    行为说明：
    - 输出目录不存在时会自动创建；同名文件会被直接覆盖。
    - 只传 path 时，会生成一个随机文件名、内容为随机文章的 txt 文件。
    - path 可以是目录，也可以是完整文件路径；后者会根据扩展名推断文件类型。
    - doc 文件使用 docx 兼容格式写入，仅扩展名为 .doc。

    常见用法：
    - 生成随机 txt：create_file(path="D:/tmp")
    - 生成指定内容：create_file(path="D:/tmp", file_content="第一段\\n第二段")
    - 生成约 100 KB 的 docx：create_file(path="D:/tmp", file_type="docx", file_content=100)
    - 直接指定完整路径：create_file(path="D:/tmp/report.docx", file_content="hello")

    失败时（如类型不支持、文件名非法、路径不可写）会抛出工具错误并说明原因。
    """
    try:
        resolved_type = None
        if file_type is not None:
            resolved_type = FileType.find_by_name(file_type)
            if resolved_type is None:
                raise ValueError(f"不支持的文件类型: {file_type}")

        creator = CreateFile(
            path=path,
            file_name=file_name,
            file_type=resolved_type,
            file_content=file_content,
        )
        creator.create()
    except (ValueError, TypeError, NotImplementedError) as exc:
        raise ToolError(str(exc)) from exc
    except OSError as exc:
        raise ToolError(f"文件写入失败: {exc}") from exc

    target_desc = (
        f"目标 {file_content} KB，实际 {_format_size(creator.file_size)}"
        if isinstance(file_content, int)
        else _format_size(creator.file_size)
    )
    overwrite_desc = "，已覆盖同名文件" if creator.overwritten else ""

    return CreateFileResult(
        message=f"已创建 {creator.file_name}（{target_desc}）{overwrite_desc}",
        file_path=str(Path(creator.file_path).resolve()),
        file_name=creator.file_name,
        file_type=creator.file_type.value["name"],
        size_bytes=creator.file_size,
        overwritten=creator.overwritten,
    )
