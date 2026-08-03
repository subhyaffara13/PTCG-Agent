import json
from pathlib import Path


def save_processed_players(processed_file: Path, processed_players: dict):
    try:
        processed_file.write_text(json.dumps(processed_players, indent=2), encoding="utf-8")
    except Exception as e:
        logger.error(f"Failed to save leaderboard players: {e}")

