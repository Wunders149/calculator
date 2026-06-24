# Calculatrice Scientifique

A scientific calculator desktop application with both **GUI** (Tkinter) and **CLI** interfaces. Features trigonometric functions, logarithms, factorials, constants, and more — with a dark theme and safe expression evaluation.

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

## Project Structure

| File | Description |
|---|---|
| `calculator_gui.py` | Tkinter GUI application (533 lines) |
| `calculator.py` | Terminal-based CLI application |
| `calculator_math.py` | Shared math functions + safe AST evaluator |
| `test_calculator.py` | 63 unit tests |
| `calculator_gui.spec` | PyInstaller build configuration |
| `run_calc.bat` | Quick-launch batch script |
| `fix.ps1` | Helper script (encoding fix) |

## Architecture

- **`calculator_math.py`** contains all mathematical operations and a whitelist-based AST expression evaluator (`safe_eval`). It replaces the original `eval()` approach with a secure recursive tree walker.
- **`calculator_gui.py`** builds the Tkinter UI, handles button/keyboard input, and delegates evaluation to `calculator_math`.
- **`calculator.py`** provides the same functionality through a menu-driven terminal interface.

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
