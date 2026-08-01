
def initial_cell(
    prefs: AdaptiveRouterPreferences, request_type: RequestType
) -> BanditCell:
    """
    Cold-start prior for a (model, request_type) cell.

    mean = base_tier_weight[tier] + (STRENGTH_BONUS if request_type in strengths else 0)
    capped at 0.95 to avoid an over-confident prior.
    Total mass = COLD_START_MASS so that ~10 real observations can move it noticeably.
    """
    if prefs.quality_tier not in BASE_TIER_WEIGHT:
        valid = sorted(BASE_TIER_WEIGHT)
        raise ValueError(
            f"quality_tier={prefs.quality_tier} is not supported; "
            f"valid tiers are {valid}"
        )
    base = BASE_TIER_WEIGHT[prefs.quality_tier]
    bonus = STRENGTH_BONUS if request_type in prefs.strengths else 0.0
    mean = min(0.95, base + bonus)
    alpha = mean * COLD_START_MASS
    beta = (1.0 - mean) * COLD_START_MASS
    return BanditCell(alpha=alpha, beta=beta)

