from __future__ import annotations

from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication, QMenu, QSystemTrayIcon

from src.system.icons import app_icon


class TrayController(QObject):
    open_requested = Signal()
    start_pause_requested = Signal()
    quit_requested = Signal()

    def __init__(self, app: QApplication, timer_engine) -> None:
        super().__init__()
        self._app = app
        self._timer_engine = timer_engine
        self._tray = QSystemTrayIcon(app_icon(), self)
        self._tray.setToolTip("番茄钟")
        self._menu = QMenu()

        self._open_action = QAction("打开主界面", self)
        self._toggle_action = QAction("开始 / 暂停", self)
        self._quit_action = QAction("退出", self)

        self._menu.addAction(self._open_action)
        self._menu.addAction(self._toggle_action)
        self._menu.addSeparator()
        self._menu.addAction(self._quit_action)
        self._tray.setContextMenu(self._menu)

        self._open_action.triggered.connect(self.open_requested.emit)
        self._toggle_action.triggered.connect(self.start_pause_requested.emit)
        self._quit_action.triggered.connect(self.quit_requested.emit)
        self._tray.activated.connect(self._handle_activated)

    def show(self) -> None:
        self._tray.show()

    def show_break_notification(self, title: str, seconds: int) -> None:
        minutes = max(seconds // 60, 1)
        self.show_message("休息提醒", f"{title}，时长约 {minutes} 分钟。")

    def show_message(self, title: str, message: str) -> None:
        self._tray.showMessage(title, message, QSystemTrayIcon.Information, 3000)

    def _handle_activated(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        if reason == QSystemTrayIcon.Trigger:
            self.open_requested.emit()
