# Repository Guidelines

## Project Structure & Module Organization

This is a Python package built with a `src` layout. Application code lives in `src/file_generation/`: `server.py` defines the FastMCP tools, `create_file/` contains file type and generation logic, and `bullshit_generator/` contains text generation plus its JSON data resource. There is currently no test directory; add tests under `tests/` as the project grows.

## Build, Test, and Development Commands

Use Python 3.14 or newer and `uv` for environment and package management:

- `uv sync` installs the locked project dependencies into the local environment.
- `uv run file-generation` runs the installed console script, when its package entry point is implemented.
- `uv build` builds distributable package artifacts.
- `uv run pytest` runs tests once a pytest suite is added.

Run commands from the repository root. Keep `uv.lock` committed so dependency resolution remains reproducible.

## Coding Style & Naming Conventions

Follow standard Python style: four spaces per indentation level, `snake_case` for modules, functions, and variables, and `PascalCase` for classes. Keep modules focused on one responsibility and use type hints on public functions. Preserve the existing `src/file_generation` package structure; use lowercase module filenames for new modules.

## Testing Guidelines

No test framework or tests are currently configured. When adding tests, use pytest, place them in `tests/`, and name files `test_*.py` and test functions `test_*`. Cover generated file types and invalid inputs, including path and content handling. Run `uv run pytest` before submitting changes.

## Commit & Pull Request Guidelines

The repository has no commit history yet, so no established commit convention can be inferred. Use a short imperative commit subject (for example, `Add TXT file generation`). Pull requests should explain the behavior change, list validation commands and results, link related issues when applicable, and include sample output or screenshots for user-visible changes.

## Security & Configuration

Do not commit credentials, generated output files, or local virtual environments. Keep configuration and data needed at runtime in the package; document any new environment variables in `README.md`.
