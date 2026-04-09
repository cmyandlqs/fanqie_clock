from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(slots=True)
class AppConfig:
    focus_minutes: int = 25
    short_break_minutes: int = 4
    long_break_minutes: int = 8
    cycles_before_long_break: int = 4
    floating_always_on_top: bool = True
    floating_position_x: int = 120
    floating_position_y: int = 120
    launch_on_startup: bool = True
    allow_multiple_snooze: bool = True


class ConfigManager:
    def __init__(self) -> None:
        self._config_dir = Path.home() / "AppData" / "Local" / "FanqieClock"
        self._config_file = self._config_dir / "config.json"

    def load(self) -> AppConfig:
        if not self._config_file.exists():
            return AppConfig()
        try:
            data = json.loads(self._config_file.read_text(encoding="utf-8"))
            return AppConfig(**data)
        except (OSError, ValueError, TypeError):
            return AppConfig()

    def save(self, config: AppConfig) -> None:
        self._config_dir.mkdir(parents=True, exist_ok=True)
        self._config_file.write_text(
            json.dumps(asdict(config), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
