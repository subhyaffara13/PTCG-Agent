
def _resolve_market_params(overrides):
    """Merge per-resource overrides onto MARKET_PARAMS defaults (sparse)."""
    resolved = {item: dict(p) for item, p in MARKET_PARAMS.items()}
    if not overrides:
        return resolved
    for item, patch in overrides.items():
        if item in resolved and isinstance(patch, dict):
            resolved[item].update(patch)
    return resolved

