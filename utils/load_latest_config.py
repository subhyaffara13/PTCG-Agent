
def load_latest_config(r):
    """Fetch the latest archetype and model weights from Redis or local cache."""
    if not r:
        return "aggro", None
    try:
        archetype = r.get("ptcg:latest_archetype")
        archetype = archetype.decode("utf-8") if archetype else "aggro"
        weights_bytes = r.get("ptcg:latest_weights")
        weights = pickle.loads(weights_bytes) if weights_bytes else None  # nosec B301
        return archetype, weights
    except Exception as e:
        logger.warning(f"Failed to load configuration from Redis: {e}")
        return "aggro", None

