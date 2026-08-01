
def load_processed_players(processed_file: Path) -> dict:
    if processed_file.exists():
        try:
            return json.loads(processed_file.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}

