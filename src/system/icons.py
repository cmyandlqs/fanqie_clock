from __future__ import annotations

from pathlib import Path

from PySide6.QtGui import QIcon


def app_icon() -> QIcon:
    icon_path = Path(__file__).resolve().parents[2] / "assets" / "tomato.svg"
    return QIcon(str(icon_path))
