
def _should_store_prompts_and_responses_in_spend_logs() -> bool:
    from litellm.proxy.proxy_server import general_settings
    from litellm.secret_managers.main import get_secret_bool

    # Check general_settings (from DB or proxy_config.yaml)
    store_prompts_value = general_settings.get("store_prompts_in_spend_logs")

    # Normalize case: handle True/true/TRUE, False/false/FALSE, None/null
    if store_prompts_value is True:
        return True
    elif isinstance(store_prompts_value, str):
        # Case-insensitive string comparison
        if store_prompts_value.lower() == "true":
            return True

    # Also check environment variable
    return get_secret_bool("STORE_PROMPTS_IN_SPEND_LOGS") is True

