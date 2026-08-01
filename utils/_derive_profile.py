
def _derive_profile(hand_score: float) -> str:
    from cb_agents.hand_analyst_helpers import derive_profile_helper
    return derive_profile_helper(hand_score, _PROFILE_THRESHOLDS)


def _derive_profile(hand_score: float) -> str:
    from cb_agents.hand_analyst_helpers import derive_profile_helper
    return derive_profile_helper(hand_score, _PROFILE_THRESHOLDS)

