import logging
logger = logging.getLogger(__name__)

def _try_load_json(path, default=None):
    import json
    if default is None: default = {}
    try:
        if path.exists(): return json.loads(path.read_text(encoding="utf-8"))
    except Exception: pass
    return default

def _load_log_content(path):
    if not path.exists(): return []
    import json
    try:
        content = path.read_text(encoding="utf-8").strip()
        if not content: return []
        if content.startswith("[") and content.endswith("]"):
            try: return json.loads(content)
            except: pass
        return [json.loads(line) for line in content.splitlines() if line.strip()]
    except Exception as e:
        logging.getLogger(__name__).error(f"Failed to load log file {path.name}: {e}")
    return []
