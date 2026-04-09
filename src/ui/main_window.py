from __future__ import annotations

from dataclasses import replace

from PySide6.QtCore import QPoint, Qt, Signal
from PySide6.QtGui import QColor, QLinearGradient, QMouseEvent, QPainter, QPaintEvent
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from src.core.state import DisplaySnapshot, StateSnapshot
from src.system.config import AppConfig
from src.system.icons import app_icon
from src.ui.stepper_input import StepperInput
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

        self._focus_spin = StepperInput()
        self._short_break_spin = StepperInput()
        self._long_break_spin = StepperInput()
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
        title_layout.setContentsMargins(0, 0, 0, 4)
        title_layout.setSpacing(12)
        title_layout.setAlignment(Qt.AlignVCenter)

        title_label = QLabel("番茄钟")
        title_label.setObjectName("TitleLabel")
        subtitle = QLabel("轻量专注，准时休息")
        subtitle.setStyleSheet("font-size: 12px; font-weight: 500; color: #9a3412;")
        title_stack = QVBoxLayout()
        title_stack.setContentsMargins(0, 0, 0, 0)
        title_stack.setSpacing(4)
        title_stack.addWidget(title_label)
        title_stack.addWidget(subtitle)

        traffic_lights = QHBoxLayout()
        traffic_lights.setSpacing(6)
        traffic_lights.setContentsMargins(0, 0, 0, 0)
        traffic_lights.setAlignment(Qt.AlignVCenter)
        for color in ("#ff5f57", "#febc2e", "#28c840"):
            light = QLabel()
            light.setFixedSize(10, 10)
            light.setStyleSheet(
                f"background:{color}; border-radius:5px; border:1px solid rgba(0,0,0,0.08);"
            )
            traffic_lights.addWidget(light)

        left_cluster = QVBoxLayout()
        left_cluster.setContentsMargins(0, 0, 0, 0)
        left_cluster.setSpacing(6)
        left_cluster.setAlignment(Qt.AlignVCenter)
        left_cluster.addLayout(traffic_lights)
        left_cluster.addLayout(title_stack)

        close_button = QToolButton()
        close_button.setObjectName("TitleButton")
        close_button.setText("收起")
        close_button.setFixedHeight(30)
        close_button.clicked.connect(self.close_requested.emit)

        title_layout.addLayout(left_cluster, 0)
        title_layout.addStretch()
        title_layout.addWidget(close_button, 0, Qt.AlignVCenter)

        card_layout.addWidget(title_bar)

        self._status_label.setAlignment(Qt.AlignCenter)
        self._time_label.setAlignment(Qt.AlignCenter)
        self._cycle_label.setAlignment(Qt.AlignCenter)
        self._status_label.setStyleSheet(
            "font-size: 14px; font-weight: 700; color: #9a3412; "
            "background: rgba(255,255,255,0.66); border:1px solid rgba(194,65,12,0.10); "
            "border-radius: 12px; padding: 6px 14px;"
        )
        self._time_label.setStyleSheet(
            "font-size: 58px; font-weight: 800; color: #7c2d12; letter-spacing: 1px;"
        )
        self._cycle_label.setStyleSheet(
            "font-size: 13px; color: #9c6b4f; background: rgba(255,248,241,0.88); "
            "border-radius: 10px; padding: 4px 10px;"
        )

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
        settings_layout.setSpacing(18)

        settings_layout.addWidget(self._build_duration_row("专注时长", self._focus_spin))
        settings_layout.addWidget(self._build_duration_row("短休息", self._short_break_spin))
        settings_layout.addWidget(self._build_duration_row("长休息", self._long_break_spin))

        for spin in (self._focus_spin, self._short_break_spin, self._long_break_spin):
            spin.valueChanged.connect(self._emit_config_change)

        self._startup_checkbox.stateChanged.connect(self._emit_config_change)
        self._topmost_checkbox.stateChanged.connect(self._emit_config_change)

        settings_layout.addWidget(self._build_toggle_row("开机自动启动", self._startup_checkbox))
        settings_layout.addWidget(self._build_toggle_row("悬浮球始终置顶", self._topmost_checkbox))

        footer = QLabel("by sikm")
        footer.setObjectName("FooterLabel")
        footer.setAlignment(Qt.AlignRight)
        settings_layout.addWidget(footer)

        card_layout.addWidget(settings_panel)

        root.addWidget(card)

    def _build_duration_row(self, label_text: str, spin_box: StepperInput) -> QWidget:
        row = QFrame()
        row.setObjectName("SettingRow")
        row.setMinimumHeight(40)
        layout = QHBoxLayout(row)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        layout.setAlignment(Qt.AlignVCenter)

        label = QLabel(label_text)
        label.setObjectName("SettingLabel")
        label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        minute_label = QLabel("分钟")
        minute_label.setObjectName("MinuteLabel")

        layout.addWidget(label, 0, Qt.AlignVCenter)
        layout.addStretch(1)
        layout.addWidget(spin_box, 0, Qt.AlignVCenter)
        layout.addWidget(minute_label, 0, Qt.AlignVCenter)
        return row

    def _build_toggle_row(self, label_text: str, toggle: ToggleSwitch) -> QWidget:
        row = QFrame()
        row.setObjectName("SettingRow")
        row.setMinimumHeight(42)
        layout = QHBoxLayout(row)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        layout.setAlignment(Qt.AlignVCenter)

        label = QLabel(label_text)
        label.setObjectName("SettingLabel")
        label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        toggle.setText("")

        layout.addWidget(label, 0, Qt.AlignVCenter)
        layout.addStretch(1)
        layout.addWidget(toggle, 0, Qt.AlignVCenter)
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
        painter.setBrush(QColor(0, 0, 0, 18))
        painter.drawRoundedRect(self.rect().adjusted(8, 10, -8, -2), 30, 30)

        glow = QLinearGradient(0, 0, self.width(), self.height())
        glow.setColorAt(0.0, QColor(255, 255, 255, 90))
        glow.setColorAt(0.25, QColor(255, 248, 242, 35))
        glow.setColorAt(1.0, QColor(255, 255, 255, 0))
        painter.setBrush(glow)
        painter.drawRoundedRect(self.rect().adjusted(4, 4, -4, -8), 32, 32)
        super().paintEvent(event)
