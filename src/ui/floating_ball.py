from __future__ import annotations

from PySide6.QtCore import QPoint, Qt, Signal
from PySide6.QtGui import QColor, QMouseEvent, QPainter, QPaintEvent
from PySide6.QtWidgets import QWidget

from src.core.state import DisplaySnapshot, StateSnapshot, TimerState
from src.system.config import AppConfig
from src.system.icons import app_icon


class FloatingBall(QWidget):
    open_requested = Signal()
    position_changed = Signal(int, int)

    def __init__(self, timer_engine, config: AppConfig) -> None:
        super().__init__()
        self._timer_engine = timer_engine
        self._config = config
        self._time_text = "25:00"
        self._status = "待开始"
        self._drag_offset: QPoint | None = None
        self._press_pos: QPoint | None = None
        self._state = TimerState.IDLE

        self.setWindowTitle("番茄钟悬浮球")
        self.setWindowIcon(app_icon())
        self.setFixedSize(88, 88)
        self.setWindowFlags(
            Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.move(config.floating_position_x, config.floating_position_y)

    def apply_config(self, config: AppConfig) -> None:
        self._config = config
        flags = Qt.FramelessWindowHint | Qt.Tool
        if config.floating_always_on_top:
            flags |= Qt.WindowStaysOnTopHint
        self.setWindowFlags(flags)
        self.show()

    def update_display(self, snapshot: DisplaySnapshot) -> None:
        self._time_text = snapshot.time_text
        self._status = snapshot.status_text
        self.update()

    def update_state(self, snapshot: StateSnapshot) -> None:
        self._state = snapshot.state
        self.update()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self._press_pos = event.globalPosition().toPoint()
            self._drag_offset = self._press_pos - self.frameGeometry().topLeft()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self._drag_offset is not None and event.buttons() & Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_offset)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton and self._drag_offset is not None:
            release_pos = event.globalPosition().toPoint()
            moved = (
                0 if self._press_pos is None else (release_pos - self._press_pos).manhattanLength()
            )
            if moved < 4:
                self.open_requested.emit()
            self._config.floating_position_x = self.x()
            self._config.floating_position_y = self.y()
            self.position_changed.emit(self.x(), self.y())
            self._drag_offset = None
            self._press_pos = None
        super().mouseReleaseEvent(event)

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        color = QColor("#111827")
        if self._state in {
            TimerState.SHORT_BREAK,
            TimerState.LONG_BREAK,
            TimerState.BREAK_PROMPT,
        }:
            color = QColor("#0f766e")
        elif self._state == TimerState.PAUSED:
            color = QColor("#475467")

        painter.setBrush(QColor(15, 23, 42, 32))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(self.rect().adjusted(4, 6, -4, -2))
        painter.setBrush(color)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(self.rect().adjusted(2, 2, -2, -6))

        painter.setPen(QColor("#f8fafc"))
        font = painter.font()
        font.setPointSize(14)
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(
            self.rect().adjusted(0, 6, 0, -12), Qt.AlignCenter, self._time_text
        )

        font.setPointSize(8)
        font.setBold(False)
        painter.setFont(font)
        painter.drawText(
            self.rect().adjusted(0, 40, 0, -4), Qt.AlignCenter, self._status
        )
