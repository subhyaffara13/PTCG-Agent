
def _has_priorities(model_preferences: "ModelPreferences") -> bool:
    """Return True if any priority weight is set (non-None and > 0)."""
    return any(
        (getattr(model_preferences, attr, None) or 0) > 0
        for attr in ("costPriority", "speedPriority", "intelligencePriority")
    )

