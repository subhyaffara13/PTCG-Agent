
def get_fine_tuning_provider_config(
    custom_llm_provider: str,
):
    global fine_tuning_config
    if fine_tuning_config is None:
        raise ValueError(
            "fine_tuning_config is not set, set it on your config.yaml file."
        )
    for setting in fine_tuning_config:
        if setting.get("custom_llm_provider") == custom_llm_provider:
            return setting
    return None

