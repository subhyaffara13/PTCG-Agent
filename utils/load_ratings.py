
def load_ratings(elo_file):
    import logging
    logger = logging.getLogger(__name__)
    if elo_file.exists():
        try: return json.loads(elo_file.read_text(encoding="utf-8"))
        except Exception as e: logger.error(f"Failed to load Elo ratings: {e}")
    return {}

