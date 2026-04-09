from __future__ import annotations

from PySide6.QtCore import QPoint, Qt, Signal
from PySide6.QtGui import QColor, QLinearGradient, QMouseEvent, QPainter, QPaintEvent, QRadialGradient
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

        outer_rect = self.rect().adjusted(2, 2, -2, -6)
        shadow_rect = self.rect().adjusted(4, 8, -4, -1)

        painter.setBrush(QColor(15, 23, 42, 32))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(shadow_rect)

        body_gradient = QLinearGradient(0, outer_rect.top(), 0, outer_rect.bottom())
        body_gradient.setColorAt(0.0, color.lighter(128))
        body_gradient.setColorAt(0.55, color)
        body_gradient.setColorAt(1.0, color.darker(112))
        painter.setBrush(body_gradient)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(outer_rect)

        ring_gradient = QLinearGradient(outer_rect.left(), outer_rect.top(), outer_rect.right(), outer_rect.bottom())
        ring_gradient.setColorAt(0.0, QColor(255, 255, 255, 95))
        ring_gradient.setColorAt(1.0, QColor(255, 255, 255, 12))
        painter.setBrush(Qt.NoBrush)
        painter.setPen(QColor(255, 255, 255, 55))
        painter.drawEllipse(outer_rect.adjusted(1, 1, -1, -1))

        highlight = QRadialGradient(outer_rect.center().x() - 16, outer_rect.top() + 18, 34)
        highlight.setColorAt(0.0, QColor(255, 255, 255, 120))
        highlight.setColorAt(0.7, QColor(255, 255, 255, 20))
        highlight.setColorAt(1.0, QColor(255, 255, 255, 0))
        painter.setBrush(highlight)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(outer_rect.adjusted(8, 6, -18, -30))

        painter.setPen(QColor("#f8fafc"))
        font = painter.font()
        font.setPointSize(14)
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(
            outer_rect.adjusted(0, 8, 0, -14), Qt.AlignCenter, self._time_text
        )

        font.setPointSize(8)
        font.setBold(False)
        painter.setFont(font)
        painter.drawText(
            outer_rect.adjusted(0, 42, 0, -2), Qt.AlignCenter, self._status
        )
