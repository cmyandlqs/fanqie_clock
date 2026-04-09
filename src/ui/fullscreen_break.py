from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from src.core.state import DisplaySnapshot, StateSnapshot, TimerState
from src.system.screen import screen_geometries


class BreakOverlay(QWidget):
    skip_requested = Signal()
    snooze_requested = Signal()
    close_requested = Signal()
    start_next_requested = Signal()

    def __init__(self, title: str, seconds: int) -> None:
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setStyleSheet(
            """
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(28, 25, 23, 238),
                    stop:0.55 rgba(68, 64, 60, 232),
                    stop:1 rgba(124, 45, 18, 228));
                color: white;
                font-family: "Segoe UI";
            }
            QFrame {
                background: rgba(255, 248, 240, 0.10);
                border-radius: 28px;
                border: 1px solid rgba(255, 237, 213, 0.22);
            }
            QPushButton {
                background: rgba(255, 247, 237, 0.96);
                color: #7c2d12;
                border: none;
                border-radius: 14px;
                padding: 12px 18px;
                font-weight: 700;
            }
            """
        )

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        card = QFrame()
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(36, 36, 36, 36)
        card_layout.setSpacing(18)

        self._title_label = QLabel(title)
        self._title_label.setAlignment(Qt.AlignCenter)
        self._title_label.setStyleSheet("font-size: 38px; font-weight: 700; color: #fff7ed;")
        self._time_label = QLabel(self._format_seconds(seconds))
        self._time_label.setAlignment(Qt.AlignCenter)
        self._time_label.setStyleSheet("font-size: 72px; font-weight: 800; color: #ffedd5;")
        hint_label = QLabel("站起来活动一下，看看远处，放松眼睛。")
        hint_label.setAlignment(Qt.AlignCenter)
        hint_label.setStyleSheet("font-size: 16px; color: rgba(255,247,237,0.88);")

        actions = QHBoxLayout()
        skip_button = QPushButton("跳过休息")
        snooze_button = QPushButton("延后 5 分钟")
        close_button = QPushButton("关闭提醒")
        next_button = QPushButton("开始下一轮")
        skip_button.clicked.connect(self.skip_requested.emit)
        snooze_button.clicked.connect(self.snooze_requested.emit)
        close_button.clicked.connect(self.close_requested.emit)
        next_button.clicked.connect(self.start_next_requested.emit)
        actions.addWidget(skip_button)
        actions.addWidget(snooze_button)
        actions.addWidget(close_button)
        actions.addWidget(next_button)

        card_layout.addWidget(self._title_label)
        card_layout.addWidget(self._time_label)
        card_layout.addWidget(hint_label)
        card_layout.addLayout(actions)
        layout.addWidget(card)

    def update_title(self, title: str) -> None:
        self._title_label.setText(title)

    def update_countdown(self, snapshot: DisplaySnapshot) -> None:
        self._time_label.setText(snapshot.time_text)

    def _format_seconds(self, total_seconds: int) -> str:
        minutes, seconds = divmod(total_seconds, 60)
        return f"{minutes:02d}:{seconds:02d}"


class FullscreenBreakController(QWidget):
    skip_requested = Signal()
    snooze_requested = Signal()
    close_requested = Signal()
    start_next_requested = Signal()

    def __init__(self, timer_engine) -> None:
        super().__init__()
        self._timer_engine = timer_engine
        self._overlays: list[BreakOverlay] = []
        self._last_title = "该休息一下了"

    def show_break_prompt(self, title: str, seconds: int) -> None:
        self._last_title = title
        self.close_all()
        for geometry in screen_geometries():
            overlay = BreakOverlay(title, seconds)
            overlay.setGeometry(geometry)
            overlay.skip_requested.connect(self._handle_skip)
            overlay.snooze_requested.connect(self._handle_snooze)
            overlay.close_requested.connect(self._handle_close)
            overlay.start_next_requested.connect(self._handle_start_next)
            overlay.showFullScreen()
            overlay.raise_()
            overlay.activateWindow()
            self._overlays.append(overlay)

    def update_countdown(self, snapshot: DisplaySnapshot) -> None:
        if not self._overlays:
            return
        for overlay in self._overlays:
            overlay.update_countdown(snapshot)

    def handle_state_changed(self, snapshot: StateSnapshot) -> None:
        if snapshot.state != TimerState.BREAK_PROMPT:
            self.close_all()

    def close_all(self) -> None:
        while self._overlays:
            overlay = self._overlays.pop()
            overlay.close()

    def _handle_skip(self) -> None:
        self.close_all()
        self.skip_requested.emit()

    def _handle_snooze(self) -> None:
        self.close_all()
        self.snooze_requested.emit()

    def _handle_close(self) -> None:
        self.close_all()
        self.close_requested.emit()

    def _handle_start_next(self) -> None:
        self.close_all()
        self.start_next_requested.emit()
