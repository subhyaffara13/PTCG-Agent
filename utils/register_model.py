
def register_model(model_cost: Union[str, dict]):
    """
    Register new / Override existing models (and their pricing) to specific providers.
    Provide EITHER a model cost dictionary or a url to a hosted json blob
    Example usage:
    model_cost_dict = {
        "gpt-4": {
            "max_tokens": 8192,
            "input_cost_per_token": 0.00003,
            "output_cost_per_token": 0.00006,
            "litellm_provider": "openai",
            "mode": "chat"
        },
    }
    """

    loaded_model_cost = {}
    if isinstance(model_cost, dict):
        # Convert stringified numbers to appropriate numeric types
        loaded_model_cost = model_cost
    elif isinstance(model_cost, str):
        loaded_model_cost = litellm.get_model_cost_map(url=model_cost)

    # Providers that trigger side effects (e.g., OAuth flows) when get_model_info is called
    # Skip get_model_info for these providers during model registration
    _skip_get_model_info_providers = {
        LlmProviders.GITHUB_COPILOT.value,
        LlmProviders.CHATGPT.value,
    }

    for key, value in loaded_model_cost.items():
        ## get model info ##
        provider = value.get("litellm_provider", "")
        _key_str = str(key)
        if provider in _skip_get_model_info_providers or any(
            _key_str.startswith(f"{p}/") for p in _skip_get_model_info_providers
        ):
            existing_model = litellm.model_cost.get(key, {})
            model_cost_key = key
        else:
            try:
                existing_model = cast(dict, get_model_info(model=key))
                model_cost_key = existing_model["key"]
            except Exception:
                existing_model = {}
                model_cost_key = key
                builtin_entry = _resolve_builtin_model_cost_entry(
                    key=_key_str, provider=provider
                )
                if builtin_entry is not None:
                    for field in _CACHE_PRICING_FIELDS:
                        if (
                            value.get(field) is None
                            and builtin_entry.get(field) is not None
                        ):
                            existing_model[field] = builtin_entry[field]
                elif (
                    value.get("cache_creation_input_token_cost") is None
                    and value.get("cache_read_input_token_cost") is None
                ):
                    verbose_logger.warning(
                        f"register_model: model={key} not in built-in cost map and no "
                        "prefix/region variant matched; cache cost fields will default "
                        "to 0. To track cache cost, add cache_creation_input_token_cost "
                        "and cache_read_input_token_cost to model_info"
                    )
        # ``get_model_info`` returns ``litellm_provider: None`` when the
        # provider is unknown (e.g. custom deployments registered via
        # ``Router.add_deployment``). Persisting that None into
        # ``litellm.model_cost`` causes ``_check_provider_match`` to drop
        # custom pricing on subsequent cost lookups.
        if existing_model.get("litellm_provider") is None:
            existing_model.pop("litellm_provider", None)
        # Same pattern for cost fields (#30198): ``_get_model_info_helper``
        # synthesizes ``input_cost_per_token`` / ``output_cost_per_token``
        # = 0 when they are absent from the raw entry. Writing those zeros
        # back flips a sparse entry from "no cost keys" (priced via name)
        # to "cost keys = 0" (free), which makes
        # ``_is_cost_explicitly_configured`` return True and silently
        # disables budget enforcement on the next re-registration.
        _raw_entry = litellm.model_cost.get(model_cost_key)
        if _raw_entry is None:
            _raw_entry = litellm.model_cost.get(key)
        if _raw_entry is None:
            _raw_entry = {}
        for _cost_field in ("input_cost_per_token", "output_cost_per_token"):
            if _cost_field not in _raw_entry and _cost_field not in value:
                existing_model.pop(_cost_field, None)
        ## override / add new keys to the existing model cost dictionary
        updated_dictionary = _update_dictionary(existing_model, value)
        litellm.model_cost.setdefault(model_cost_key, {}).update(updated_dictionary)

        # Invalidate case-insensitive lookup map since model_cost was modified
        _invalidate_model_cost_lowercase_map()

        verbose_logger.debug(
            f"added/updated model={model_cost_key} in litellm.model_cost: {model_cost_key}"
        )
        # add new model names to provider lists
        if value.get("litellm_provider") == "openai":
            if key not in litellm.open_ai_chat_completion_models:
                litellm.open_ai_chat_completion_models.add(key)
        elif value.get("litellm_provider") == "text-completion-openai":
            if key not in litellm.open_ai_text_completion_models:
                litellm.open_ai_text_completion_models.add(key)
        elif value.get("litellm_provider") == "cohere":
            if key not in litellm.cohere_models:
                litellm.cohere_models.add(key)
        elif value.get("litellm_provider") == "anthropic":
            if key not in litellm.anthropic_models:
                litellm.anthropic_models.add(key)
        elif value.get("litellm_provider") == "openrouter":
            split_string = key.split("/", 1)
            if split_string[-1] not in litellm.openrouter_models:
                litellm.openrouter_models.add(split_string[-1])
        elif value.get("litellm_provider") == "vercel_ai_gateway":
            if key not in litellm.vercel_ai_gateway_models:
                litellm.vercel_ai_gateway_models.add(key)
        elif value.get("litellm_provider") == "vertex_ai-text-models":
            if key not in litellm.vertex_text_models:
                litellm.vertex_text_models.add(key)
        elif value.get("litellm_provider") == "vertex_ai-code-text-models":
            if key not in litellm.vertex_code_text_models:
                litellm.vertex_code_text_models.add(key)
        elif value.get("litellm_provider") == "vertex_ai-chat-models":
            if key not in litellm.vertex_chat_models:
                litellm.vertex_chat_models.add(key)
        elif value.get("litellm_provider") == "vertex_ai-code-chat-models":
            if key not in litellm.vertex_code_chat_models:
                litellm.vertex_code_chat_models.add(key)
        elif value.get("litellm_provider") == "ai21":
            if key not in litellm.ai21_models:
                litellm.ai21_models.add(key)
        elif value.get("litellm_provider") == "nlp_cloud":
            if key not in litellm.nlp_cloud_models:
                litellm.nlp_cloud_models.add(key)
        elif value.get("litellm_provider") == "aleph_alpha":
            if key not in litellm.aleph_alpha_models:
                litellm.aleph_alpha_models.add(key)
        elif value.get("litellm_provider") == "bedrock":
            if key not in litellm.bedrock_models:
                litellm.bedrock_models.add(key)
        elif value.get("litellm_provider") == "novita":
            if key not in litellm.novita_models:
                litellm.novita_models.add(key)
    return model_cost

