import logging
from typing import Optional, Tuple

def _apply_cost_margin(
    base_cost: float,
    custom_llm_provider: Optional[str],
) -> Tuple[float, float, float, float]:
    """
    Apply provider-specific or global cost margin from module-level config.

    Args:
        base_cost: The base cost before margin (after discount if applicable)
        custom_llm_provider: The LLM provider name

    Returns:
        Tuple of (final_cost, margin_percent, margin_fixed_amount, margin_total_amount)
    """
    original_cost = base_cost
    margin_percent = 0.0
    margin_fixed_amount = 0.0
    margin_total_amount = 0.0

    # Get margin config - check provider-specific first, then global
    margin_config = None
    if custom_llm_provider and custom_llm_provider in litellm.cost_margin_config:
        margin_config = litellm.cost_margin_config[custom_llm_provider]
        if verbose_logger.isEnabledFor(logging.DEBUG):
            verbose_logger.debug(
                f"Found provider-specific margin config for {custom_llm_provider}: {margin_config}"
            )
    elif "global" in litellm.cost_margin_config:
        margin_config = litellm.cost_margin_config["global"]
        if verbose_logger.isEnabledFor(logging.DEBUG):
            verbose_logger.debug(f"Using global margin config: {margin_config}")
    else:
        if verbose_logger.isEnabledFor(logging.DEBUG):
            verbose_logger.debug(
                f"No margin config found. Provider: {custom_llm_provider}, "
                f"Available configs: {list(litellm.cost_margin_config.keys())}"
            )

    if margin_config is not None:
        # Handle different margin config formats
        if isinstance(margin_config, (int, float)):
            # Simple percentage: {"openai": 0.10}
            margin_percent = float(margin_config)
            margin_total_amount = original_cost * margin_percent
        elif isinstance(margin_config, dict):
            # Complex config: {"percentage": 0.08, "fixed_amount": 0.0005}
            if "percentage" in margin_config:
                margin_percent = float(margin_config["percentage"])
                margin_total_amount += original_cost * margin_percent
            if "fixed_amount" in margin_config:
                margin_fixed_amount = float(margin_config["fixed_amount"])
                margin_total_amount += margin_fixed_amount

        final_cost = original_cost + margin_total_amount

        if verbose_logger.isEnabledFor(logging.DEBUG):
            verbose_logger.debug(
                f"Applied margin to {custom_llm_provider or 'global'}: "
                f"${original_cost:.6f} -> ${final_cost:.6f} "
                f"(margin: {margin_percent*100 if margin_percent > 0 else 0}% + ${margin_fixed_amount:.6f} = ${margin_total_amount:.6f})"
            )

        return final_cost, margin_percent, margin_fixed_amount, margin_total_amount

    return base_cost, margin_percent, margin_fixed_amount, margin_total_amount

