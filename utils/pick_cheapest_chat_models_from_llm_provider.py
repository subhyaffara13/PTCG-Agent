
def pick_cheapest_chat_models_from_llm_provider(custom_llm_provider: str, n=1):
    """
    Pick the n cheapest chat models from the LLM provider.

    Args:
        custom_llm_provider (str): The name of the LLM provider.
        n (int): The number of cheapest models to return.

    Returns:
        list[str]: A list of the n cheapest chat models.
    """
    if custom_llm_provider not in litellm.models_by_provider:
        return []

    known_models = litellm.models_by_provider.get(custom_llm_provider, [])
    model_costs = []

    for model in known_models:
        try:
            model_info = litellm.get_model_info(
                model=model, custom_llm_provider=custom_llm_provider
            )
        except Exception:
            continue
        if model_info.get("mode") != "chat":
            continue
        _cost = (model_info.get("input_cost_per_token") or 0.0) + (
            model_info.get("output_cost_per_token") or 0.0
        )
        model_costs.append((model, _cost))

    # Sort by cost (ascending)
    model_costs.sort(key=lambda x: x[1])

    # Return the top n cheapest models
    return [model for model, _ in model_costs[:n]]

