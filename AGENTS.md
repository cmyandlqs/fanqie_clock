# Repository Guidelines

## Project Structure & Module Organization

This repository is currently in the planning stage. The main product document lives at [`需求文档.md`](D:\sikm\Desktop\PythonProject\AI-apps\Fanqie_clock\需求文档.md). Keep new planning notes in the repository root only if they are project-level documents.

When implementation starts, use a simple layout:

- `src/` for application code
- `tests/` for automated tests
- `assets/` for icons, images, and UI resources
- `docs/` for design notes, architecture, and release decisions

Prefer small, focused modules. For example: `src/timer/`, `src/ui/`, `src/system/`.

## Build, Test, and Development Commands

No build system is committed yet. If the project follows the current Python desktop direction, standardize around:

- `python -m venv .venv` to create a virtual environment
- `.venv\Scripts\activate` to activate it on Windows
- `pip install -r requirements.txt` to install dependencies
- `python -m pytest` to run tests
- `python -m src.main` to start the app locally

Add new commands to this file when the toolchain is finalized.

## Coding Style & Naming Conventions

Use 4-space indentation for Python. Follow PEP 8 and keep functions and modules in `snake_case`, classes in `PascalCase`, and constants in `UPPER_SNAKE_CASE`.

Keep UI code and timer logic separate. Avoid large mixed files such as one file owning windows, state, and persistence together.

If formatting tools are added, prefer `black` and `ruff` and run them before opening a PR.

## Testing Guidelines

Use `pytest` for unit and integration tests. Place tests under `tests/` and name files `test_<module>.py`.

Focus first on timer state transitions, reminder scheduling, persistence, and multi-window behavior. Add regression tests for every bug fix that affects timing or reminder flow.

## Commit & Pull Request Guidelines

Git history is not yet available as a stable reference, so use short imperative commit messages such as:

- `Add timer state machine skeleton`
- `Implement floating window drag behavior`

Each pull request should include:

- a brief summary of the change
- the user-facing impact
- test notes
- screenshots or recordings for UI changes

## Security & Configuration Tips

Do not commit local machine paths, packaged binaries, secrets, or personal startup settings. Keep user-specific configuration out of version control and document required environment variables in `docs/` or `README.md` once introduced.

## github管理策略

注意版本控制，完成一个比较大的功能迭代，都要使用git就是commit，push，commit message要清晰简洁，中英文两种
