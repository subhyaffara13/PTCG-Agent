
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

