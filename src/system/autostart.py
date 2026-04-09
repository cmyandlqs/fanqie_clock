from __future__ import annotations

import os
import sys
from pathlib import Path


class AutoStartManager:
    def __init__(self) -> None:
        startup_dir = (
            Path.home()
            / "AppData"
            / "Roaming"
            / "Microsoft"
            / "Windows"
            / "Start Menu"
            / "Programs"
            / "Startup"
        )
        self._shortcut_path = startup_dir / "Fanqie Clock.cmd"

    def enable(self) -> None:
        try:
            if getattr(sys, "frozen", False):
                executable = Path(sys.executable)
                command = f'@echo off\r\n"{executable}"\r\n'
            else:
                target = Path(__file__).resolve().parents[2] / "src" / "main.py"
                python_exe = Path(os.sys.executable)
                command = f'@echo off\r\n"{python_exe}" "{target}"\r\n'
            self._shortcut_path.write_text(command, encoding="utf-8")
        except OSError:
            return

    def disable(self) -> None:
        try:
            self._shortcut_path.unlink(missing_ok=True)
        except OSError:
            return
