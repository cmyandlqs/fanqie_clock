from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtGui import QIcon


def resource_path(*parts: str) -> Path:
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS).joinpath(*parts)
    return Path(__file__).resolve().parents[2].joinpath(*parts)


def app_icon() -> QIcon:
    icon_path = resource_path("assets", "tomato.svg")
    return QIcon(str(icon_path))
