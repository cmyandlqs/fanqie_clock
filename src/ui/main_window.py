from __future__ import annotations

from dataclasses import replace

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from src.core.state import DisplaySnapshot, StateSnapshot
from src.system.config import AppConfig
from src.ui.styles import APP_STYLESHEET


class MainWindow(QWidget):
    close_requested = Signal()
    config_changed = Signal(object)

    def __init__(self, timer_engine, config: AppConfig) -> None:
        super().__init__()
        self._timer_engine = timer_engine
        self._config = replace(config)

        self.setWindowTitle("Fanqie Clock")
        self.setMinimumSize(520, 640)
        self.setStyleSheet(APP_STYLESHEET)

        self._status_label = QLabel("Ready")
        self._time_label = QLabel("25:00")
        self._cycle_label = QLabel("Cycle 1 / 4")

        self._focus_spin = QSpinBox()
        self._short_break_spin = QSpinBox()
        self._long_break_spin = QSpinBox()
        self._startup_checkbox = QCheckBox("Launch on startup")
        self._topmost_checkbox = QCheckBox("Floating ball always on top")

        self._build_ui()
        self._apply_config()

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(28, 28, 28, 28)

        card = QFrame()
        card.setObjectName("Card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(28, 28, 28, 28)
        card_layout.setSpacing(20)

        self._status_label.setAlignment(Qt.AlignCenter)
        self._time_label.setAlignment(Qt.AlignCenter)
        self._cycle_label.setAlignment(Qt.AlignCenter)
        self._status_label.setStyleSheet("font-size: 18px; font-weight: 600;")
        self._time_label.setStyleSheet("font-size: 56px; font-weight: 700;")
        self._cycle_label.setStyleSheet("font-size: 14px; color: #667085;")

        card_layout.addWidget(self._status_label)
        card_layout.addWidget(self._time_label)
        card_layout.addWidget(self._cycle_label)

        actions = QHBoxLayout()
        start_button = QPushButton("Start")
        pause_button = QPushButton("Pause")
        reset_button = QPushButton("Reset")
        pause_button.setProperty("variant", "secondary")
        reset_button.setProperty("variant", "secondary")
        start_button.clicked.connect(self._timer_engine.start_or_resume)
        pause_button.clicked.connect(self._timer_engine.pause)
        reset_button.clicked.connect(self._timer_engine.reset)
        actions.addWidget(start_button)
        actions.addWidget(pause_button)
        actions.addWidget(reset_button)
        card_layout.addLayout(actions)

        settings_grid = QGridLayout()
        settings_grid.addWidget(QLabel("Focus"), 0, 0)
        settings_grid.addWidget(QLabel("Short break"), 1, 0)
        settings_grid.addWidget(QLabel("Long break"), 2, 0)
        settings_grid.addWidget(self._focus_spin, 0, 1)
        settings_grid.addWidget(self._short_break_spin, 1, 1)
        settings_grid.addWidget(self._long_break_spin, 2, 1)

        for spin in (self._focus_spin, self._short_break_spin, self._long_break_spin):
            spin.setRange(1, 120)
            spin.valueChanged.connect(self._emit_config_change)

        self._startup_checkbox.stateChanged.connect(self._emit_config_change)
        self._topmost_checkbox.stateChanged.connect(self._emit_config_change)

        card_layout.addLayout(settings_grid)
        card_layout.addWidget(self._startup_checkbox)
        card_layout.addWidget(self._topmost_checkbox)

        root.addWidget(card)

    def _apply_config(self) -> None:
        self._focus_spin.setValue(self._config.focus_minutes)
        self._short_break_spin.setValue(self._config.short_break_minutes)
        self._long_break_spin.setValue(self._config.long_break_minutes)
        self._startup_checkbox.setChecked(self._config.launch_on_startup)
        self._topmost_checkbox.setChecked(self._config.floating_always_on_top)

    def _emit_config_change(self) -> None:
        self._config.focus_minutes = self._focus_spin.value()
        self._config.short_break_minutes = self._short_break_spin.value()
        self._config.long_break_minutes = self._long_break_spin.value()
        self._config.launch_on_startup = self._startup_checkbox.isChecked()
        self._config.floating_always_on_top = self._topmost_checkbox.isChecked()
        self.config_changed.emit(replace(self._config))

    def update_timer_display(self, snapshot: DisplaySnapshot) -> None:
        self._time_label.setText(snapshot.time_text)
        self._status_label.setText(snapshot.status_text)

    def update_state(self, snapshot: StateSnapshot) -> None:
        self._cycle_label.setText(
            f"Cycle {snapshot.current_cycle} / {self._config.cycles_before_long_break}"
        )

    def show_centered(self) -> None:
        handle = self.windowHandle()
        screen = self.screen() or (handle.screen() if handle is not None else None)
        if screen is not None:
            geometry = screen.availableGeometry()
            width = max(int(geometry.width() * 0.25), 520)
            height = max(int(geometry.height() * 0.55), 640)
            self.resize(width, height)
            self.move(
                geometry.center().x() - self.width() // 2,
                geometry.center().y() - self.height() // 2,
            )
        self.show()

    def closeEvent(self, event) -> None:
        event.ignore()
        self.close_requested.emit()
