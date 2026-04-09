from __future__ import annotations

import signal
import sys

from PySide6.QtCore import QTimer
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication

from src.core.timer_engine import TimerEngine
from src.system.autostart import AutoStartManager
from src.system.config import AppConfig, ConfigManager
from src.system.icons import app_icon
from src.system.tray import TrayController
from src.ui.floating_ball import FloatingBall
from src.ui.fullscreen_break import FullscreenBreakController
from src.ui.main_window import MainWindow


class FanqieApplication:
    def __init__(self) -> None:
        self.qt_app = QApplication(sys.argv)
        self.qt_app.setApplicationName("番茄钟")
        self.qt_app.setWindowIcon(app_icon())
        self.qt_app.setQuitOnLastWindowClosed(False)
        self.qt_app.setFont(QFont("Microsoft YaHei", 10))
        signal.signal(signal.SIGINT, self._handle_sigint)
        self._signal_timer = QTimer()
        self._signal_timer.timeout.connect(lambda: None)
        self._signal_timer.start(250)

        self.config_manager = ConfigManager()
        self.config: AppConfig = self.config_manager.load()
        self.timer_engine = TimerEngine(config=self.config)
        self.autostart_manager = AutoStartManager()

        self.main_window = MainWindow(self.timer_engine, self.config)
        self.floating_ball = FloatingBall(self.timer_engine, self.config)
        self.fullscreen_break = FullscreenBreakController(self.timer_engine)
        self.tray = TrayController(self.qt_app, self.timer_engine)

        self._connect_signals()
        self._apply_initial_settings()

    def _connect_signals(self) -> None:
        self.floating_ball.open_requested.connect(self.show_main_window)
        self.floating_ball.position_changed.connect(self._handle_ball_position_changed)
        self.main_window.close_requested.connect(self.hide_main_window)
        self.main_window.config_changed.connect(self._handle_config_changed)

        self.timer_engine.display_updated.connect(self.main_window.update_timer_display)
        self.timer_engine.display_updated.connect(self.floating_ball.update_display)
        self.timer_engine.display_updated.connect(self.fullscreen_break.update_countdown)
        self.timer_engine.state_changed.connect(self.main_window.update_state)
        self.timer_engine.state_changed.connect(self.floating_ball.update_state)
        self.timer_engine.state_changed.connect(self.fullscreen_break.handle_state_changed)
        self.timer_engine.break_prompt_requested.connect(
            self.fullscreen_break.show_break_prompt
        )
        self.timer_engine.break_prompt_requested.connect(
            self.tray.show_break_notification
        )
        self.timer_engine.notification_requested.connect(self.tray.show_message)

        self.fullscreen_break.skip_requested.connect(self.timer_engine.skip_break)
        self.fullscreen_break.snooze_requested.connect(self.timer_engine.snooze_break)
        self.fullscreen_break.close_requested.connect(
            self.timer_engine.dismiss_break_prompt
        )
        self.fullscreen_break.start_next_requested.connect(self.timer_engine.start_focus)

        self.tray.open_requested.connect(self.show_main_window)
        self.tray.start_pause_requested.connect(self._toggle_start_pause)
        self.tray.quit_requested.connect(self.qt_app.quit)

    def _apply_initial_settings(self) -> None:
        self.main_window.update_state(self.timer_engine.state_snapshot())
        self.main_window.update_timer_display(self.timer_engine.display_snapshot())
        self.floating_ball.update_state(self.timer_engine.state_snapshot())
        self.floating_ball.update_display(self.timer_engine.display_snapshot())

        if self.config.launch_on_startup:
            self.autostart_manager.enable()
        else:
            self.autostart_manager.disable()

        self.floating_ball.show()
        self.tray.show()

    def _handle_config_changed(self, config: AppConfig) -> None:
        self.config = config
        self.config_manager.save(config)
        self.timer_engine.apply_config(config)
        self.floating_ball.apply_config(config)
        if config.launch_on_startup:
            self.autostart_manager.enable()
        else:
            self.autostart_manager.disable()

    def _toggle_start_pause(self) -> None:
        if self.timer_engine.is_running:
            self.timer_engine.pause()
            return
        self.timer_engine.start_or_resume()

    def _handle_ball_position_changed(self, x: int, y: int) -> None:
        self.config.floating_position_x = x
        self.config.floating_position_y = y
        self.config_manager.save(self.config)

    def show_main_window(self) -> None:
        self.main_window.show_centered()
        self.main_window.raise_()
        self.main_window.activateWindow()

    def hide_main_window(self) -> None:
        self.main_window.hide()

    def run(self) -> int:
        return self.qt_app.exec()

    def _handle_sigint(self, *_args) -> None:
        self.qt_app.quit()


def main() -> int:
    app = FanqieApplication()
    return app.run()
