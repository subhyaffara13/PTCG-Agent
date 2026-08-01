
def apply_metagame_weights(current_weights):
    from factory.configs import DEFAULT_ARCHETYPE_WEIGHTS
    meta_dist_path = Path("logs/metagame_distribution.json")
    if not meta_dist_path.exists():
        return False
    try:
        meta_data = json.loads(meta_dist_path.read_text(encoding="utf-8"))
        dominant_meta = meta_data.get("dominant_meta", "")
        if not dominant_meta:
            return False
        logger.info(f"Architecture Team adapting weights to counter dominant meta: {dominant_meta}")
        for arch in current_weights:
            w = list(current_weights[arch])
            if dominant_meta == "Lightning" and arch == "aggro_push":
                w[0] = min(0.7, w[0] + 0.1)
                w[2] = min(0.5, w[2] + 0.1)
            elif dominant_meta == "Fire" and arch == "aggro_push":
                w[1] = min(0.6, w[1] + 0.1)
            total = sum(w)
            current_weights[arch] = tuple(round(x / total, 3) for x in w)
        return True
    except Exception as dist_err:
        logger.warning(f"Failed to parse metagame_distribution.json: {dist_err}")
        return False

