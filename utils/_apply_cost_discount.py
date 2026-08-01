
def _apply_cost_discount(
    base_cost: float,
    custom_llm_provider: Optional[str],
) -> Tuple[float, float, float]:
    """
    Apply provider-specific cost discount from module-level config.

    Args:
        base_cost: The base cost before discount
        custom_llm_provider: The LLM provider name

    Returns:
        Tuple of (final_cost, discount_percent, discount_amount)
    """
    original_cost = base_cost
    discount_percent = 0.0
    discount_amount = 0.0

    if custom_llm_provider and custom_llm_provider in litellm.cost_discount_config:
        discount_percent = litellm.cost_discount_config[custom_llm_provider]
        discount_amount = original_cost * discount_percent
        final_cost = original_cost - discount_amount

        if verbose_logger.isEnabledFor(logging.DEBUG):
            verbose_logger.debug(
                f"Applied {discount_percent*100}% discount to {custom_llm_provider}: "
                f"${original_cost:.6f} -> ${final_cost:.6f} (saved ${discount_amount:.6f})"
            )

        return final_cost, discount_percent, discount_amount

    return base_cost, discount_percent, discount_amount

