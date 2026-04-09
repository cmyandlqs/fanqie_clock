from __future__ import annotations

from dataclasses import replace

from PySide6.QtCore import QPoint, Qt, Signal
from PySide6.QtGui import QColor, QMouseEvent, QPainter, QPaintEvent
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSpinBox,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from src.core.state import DisplaySnapshot, StateSnapshot
from src.system.config import AppConfig
from src.system.icons import app_icon
from src.ui.styles import APP_STYLESHEET
from src.ui.toggle_switch import ToggleSwitch


class MainWindow(QWidget):
    close_requested = Signal()
    config_changed = Signal(object)

    def __init__(self, timer_engine, config: AppConfig) -> None:
        super().__init__()
        self._timer_engine = timer_engine
        self._config = replace(config)
        self._drag_origin: QPoint | None = None

        self.setWindowTitle("番茄钟")
        self.setWindowIcon(app_icon())
        self.setMinimumSize(640, 700)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setStyleSheet(APP_STYLESHEET)

        self._status_label = QLabel("待开始")
        self._time_label = QLabel("25:00")
        self._cycle_label = QLabel("第 1 轮 / 共 4 轮")

        self._focus_spin = QSpinBox()
        self._short_break_spin = QSpinBox()
        self._long_break_spin = QSpinBox()
        self._startup_checkbox = ToggleSwitch("开机自动启动")
        self._topmost_checkbox = ToggleSwitch("悬浮球始终置顶")

        self._build_ui()
        self._apply_config()

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(18, 18, 18, 18)

        card = QFrame()
        card.setObjectName("Card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(28, 28, 28, 28)
        card_layout.setSpacing(22)

        title_bar = QFrame()
        title_bar.setObjectName("TitleBar")
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(0, 0, 0, 6)
        title_layout.setSpacing(12)

        title_label = QLabel("番茄钟")
        title_label.setObjectName("TitleLabel")
        subtitle = QLabel("轻量专注，准时休息")
        subtitle.setStyleSheet("font-size: 12px; font-weight: 500; color: #9a3412;")
        title_stack = QVBoxLayout()
        title_stack.setContentsMargins(0, 0, 0, 0)
        title_stack.setSpacing(4)
        title_stack.addWidget(title_label)
        title_stack.addWidget(subtitle)

        close_button = QToolButton()
        close_button.setObjectName("TitleButton")
        close_button.setText("收起")
        close_button.clicked.connect(self.close_requested.emit)

        title_layout.addLayout(title_stack)
        title_layout.addStretch()
        title_layout.addWidget(close_button)

        card_layout.addWidget(title_bar)

        self._status_label.setAlignment(Qt.AlignCenter)
        self._time_label.setAlignment(Qt.AlignCenter)
        self._cycle_label.setAlignment(Qt.AlignCenter)
        self._status_label.setStyleSheet("font-size: 18px; font-weight: 700; color: #9a3412;")
        self._time_label.setStyleSheet("font-size: 58px; font-weight: 800; color: #7c2d12; letter-spacing: 1px;")
        self._cycle_label.setStyleSheet("font-size: 14px; color: #9c6b4f;")

        card_layout.addWidget(self._status_label)
        card_layout.addWidget(self._time_label)
        card_layout.addWidget(self._cycle_label)

        actions = QHBoxLayout()
        actions.setSpacing(12)
        start_button = QPushButton("开始")
        pause_button = QPushButton("暂停")
        reset_button = QPushButton("重置")
        pause_button.setProperty("variant", "secondary")
        reset_button.setProperty("variant", "secondary")
        start_button.clicked.connect(self._timer_engine.start_or_resume)
        pause_button.clicked.connect(self._timer_engine.pause)
        reset_button.clicked.connect(self._timer_engine.reset)
        actions.addWidget(start_button)
        actions.addWidget(pause_button)
        actions.addWidget(reset_button)
        card_layout.addLayout(actions)

        settings_panel = QFrame()
        settings_panel.setObjectName("SettingsPanel")
        settings_layout = QVBoxLayout(settings_panel)
        settings_layout.setContentsMargins(20, 20, 20, 20)
        settings_layout.setSpacing(16)

        panel_title = QLabel("设置")
        panel_title.setStyleSheet("font-size: 16px; font-weight: 700; color: #7c2d12; min-height: 24px;")
        settings_layout.addWidget(panel_title)

        settings_layout.addWidget(self._build_duration_row("专注时长", self._focus_spin))
        settings_layout.addWidget(self._build_duration_row("短休息", self._short_break_spin))
        settings_layout.addWidget(self._build_duration_row("长休息", self._long_break_spin))

        for spin in (self._focus_spin, self._short_break_spin, self._long_break_spin):
            spin.setRange(1, 120)
            spin.setButtonSymbols(QSpinBox.NoButtons)
            spin.valueChanged.connect(self._emit_config_change)

        self._startup_checkbox.stateChanged.connect(self._emit_config_change)
        self._topmost_checkbox.stateChanged.connect(self._emit_config_change)

        settings_layout.addWidget(self._startup_checkbox)
        settings_layout.addWidget(self._topmost_checkbox)

        footer = QLabel("by sikm")
        footer.setObjectName("FooterLabel")
        footer.setAlignment(Qt.AlignRight)
        settings_layout.addWidget(footer)

        card_layout.addWidget(settings_panel)

        root.addWidget(card)

    def _build_duration_row(self, label_text: str, spin_box: QSpinBox) -> QWidget:
        row = QFrame()
        row.setObjectName("SettingRow")
        layout = QHBoxLayout(row)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        label = QLabel(label_text)
        label.setObjectName("SettingLabel")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        label.setFixedWidth(92)

        minus_button = QToolButton()
        minus_button.setObjectName("SpinButton")
        minus_button.setText("-")
        minus_button.clicked.connect(lambda: spin_box.setValue(spin_box.value() - 1))

        plus_button = QToolButton()
        plus_button.setObjectName("SpinButton")
        plus_button.setText("+")
        plus_button.clicked.connect(lambda: spin_box.setValue(spin_box.value() + 1))

        minute_label = QLabel("分钟")
        minute_label.setObjectName("MinuteLabel")

        layout.addWidget(label)
        layout.addWidget(minus_button)
        layout.addWidget(spin_box)
        layout.addWidget(plus_button)
        layout.addWidget(minute_label)
        layout.addSpacing(6)
        layout.addStretch(1)
        return row

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
            f"第 {snapshot.current_cycle} 轮 / 共 {self._config.cycles_before_long_break} 轮"
        )

    def show_centered(self) -> None:
        handle = self.windowHandle()
        screen = self.screen() or (handle.screen() if handle is not None else None)
        if screen is not None:
            geometry = screen.availableGeometry()
            width = max(int(geometry.width() * 0.32), 640)
            height = max(int(geometry.height() * 0.62), 700)
            self.resize(width, height)
            self.move(
                geometry.center().x() - self.width() // 2,
                geometry.center().y() - self.height() // 2,
            )
        self.show()

    def closeEvent(self, event) -> None:
        event.ignore()
        self.close_requested.emit()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self._drag_origin = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self._drag_origin is not None and event.buttons() & Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_origin)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self._drag_origin = None
        super().mouseReleaseEvent(event)

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(0, 0, 0, 24))
        painter.drawRoundedRect(self.rect().adjusted(8, 8, -8, -4), 30, 30)
        super().paintEvent(event)
