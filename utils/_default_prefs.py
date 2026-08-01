
def _default_prefs() -> AdaptiveRouterPreferences:
    """Tier-2 prior with no declared strengths; used when a model omits prefs."""
    return AdaptiveRouterPreferences(quality_tier=2, strengths=[])

