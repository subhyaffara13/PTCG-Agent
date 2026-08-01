
def _normalize_service_tier(service_tier: object) -> str | None:
    """
    Reduce a service_tier value to a concrete billable tier string or None.

    "auto" is a routing preference and any non-string value is not a billable
    tier, so both defer to standard pricing (or to the tier the provider reports
    on the response usage) instead of crashing the downstream cost-key lookup,
    which calls service_tier.lower()
    """
    if (
        not isinstance(service_tier, str)
        or service_tier.lower() == ServiceTier.AUTO.value
    ):
        return None
    return service_tier

