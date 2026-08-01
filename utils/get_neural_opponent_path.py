
def get_neural_opponent_path(checkpoint_id):
    try:
        from factory.model_checkpoint_manager import ModelCheckpointManager
        mcm = ModelCheckpointManager()
        for c in mcm.registry:
            if c["id"] == checkpoint_id: return c["path"]
    except Exception: pass
    return None

