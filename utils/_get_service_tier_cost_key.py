from typing import Optional

def _get_service_tier_cost_key(base_key: str, service_tier: Optional[str]) -> str:
    """
    Get the appropriate cost key based on service tier.

    Args:
        base_key: The base cost key (e.g., "input_cost_per_token")
        service_tier: The service tier ("flex", "priority", or None for standard)

    Returns:
        str: The cost key to use (e.g., "input_cost_per_token_flex" or "input_cost_per_token")
    """
    if service_tier is None:
        return base_key

    # Only use service tier specific keys for "flex" and "priority"
    if service_tier.lower() in [ServiceTier.FLEX.value, ServiceTier.PRIORITY.value]:
        return f"{base_key}_{service_tier.lower()}"

    # For any other service tier, use standard pricing
    return base_key

