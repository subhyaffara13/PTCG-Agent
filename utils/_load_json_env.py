
def _load_json_env(var_name: str) -> Optional[Dict[str, Any]]:
    raw = os.environ.get(var_name)
    if not raw:
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return None

