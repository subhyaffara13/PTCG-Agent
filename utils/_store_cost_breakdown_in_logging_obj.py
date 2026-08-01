
def _store_cost_breakdown_in_logging_obj(
    litellm_logging_obj: Optional[LitellmLoggingObject],
    prompt_tokens_cost_usd_dollar: float,
    completion_tokens_cost_usd_dollar: float,
    cost_for_built_in_tools_cost_usd_dollar: float,
    total_cost_usd_dollar: float,
    additional_costs: Optional[dict] = None,
    original_cost: Optional[float] = None,
    discount_percent: Optional[float] = None,
    discount_amount: Optional[float] = None,
    margin_percent: Optional[float] = None,
    margin_fixed_amount: Optional[float] = None,
    margin_total_amount: Optional[float] = None,
    cache_read_cost: Optional[float] = None,
    cache_creation_cost: Optional[float] = None,
) -> None:
    """
    Helper function to store cost breakdown in the logging object.

    Args:
        litellm_logging_obj: The logging object to store breakdown in
        prompt_tokens_cost_usd_dollar: Cost of input tokens
        completion_tokens_cost_usd_dollar: Cost of completion tokens (includes reasoning if applicable)
        cost_for_built_in_tools_cost_usd_dollar: Cost of built-in tools
        total_cost_usd_dollar: Total cost of request
        additional_costs: Free-form additional costs dict (e.g., {"azure_model_router_flat_cost": 0.00014})
        original_cost: Cost before discount
        discount_percent: Discount percentage applied (0.05 = 5%)
        discount_amount: Discount amount in USD
        margin_percent: Margin percentage applied (0.10 = 10%)
        margin_fixed_amount: Fixed margin amount in USD
        margin_total_amount: Total margin added in USD
    """
    if litellm_logging_obj is None:
        return

    try:
        # Store the cost breakdown
        litellm_logging_obj.set_cost_breakdown(
            input_cost=prompt_tokens_cost_usd_dollar,
            output_cost=completion_tokens_cost_usd_dollar,
            total_cost=total_cost_usd_dollar,
            cost_for_built_in_tools_cost_usd_dollar=cost_for_built_in_tools_cost_usd_dollar,
            additional_costs=additional_costs,
            original_cost=original_cost,
            discount_percent=discount_percent,
            discount_amount=discount_amount,
            margin_percent=margin_percent,
            margin_fixed_amount=margin_fixed_amount,
            margin_total_amount=margin_total_amount,
            cache_read_cost=cache_read_cost,
            cache_creation_cost=cache_creation_cost,
        )

    except Exception as breakdown_error:
        verbose_logger.debug(f"Error storing cost breakdown: {str(breakdown_error)}")
        # Don't fail the main cost calculation if breakdown storage fails
        pass

