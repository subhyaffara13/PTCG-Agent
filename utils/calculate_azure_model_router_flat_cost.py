
def calculate_azure_model_router_flat_cost(model: str, prompt_tokens: int) -> float:
    """
    Calculate the flat cost for Azure AI Foundry Model Router.

    Args:
        model: The model name (should be a model router model)
        prompt_tokens: Number of prompt tokens

    Returns:
        float: The flat cost in USD, or 0.0 if not applicable
    """
    if not _is_azure_model_router(model):
        return 0.0

    # Get the model router pricing from model_prices_and_context_window.json
    # Use "model_router" as the key (without actual model name suffix)
    model_info = get_model_info(model="model_router", custom_llm_provider="azure_ai")
    router_flat_cost_per_token = model_info.get("input_cost_per_token", 0)

    if router_flat_cost_per_token and router_flat_cost_per_token > 0:
        return prompt_tokens * router_flat_cost_per_token

    return 0.0

