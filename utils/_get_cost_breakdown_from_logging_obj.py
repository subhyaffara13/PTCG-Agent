from typing import Optional, Tuple

def _get_cost_breakdown_from_logging_obj(
    litellm_logging_obj: Optional[LiteLLMLoggingObj],
) -> Tuple[Optional[float], Optional[float], Optional[float], Optional[float]]:
    """
    Extract discount and margin information from logging object's cost breakdown.

    Returns:
        Tuple of (original_cost, discount_amount, margin_total_amount, margin_percent)
    """
    if not litellm_logging_obj or not hasattr(litellm_logging_obj, "cost_breakdown"):
        return None, None, None, None

    cost_breakdown = litellm_logging_obj.cost_breakdown
    if not cost_breakdown:
        return None, None, None, None

    original_cost = cost_breakdown.get("original_cost")
    discount_amount = cost_breakdown.get("discount_amount")
    margin_total_amount = cost_breakdown.get("margin_total_amount")
    margin_percent = cost_breakdown.get("margin_percent")

    return original_cost, discount_amount, margin_total_amount, margin_percent

