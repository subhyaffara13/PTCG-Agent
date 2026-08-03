from typing import Optional, Tuple

def batch_cost_calculator(
    usage: Usage,
    model: str,
    custom_llm_provider: Optional[str] = None,
    model_info: Optional[ModelInfo] = None,
    data_residency: Optional[str] = None,
) -> Tuple[float, float]:
    """
    Calculate the cost of a batch job.

    Args:
        model_info: Optional deployment-level model info containing custom
            batch pricing (e.g. input_cost_per_token_batches). When provided,
            skips the global litellm.get_model_info() lookup so that
            deployment-specific pricing is used.
    """

    _, custom_llm_provider, _, _ = litellm.get_llm_provider(
        model=model, custom_llm_provider=custom_llm_provider
    )

    verbose_logger.debug(
        "Calculating batch cost per token. model=%s, custom_llm_provider=%s",
        model,
        custom_llm_provider,
    )

    if model_info is None:
        try:
            model_info = litellm.get_model_info(
                model=model, custom_llm_provider=custom_llm_provider
            )
        except Exception:
            model_info = None
    elif not any(
        model_info.get(k) is not None
        for k in (
            "input_cost_per_token_batches",
            "input_cost_per_token",
            "output_cost_per_token_batches",
            "output_cost_per_token",
        )
    ):
        # model_info was provided (e.g. deployment metadata with only id/db_model)
        # but carries no pricing fields. Fall back to the global pricing table so
        # that standard model pricing is used instead of silently returning $0.
        try:
            global_info = litellm.get_model_info(
                model=model, custom_llm_provider=custom_llm_provider
            )
            if global_info:
                model_info = global_info
        except Exception:
            pass

    if not model_info:
        return 0.0, 0.0

    input_cost_per_token_batches = model_info.get("input_cost_per_token_batches")
    input_cost_per_token = model_info.get("input_cost_per_token")
    output_cost_per_token_batches = model_info.get("output_cost_per_token_batches")
    output_cost_per_token = model_info.get("output_cost_per_token")
    total_prompt_cost = 0.0
    total_completion_cost = 0.0
    if input_cost_per_token_batches:
        total_prompt_cost = usage.prompt_tokens * input_cost_per_token_batches
    elif input_cost_per_token:
        # Subtract cached tokens from prompt_tokens before calculating cost
        # Fixes issue where cached tokens are being charged again
        total_prompt_cost = (
            get_billable_input_tokens(usage) * (input_cost_per_token) / 2
        )  # batch cost is usually half of the regular token cost

        # Add cache read cost if applicable
        details = _parse_prompt_tokens_details(usage)
        cache_read_tokens = details["cache_hit_tokens"]
        cache_read_cost_key = _get_service_tier_cost_key(
            "cache_read_input_token_cost", None
        )
        total_prompt_cost += (
            calculate_cost_component(model_info, cache_read_cost_key, cache_read_tokens)
            / 2
        )
    if output_cost_per_token_batches:
        total_completion_cost = usage.completion_tokens * output_cost_per_token_batches
    elif output_cost_per_token:
        total_completion_cost = (
            usage.completion_tokens * (output_cost_per_token) / 2
        )  # batch cost is usually half of the regular token cost

    uplift = _get_regional_uplift_multiplier(model_info, data_residency)
    if uplift != 1.0:
        total_prompt_cost *= uplift
        total_completion_cost *= uplift

    return total_prompt_cost, total_completion_cost

