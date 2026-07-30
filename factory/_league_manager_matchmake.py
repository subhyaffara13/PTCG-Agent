import random

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

def _matchmake_exploiter(ratings):
    exploiters = ["aggro_exploiter", "control_exploiter", "combo_exploiter"]
    weights = [ratings.get(e, 1200) for e in exploiters]
    return random.choices(exploiters, weights=weights, k=1)[0]
