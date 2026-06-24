# Calculatrice Scientifique

A scientific calculator application with **desktop** (Tkinter GUI + CLI) and **mobile** (Web + Kivy) interfaces. Features trigonometric functions, logarithms, factorials, constants, and more — with a dark Catppuccin theme and safe AST-based expression evaluation.

## Features

- **Basic operations**: `+`, `-`, `*`, `/`, `^`, `%` (modulo)
- **Trigonometry**: `sin`, `cos`, `tan` with **DEG / RAD** toggle
- **Logarithms**: `log` (base 10), `ln` (natural)
- **Advanced**: `√` (sqrt), `x²` (square), `x^y` (power), `!` (factorial), `1/x` (inverse)
- **Constants**: `π` (pi), `e`
- **Parentheses** and implicit multiplication (`2π`, `5(3+2)`)
- **Result chaining**: after `=`, pressing an operator continues from the result
- **Keyboard input** (GUI): digits, operators, Enter, Backspace, Delete, Escape
- **Dark theme** with Catppuccin-inspired colors
- **DPI-aware**: scales on high-resolution displays
- **Safe evaluation**: AST-based expression parser — no `eval()` — blocks malicious input
- **Mobile responsive web app**: Flask backend, touch-friendly layout, works on any device
- **63 unit tests**: full coverage of math operations and edge cases

## Getting Started

### Requirements

- Python 3.8+

### Run the GUI

```bash
python calculator_gui.py
```

### Run the CLI

```bash
python calculator.py
```

### Run the Web App (mobile-friendly)

```bash
pip install flask
python calculator_web.py
```

Then open `http://localhost:5000` or `http://<YOUR_IP>:5000` on any device on the same network.

## Build a Desktop Executable

The project uses **PyInstaller** to package the GUI into a standalone `.exe`.

### 1. Install PyInstaller

```bash
pip install pyinstaller
```

### 2. Build

```bash
pyinstaller calculator_gui.spec
```

The executable is produced at `dist/calculator_gui.exe`.

> **Note:** If the `.spec` file is missing or outdated, regenerate it:
> ```bash
> pyinstaller --onefile --windowed --name calculator_gui calculator_gui.py
> ```
> The `--windowed` flag suppresses the console window on Windows. The build
> automatically includes `calculator_math.py` as a detected import.

### 3. Run the executable

```bash
dist\calculator_gui.exe
```

The resulting executable is **~11 MB** (standalone, no Python required).

## Mobile App

Two options are available: a **web app** (recommended, works on all devices immediately) and a **Kivy APK** (native Android).

### Option 1 — Web App (recommended)

A Flask-based web version with a touch-optimized, mobile-responsive UI. Runs on your computer and is accessible from any phone or tablet on the same network with no installation required on the device.

```bash
# Install Flask
pip install flask

# Start the server
python calculator_web.py
```

Then open `http://<YOUR_IP>:5000` on your phone (find your IP with `ipconfig` on Windows, or `ifconfig` on Linux/macOS).

> **Web UI features:** accent bar, equal-height button grid, responsive `clamp()` typography, visual press feedback (scale + brightness), smooth animations, and Catppuccin color scheme — all optimised for touch on small screens up to tablets.

> **Note:** The web app evaluates expressions **server-side** using `calculator_math.py`,
> keeping the same safe AST-based evaluator as the desktop version.

### Option 2 — Native Android APK (Kivy)

A **Kivy**-based mobile version is included at `calculator_mobile.py`.

#### Test on desktop

```bash
pip install kivy       # requires Python 3.8–3.12
python calculator_mobile.py
```

#### Build APK with Buildozer

Requires **Linux** or **WSL 2** (Windows):

```bash
# Inside Ubuntu/WSL:
sudo apt update && sudo apt install -y python3-pip git zip unzip openjdk-17-jdk
pip install buildozer

# Build the APK
buildozer android debug
```

The APK is produced at `bin/calculator-2.0-arm64-v8a-debug.apk`.

> **Note:** Kivy does not yet support Python 3.13+. On Python 3.14+, use the web app
> (Option 1) or create a virtual environment with Python 3.12:
> ```bash
> pip install virtualenv
> virtualenv -p python3.12 venv
> venv\Scripts\activate    # Windows
> pip install kivy
> python calculator_mobile.py
> ```

## Project Structure

| File | Description |
|---|---|
| `calculator_gui.py` | Tkinter GUI application |
| `calculator.py` | Terminal-based CLI application |
| `calculator_mobile.py` | Kivy mobile app (Android / iOS) |
| `calculator_web.py` | Flask web app (mobile-responsive, touch-optimised) |
| `calculator_math.py` | Shared math functions + safe AST evaluator |
| `test_calculator.py` | 63 unit tests covering all operations and edge cases |
| `calculator_gui.spec` | PyInstaller build configuration |
| `buildozer.spec` | Android build configuration |
| `run_calc.bat` | Quick-launch batch script |
| `fix.ps1` | Helper script (encoding fix) |

## Architecture

- **`calculator_math.py`** contains all mathematical operations and a whitelist-based AST expression evaluator (`safe_eval`). It replaces the original `eval()` approach with a secure recursive tree walker.
- **`calculator_gui.py`** builds the Tkinter UI, handles button/keyboard input, and delegates evaluation to `calculator_math`.
- **`calculator.py`** provides the same functionality through a menu-driven terminal interface.
- **`calculator_web.py`** serves a Flask web app. The front-end (inline HTML/CSS/JS) renders a responsive, touch-friendly calculator and sends expressions to the server for safe AST-based evaluation.
- **`calculator_mobile.py`** is a Kivy-based app for native mobile deployment (requires Python 3.8–3.12 to run).

## Keyboard Shortcuts (GUI)

| Key | Action |
|---|---|
| `0`-`9` | Enter digit |
| `+` `-` `*` `/` `%` `.` `(` `)` | Operators / punctuation |
| `p` | Insert π |
| `e` | Insert e |
| `Enter` | Evaluate (=) |
| `Backspace` | Delete last character |
| `Delete` / `Escape` | Clear all |
