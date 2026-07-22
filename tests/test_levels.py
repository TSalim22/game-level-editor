import pytest
from levels import new_level, paint, save_level, load_level, validate, check_assets


def test_map_roundtrip_and_bounds(tmp_path):
    level = new_level()
    paint(level,2,3,1)
    paint(level,-1,0,2)
    path = tmp_path/'map.json'
    save_level(path,level)
    assert load_level(path)['tiles'][3][2] == 1
    assert level['tiles'][0][-1] == 0
    level['tiles'][0][0] = True
    with pytest.raises(ValueError): validate(level)


def test_asset_checks(tmp_path):
    (tmp_path/'wall.png').write_bytes(b'demo')
    (tmp_path/'wall.jpg').write_bytes(b'demo')
    (tmp_path/'notes.exe').write_bytes(b'demo')
    messages = check_assets(tmp_path)
    assert any('Duplicate' in m for m in messages)
    assert any('Unsupported' in m for m in messages)
