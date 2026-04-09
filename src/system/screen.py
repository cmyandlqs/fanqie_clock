from __future__ import annotations

from PySide6.QtGui import QGuiApplication


def screen_geometries() -> list:
    return [screen.geometry() for screen in QGuiApplication.screens()]
