# Game Level Editor

A Python tile-map editor with JSON save/load and asset checks.

This is a small, independent Python portfolio project. The code favours ordinary functions and clear modules over complex architecture.

## Setup

Requires Python 3.12+ (desktop tools also require Tkinter, included with the standard Windows Python installer).

```sh
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux instead: source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python editor.py
```

Run commands from this repository's root. Web apps bind to localhost by default. Each app is independent, so stop one before starting another on the same port.

## Check it

```sh
python -m pytest -q
```

## Dates

The commit author dates have been deliberately arranged between October 2025 and October 2026 at the portfolio owner's request. They are presentation metadata, not a record of the actual development timeline. Repository creation and upload timestamps remain the real dates.

## Use the editor

Paint with the left mouse button or drag; right click erases. Select wall, water, grass or empty in the toolbar. The default map is 20×15. Open JSON maps between 5–40 columns and 5–30 rows; invalid maps leave the current map intact. Save produces readable JSON with a version, width, height and row-major tile array. Unsaved changes prompt before closing or replacing a map.

**Check asset folder** reports repeated asset stems, unsupported extensions and files larger than 10 MB. It is a validator, not a texture optimizer. `samples/demo-map.json` contains a sample map. This adapts the C++/C# engine tool idea to an independent Python editor and file parsing module. Linux may require `python3-tk` from your system package manager.
