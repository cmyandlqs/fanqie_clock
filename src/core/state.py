from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class TimerState(str, Enum):
    IDLE = "idle"
    FOCUS = "focus"
    SNOOZE = "snooze"
    SHORT_BREAK = "short_break"
    LONG_BREAK = "long_break"
    PAUSED = "paused"
    BREAK_PROMPT = "break_prompt"


@dataclass(slots=True)
class StateSnapshot:
    state: TimerState
    current_cycle: int
    completed_focus_sessions: int
    is_break: bool
    is_running: bool


@dataclass(slots=True)
class DisplaySnapshot:
    total_seconds: int
    remaining_seconds: int
    status_text: str
    time_text: str
