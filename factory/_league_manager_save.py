import json

def load_ratings(elo_file):
    import logging
    logger = logging.getLogger(__name__)
    if elo_file.exists():
        try: return json.loads(elo_file.read_text(encoding="utf-8"))
        except Exception as e: logger.error(f"Failed to load Elo ratings: {e}")
    return {}

def save_ratings(elo_file, ratings):
    import logging
    logger = logging.getLogger(__name__)
    try: elo_file.write_text(json.dumps(ratings, indent=2), encoding="utf-8")
    except Exception as e: logger.error(f"Failed to save Elo ratings: {e}")

def get_neural_opponent_path(checkpoint_id):
    try:
        from factory.model_checkpoint_manager import ModelCheckpointManager
        mcm = ModelCheckpointManager()
        for c in mcm.registry:
            if c["id"] == checkpoint_id: return c["path"]
    except Exception: pass
    return None
