# Game Level Editor

A desktop tool for creating tile maps and saving them as JSON.

## Run it

Python 3.12 or later. Run these commands from the project folder:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
python editor.py
```

On macOS or Linux, activate with `source .venv/bin/activate` instead.

## How to use it

Left click or drag to paint. Right click to erase. Choose empty, wall, water or grass from the menu.

Use **Open** and **Save** for JSON maps. Try `samples/demo-map.json`. **Check asset folder** finds duplicate names, unsupported files and files over 10 MB.

Maps support 5–40 columns and 5–30 rows. Linux may need `python3-tk`.

## Tests

```sh
python -m pytest -q
```
