
def _try_load_json(path, default=None):
    import json
    if default is None: default = {}
    try:
        if path.exists(): return json.loads(path.read_text(encoding="utf-8"))
    except Exception: pass
    return default

