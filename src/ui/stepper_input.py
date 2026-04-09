from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QFrame, QHBoxLayout, QSpinBox, QToolButton, QWidget


class StepperInput(QWidget):
    valueChanged = Signal(int)

    def __init__(self, minimum: int = 1, maximum: int = 120, parent=None) -> None:
        super().__init__(parent)
        self.setMinimumHeight(38)

        self._spin_box = QSpinBox()
        self._spin_box.setRange(minimum, maximum)
        self._spin_box.setButtonSymbols(QSpinBox.NoButtons)
        self._spin_box.setAlignment(Qt.AlignCenter)
        self._spin_box.valueChanged.connect(self.valueChanged.emit)

        self._minus_button = QToolButton()
        self._minus_button.setObjectName("StepperButton")
        self._minus_button.setText("-")
        self._minus_button.clicked.connect(self._decrement)

        self._plus_button = QToolButton()
        self._plus_button.setObjectName("StepperButton")
        self._plus_button.setText("+")
        self._plus_button.clicked.connect(self._increment)

        frame = QFrame()
        frame.setObjectName("StepperFrame")
        frame.setMinimumHeight(38)
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(6)
        layout.setAlignment(Qt.AlignVCenter)
        layout.addWidget(self._minus_button, 0, Qt.AlignVCenter)
        layout.addWidget(self._spin_box, 0, Qt.AlignVCenter)
        layout.addWidget(self._plus_button, 0, Qt.AlignVCenter)

        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setAlignment(Qt.AlignVCenter)
        root.addWidget(frame, 0, Qt.AlignVCenter)

    def setValue(self, value: int) -> None:
        self._spin_box.setValue(value)

    def value(self) -> int:
        return self._spin_box.value()

    def _decrement(self) -> None:
        self._spin_box.setValue(self._spin_box.value() - 1)

    def _increment(self) -> None:
        self._spin_box.setValue(self._spin_box.value() + 1)
