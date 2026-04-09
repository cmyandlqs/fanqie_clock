from __future__ import annotations

from PySide6.QtCore import QCoreApplication

from src.core.timer_engine import TimerEngine
from src.core.state import TimerState
from src.system.config import AppConfig


def ensure_app() -> QCoreApplication:
    app = QCoreApplication.instance()
    if app is None:
        app = QCoreApplication([])
    return app


def make_engine() -> TimerEngine:
    ensure_app()
    config = AppConfig(
        focus_minutes=25,
        short_break_minutes=4,
        long_break_minutes=8,
        cycles_before_long_break=4,
    )
    return TimerEngine(config)


def test_start_focus_sets_focus_state() -> None:
    engine = make_engine()
    engine.start_focus()
    snapshot = engine.state_snapshot()
    assert snapshot.state == TimerState.FOCUS
    assert snapshot.is_running is True


def test_pause_changes_state() -> None:
    engine = make_engine()
    engine.start_focus()
    engine.pause()
    snapshot = engine.state_snapshot()
    assert snapshot.state == TimerState.PAUSED
    assert snapshot.is_running is False


def test_reset_returns_to_idle() -> None:
    engine = make_engine()
    engine.start_focus()
    engine.reset()
    snapshot = engine.state_snapshot()
    display = engine.display_snapshot()
    assert snapshot.state == TimerState.IDLE
    assert display.time_text == "25:00"


def test_skip_break_returns_to_idle() -> None:
    engine = make_engine()
    engine._state = TimerState.BREAK_PROMPT
    engine.skip_break()
    assert engine.state_snapshot().state == TimerState.IDLE
