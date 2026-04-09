from __future__ import annotations

from PySide6.QtCore import QRectF, QSize, Qt
from PySide6.QtGui import QColor, QFont, QPainter, QPaintEvent
from PySide6.QtWidgets import QCheckBox


class ToggleSwitch(QCheckBox):
    def __init__(self, text: str, parent=None) -> None:
        super().__init__(text, parent)
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(30)

    def sizeHint(self) -> QSize:
        base = super().sizeHint()
        return QSize(base.width() + 18, max(base.height(), 30))

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        try:
            painter.setRenderHint(QPainter.Antialiasing)

            track_width = 42
            track_height = 24
            margin_y = (self.height() - track_height) / 2
            track_rect = QRectF(0, margin_y, track_width, track_height)

            track_color = QColor("#fb923c") if self.isChecked() else QColor("#e7d7ca")
            knob_x = (
                track_rect.right() - track_height + 1
                if self.isChecked()
                else track_rect.left() + 1
            )
            knob_rect = QRectF(knob_x, margin_y + 1, track_height - 2, track_height - 2)

            painter.setPen(Qt.NoPen)
            painter.setBrush(track_color)
            painter.drawRoundedRect(track_rect, track_height / 2, track_height / 2)

            painter.setBrush(QColor("#ffffff"))
            painter.drawEllipse(knob_rect)

            text_rect = self.rect().adjusted(track_width + 12, 0, 0, 0)
            painter.setPen(QColor("#7c2d12"))
            font = painter.font()
            font.setPointSize(10)
            font.setWeight(QFont.Weight.DemiBold)
            painter.setFont(font)
            painter.drawText(text_rect, Qt.AlignVCenter | Qt.AlignLeft, self.text())
        finally:
            painter.end()
