from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timedelta

from PySide6.QtCore import QObject, QTimer, Signal

from src.core.state import DisplaySnapshot, StateSnapshot, TimerState
from src.system.config import AppConfig


class TimerEngine(QObject):
    display_updated = Signal(object)
    state_changed = Signal(object)
    break_prompt_requested = Signal(str, int)
    notification_requested = Signal(str, str)

    def __init__(self, config: AppConfig) -> None:
        super().__init__()
        self._config = config
        self._timer = QTimer(self)
        self._timer.setInterval(1000)
        self._timer.timeout.connect(self._on_tick)

        self._state = TimerState.IDLE
        self._state_before_pause = TimerState.IDLE
        self._current_cycle = 1
        self._completed_focus_sessions = 0
        self._duration_seconds = self._config.focus_minutes * 60
        self._remaining_seconds = self._duration_seconds
        self._target_end: datetime | None = None
        self._pending_break_seconds = 0

    @property
    def is_running(self) -> bool:
        return self._timer.isActive() and self._state not in {
            TimerState.IDLE,
            TimerState.BREAK_PROMPT,
            TimerState.PAUSED,
        }

    def apply_config(self, config: AppConfig) -> None:
        self._config = replace(config)
        if self._state in {TimerState.IDLE, TimerState.PAUSED}:
            self._duration_seconds = self._duration_for_state(
                self._state_before_pause or TimerState.FOCUS
            )
            self._remaining_seconds = min(self._remaining_seconds, self._duration_seconds)
            self._emit_all()

    def start_or_resume(self) -> None:
        if self._state == TimerState.PAUSED:
            self._resume_from_pause()
            return
        if self._state in {TimerState.IDLE, TimerState.BREAK_PROMPT}:
            self.start_focus()

    def start_focus(self) -> None:
        self._start_state(TimerState.FOCUS, self._config.focus_minutes * 60)
        self.notification_requested.emit(
            "开始专注", "当前已进入专注计时。"
        )

    def pause(self) -> None:
        if self._state not in {
            TimerState.FOCUS,
            TimerState.SNOOZE,
            TimerState.SHORT_BREAK,
            TimerState.LONG_BREAK,
        }:
            return
        self._remaining_seconds = self._calculate_remaining_seconds()
        self._state_before_pause = self._state
        self._state = TimerState.PAUSED
        self._target_end = None
        self._timer.stop()
        self._emit_all()

    def reset(self) -> None:
        self._timer.stop()
        self._state = TimerState.IDLE
        self._state_before_pause = TimerState.IDLE
        self._current_cycle = 1
        self._completed_focus_sessions = 0
        self._duration_seconds = self._config.focus_minutes * 60
        self._remaining_seconds = self._duration_seconds
        self._target_end = None
        self._emit_all()

    def skip_break(self) -> None:
        if self._state in {
            TimerState.BREAK_PROMPT,
            TimerState.SHORT_BREAK,
            TimerState.LONG_BREAK,
        }:
            self.reset_to_idle("已跳过休息")

    def snooze_break(self) -> None:
        if self._state != TimerState.BREAK_PROMPT:
            return
        self._start_state(TimerState.SNOOZE, 5 * 60)
        self.notification_requested.emit(
            "提醒已延后", "休息提醒已延后 5 分钟。"
        )

    def dismiss_break_prompt(self) -> None:
        if self._state == TimerState.BREAK_PROMPT:
            self.reset_to_idle("已关闭提醒")

    def reset_to_idle(self, message: str | None = None) -> None:
        self._timer.stop()
        self._state = TimerState.IDLE
        self._state_before_pause = TimerState.IDLE
        self._duration_seconds = self._config.focus_minutes * 60
        self._remaining_seconds = self._duration_seconds
        self._target_end = None
        self._pending_break_seconds = 0
        self._emit_all()
        if message:
            self.notification_requested.emit(message, "等待开始下一轮专注。")

    def state_snapshot(self) -> StateSnapshot:
        active_state = self._state_before_pause if self._state == TimerState.PAUSED else self._state
        return StateSnapshot(
            state=self._state,
            current_cycle=self._current_cycle,
            completed_focus_sessions=self._completed_focus_sessions,
            is_break=active_state in {TimerState.SHORT_BREAK, TimerState.LONG_BREAK},
            is_running=self.is_running,
        )

    def display_snapshot(self) -> DisplaySnapshot:
        remaining = self._calculate_remaining_seconds()
        total = self._duration_seconds if self._duration_seconds > 0 else remaining
        return DisplaySnapshot(
            total_seconds=total,
            remaining_seconds=remaining,
            status_text=self._status_text(),
            time_text=self._format_seconds(remaining),
        )

    def _resume_from_pause(self) -> None:
        resumed_state = (
            self._state_before_pause
            if self._state_before_pause != TimerState.IDLE
            else TimerState.FOCUS
        )
        self._start_state(resumed_state, self._remaining_seconds)

    def _start_state(self, state: TimerState, duration_seconds: int) -> None:
        self._state = state
        self._duration_seconds = max(duration_seconds, 1)
        self._remaining_seconds = self._duration_seconds
        self._target_end = datetime.now() + timedelta(seconds=self._duration_seconds)
        self._timer.start()
        self._emit_all()

    def _on_tick(self) -> None:
        remaining = self._calculate_remaining_seconds()
        if remaining <= 0:
            self._timer.stop()
            self._complete_current_state()
            return
        self._remaining_seconds = remaining
        self.display_updated.emit(self.display_snapshot())

    def _complete_current_state(self) -> None:
        completed_state = self._state
        self._target_end = None
        if completed_state == TimerState.FOCUS:
            self._completed_focus_sessions += 1
            self._current_cycle = (
                ((self._completed_focus_sessions - 1) % self._config.cycles_before_long_break)
                + 1
            )
            break_seconds = self._next_break_duration()
            self._pending_break_seconds = break_seconds
            self._state = TimerState.BREAK_PROMPT
            self._duration_seconds = break_seconds
            self._remaining_seconds = break_seconds
            self._target_end = datetime.now() + timedelta(seconds=break_seconds)
            self._timer.start()
            prompt_text = (
                "该休息一下了"
                if self._is_long_break_due()
                else "该休息一下了"
            )
            self._emit_all()
            self.break_prompt_requested.emit(prompt_text, break_seconds)
            return

        if completed_state == TimerState.SNOOZE:
            self._state = TimerState.BREAK_PROMPT
            self._duration_seconds = self._pending_break_seconds or (
                self._config.short_break_minutes * 60
            )
            self._remaining_seconds = self._duration_seconds
            self._target_end = datetime.now() + timedelta(seconds=self._duration_seconds)
            self._timer.start()
            self._emit_all()
            self.break_prompt_requested.emit(
                "休息提醒已恢复", self._duration_seconds
            )
            return

        if completed_state == TimerState.BREAK_PROMPT:
            self.reset_to_idle("休息结束")
            return

        if completed_state in {TimerState.SHORT_BREAK, TimerState.LONG_BREAK}:
            self.reset_to_idle("休息结束")

    def _next_break_duration(self) -> int:
        if self._is_long_break_due():
            return self._config.long_break_minutes * 60
        return self._config.short_break_minutes * 60

    def _is_long_break_due(self) -> bool:
        return self._completed_focus_sessions % self._config.cycles_before_long_break == 0

    def _duration_for_state(self, state: TimerState) -> int:
        if state == TimerState.LONG_BREAK:
            return self._config.long_break_minutes * 60
        if state == TimerState.SHORT_BREAK:
            return self._config.short_break_minutes * 60
        if state == TimerState.SNOOZE:
            return 5 * 60
        return self._config.focus_minutes * 60

    def _calculate_remaining_seconds(self) -> int:
        if self._state == TimerState.PAUSED:
            return self._remaining_seconds
        if self._target_end is None:
            return self._remaining_seconds
        delta = self._target_end - datetime.now()
        return max(int(delta.total_seconds()), 0)

    def _status_text(self) -> str:
        mapping = {
            TimerState.IDLE: "待开始",
            TimerState.FOCUS: "专注中",
            TimerState.SNOOZE: "已延后",
            TimerState.SHORT_BREAK: "短休息",
            TimerState.LONG_BREAK: "长休息",
            TimerState.PAUSED: "已暂停",
            TimerState.BREAK_PROMPT: "休息提醒",
        }
        return mapping[self._state]

    def _format_seconds(self, total_seconds: int) -> str:
        minutes, seconds = divmod(max(total_seconds, 0), 60)
        return f"{minutes:02d}:{seconds:02d}"

    def _emit_all(self) -> None:
        self.state_changed.emit(self.state_snapshot())
        self.display_updated.emit(self.display_snapshot())
