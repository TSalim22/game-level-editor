import json
from pathlib import Path

TILES = {0:('Empty','#edf1f7'),1:('Wall','#253552'),2:('Water','#389ada'),3:('Grass','#65ad6b')}


def new_level(width=20,height=15):
    if not 5<=width<=40 or not 5<=height<=30:
        raise ValueError('Width must be 5–40 and height 5–30.')
    return {'version':1,'width':width,'height':height,'tiles':[[0]*width for _ in range(height)]}


def validate(level):
    if not isinstance(level,dict) or level.get('version') != 1:
        raise ValueError('Unsupported map format.')
    width,height = level.get('width'),level.get('height')
    if type(width) is not int or type(height) is not int or not 5<=width<=40 or not 5<=height<=30:
        raise ValueError('Invalid map dimensions.')
    tiles = level.get('tiles')
    if not isinstance(tiles,list) or len(tiles)!=height:
        raise ValueError('Row count does not match height.')
    for row in tiles:
        if not isinstance(row,list) or len(row)!=width or any(type(tile) is not int or tile not in TILES for tile in row):
            raise ValueError('Invalid row or unknown tile type.')
    return level


def load_level(path):
    if Path(path).stat().st_size > 2*1024*1024:
        raise ValueError('Map file is too large.')
    return validate(json.loads(Path(path).read_text(encoding='utf-8')))


def save_level(path,level):
    validate(level)
    target = Path(path)
    temporary = target.with_suffix(target.suffix+'.tmp')
    temporary.write_text(json.dumps(level,indent=2)+'\n',encoding='utf-8')
    temporary.replace(target)


def paint(level,x,y,tile):
    if type(tile) is not int or tile not in TILES:
        raise ValueError('Unknown tile.')
    if 0<=x<level['width'] and 0<=y<level['height']:
        level['tiles'][y][x] = tile


def check_assets(folder):
    messages = []
    seen = set()
    files = [path for path in Path(folder).iterdir() if path.is_file()]
    for path in files:
        if path.stem.casefold() in seen:
            messages.append(f'Duplicate asset name: {path.stem}')
        seen.add(path.stem.casefold())
        if path.suffix.lower() not in ('.png','.jpg','.jpeg','.wav','.ogg','.json'):
            messages.append(f'Unsupported asset extension: {path.name}')
        if path.stat().st_size > 10*1024*1024:
            messages.append(f'Large asset (>10 MB): {path.name}')
    return messages or [f'{len(files)} files checked; no naming, size or extension issues found.']
