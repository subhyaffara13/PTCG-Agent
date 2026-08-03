from typing import List, Optional, Union

def _is_model_cost_zero(
    model: Optional[Union[str, List[str]]], llm_router: Optional[Router]
) -> bool:
    """
    Check if a model has zero cost (no configured pricing).

    Uses the router's get_model_group_info method to get pricing information.

    Args:
        model: The model name or list of model names
        llm_router: The LiteLLM router instance

    Returns:
        bool: True if all costs for the model are zero, False otherwise
    """
    if model is None or llm_router is None:
        return False

    # Handle list of models
    model_list = [model] if isinstance(model, str) else model

    zero_cost_cache = _get_router_zero_cost_cache(llm_router)

    for model_name in model_list:
        if zero_cost_cache is not None:
            cached = zero_cost_cache.get(model_name)
            if cached is not None:
                if cached is False:
                    return False
                continue
        try:
            # Use router's get_model_group_info method directly for better reliability
            model_group_info = llm_router.get_model_group_info(model_group=model_name)

            if model_group_info is None:
                # Model not found or no pricing info available
                # Conservative approach: assume it has cost
                verbose_proxy_logger.debug(
                    f"No model group info found for {model_name}, assuming it has cost"
                )
                if zero_cost_cache is not None:
                    zero_cost_cache[model_name] = False
                return False

            # Check costs for this model
            # Only allow bypass if BOTH costs are explicitly set to 0 (not None)
            input_cost = model_group_info.input_cost_per_token
            output_cost = model_group_info.output_cost_per_token

            # If costs are not explicitly configured (None), assume it has cost
            if input_cost is None or output_cost is None:
                verbose_proxy_logger.debug(
                    f"Model {model_name} has undefined cost (input: {input_cost}, output: {output_cost}), assuming it has cost"
                )
                if zero_cost_cache is not None:
                    zero_cost_cache[model_name] = False
                return False

            # If either cost is non-zero, return False
            if input_cost > 0 or output_cost > 0:
                verbose_proxy_logger.debug(
                    f"Model {model_name} has non-zero cost (input: {input_cost}, output: {output_cost})"
                )
                if zero_cost_cache is not None:
                    zero_cost_cache[model_name] = False
                return False

            # Costs are 0 — verify this is from explicit configuration,
            # not from defaulted sparse auto-registration entries.
            # See: https://github.com/BerriAI/litellm/issues/24770
            safe_name = str(model_name).replace("\n", "").replace("\r", "")
            if not _is_cost_explicitly_configured(model_name, llm_router):
                verbose_proxy_logger.debug(
                    "Model %s has zero cost but no explicit cost "
                    "configuration in model_cost entry — treating as unknown "
                    "cost (enforce budget)",
                    safe_name,
                )
                if zero_cost_cache is not None:
                    zero_cost_cache[model_name] = False
                return False

            verbose_proxy_logger.debug(
                "Model %s has zero cost explicitly configured (input: %s, output: %s)",
                safe_name,
                input_cost,
                output_cost,
            )
            if zero_cost_cache is not None:
                zero_cost_cache[model_name] = True

        except Exception as e:
            # If we can't determine the cost, assume it has cost (conservative approach)
            verbose_proxy_logger.debug(
                f"Error checking cost for model {model_name}: {str(e)}, assuming it has cost"
            )
            return False

    # All models checked have zero cost
    return True

