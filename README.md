# Fanqie Clock

A lightweight desktop Pomodoro timer for Windows built with **PySide6**.  
It focuses on a clean floating timer, a polished control window, and a strong full-screen break reminder.

## Preview

![Main Window](imgs/主界面.jpg)
![Break Reminder](imgs/休息.jpg)

## Features

- Small floating timer ball with drag support
- Focus / short break / long break cycle
- Full-screen break reminder across displays
- Tray integration and background running
- Launch on startup
- Local config persistence
- macOS-inspired visual style

## Tech Stack

- Python 3.13
- PySide6
- pytest
- PyInstaller for Windows packaging

## Getting Started

### 1. Create and activate a virtual environment

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

### 3. Run the app

```powershell
python -m src.main
```

## Tests

```powershell
python -m pytest tests\test_timer_engine.py -p no:cacheprovider
```

## Packaging

To build a local Windows distributable:

```powershell
pip install pyinstaller
pyinstaller FanqieClock.spec
```

The packaged app will be generated under `dist/FanqieClock/`.

## Project Structure

```text
src/
  core/      timer engine and state
  system/    tray, autostart, config, icons
  ui/        floating ball, main window, break overlay
assets/      icon and visual assets
tests/       automated tests
```

## Roadmap

- Refine break-screen acrylic effect
- Improve Windows packaging and installer flow
- Add more UI polish and runtime validation

## License

MIT
