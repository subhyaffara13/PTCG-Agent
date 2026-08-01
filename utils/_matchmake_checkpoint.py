
def _matchmake_checkpoint():
    try:
        from factory.model_checkpoint_manager import ModelCheckpointManager
        mcm = ModelCheckpointManager()
        opp = mcm.load_random_opponent()
        if opp:
            path, info = opp
            c_id = info["id"]
            return c_id, info.get("elo", 1200.0)
    except Exception:
        pass
    return None, None

