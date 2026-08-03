import json

def save_ratings(elo_file, ratings):
    import logging
    logger = logging.getLogger(__name__)
    try: elo_file.write_text(json.dumps(ratings, indent=2), encoding="utf-8")
    except Exception as e: logger.error(f"Failed to save Elo ratings: {e}")

