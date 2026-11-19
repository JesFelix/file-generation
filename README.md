# file-generation

一个基于 [FastMCP](https://github.com/jlowin/fastmcp) 的 MCP 服务，用于快速生成测试文件。

支持生成 **txt**、**docx**、**doc** 三种文件，可指定文件名、文本内容，或按大小（KB）生成随机填充内容。

## 安装

需要 Python 3.14+ 和 [uv](https://docs.astral.sh/uv/)：

```bash
uv sync
```

## 运行

```bash
uv run file-generation
```

服务通过 stdio 与 MCP 客户端通信。以 opencode 为例，在配置文件中添加：

```json
{
  "mcp": {
    "file-generation": {
      "type": "local",
      "command": ["uv", "run", "--directory", "D:/Code/file-generation", "file-generation"],
      "enabled": true
    }
  }
}
```

Claude Desktop 等客户端的配置方式类似，将 `command` 指向 `uv` 并传入对应参数即可。

## 工具：`create_file`

创建测试文件并返回文件的绝对路径。

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `path` | string | 是 | 输出目录（推荐绝对路径），也可以是完整文件路径；目录不存在会自动创建 |
| `file_type` | `"txt"` \| `"docx"` \| `"doc"` | 否 | 默认 `txt`；若 `path` 带扩展名可省略 |
| `file_name` | string | 否 | 文件名，可省略扩展名；默认使用 8 位随机字符串 |
| `file_content` | string \| int | 否 | 字符串表示文本内容；整数表示目标大小（KB，最大 20480）；省略时写入随机中文文章 |

返回值（JSON）：

```json
{
  "status": "success",
  "message": "已创建 report.docx（目标 100 KB，实际 101.2 KB）",
  "file_path": "D:\\tmp\\report.docx",
  "file_name": "report.docx",
  "file_type": "docx",
  "size_bytes": 103629,
  "overwritten": false
}
```

### 示例

```text
create_file(path="D:/tmp")
create_file(path="D:/tmp", file_name="demo", file_content="第一行\n第二行")
create_file(path="D:/tmp", file_type="docx", file_content=100)
create_file(path="D:/tmp/report.docx", file_content="hello")
```

### 行为说明

- 同名文件会被直接覆盖，返回值的 `overwritten` 会标记是否发生了覆盖。
- `path` 以受支持的扩展名（`.txt` / `.docx` / `.doc`）结尾时按完整文件路径处理，并自动推断类型；与 `file_type` 冲突时会报错。
- 传整数 `file_content` 时，txt 会生成精确大小的文件；docx / doc 会按目标字节数生成文本，由于文档压缩和格式开销，最终文件大小可能偏大或偏小，仅作近似参考。
- `doc` 使用 docx 兼容格式写入，仅扩展名为 `.doc`。
- 参数非法（类型不支持、文件名包含非法字符、大小超限等）时会返回明确的工具错误，不会静默失败。

## 开发

```bash
uv run pytest
uv build
```

项目结构：

```text
src/file_generation/
├── server.py              # MCP 工具定义
├── create_file/           # 路径解析与文件写入
└── bullshit_generator/    # 随机填充文本生成
```
