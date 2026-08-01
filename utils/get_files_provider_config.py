
def get_files_provider_config(
    custom_llm_provider: str,
):
    global files_config
    if custom_llm_provider == "vertex_ai":
        return None
    if files_config is None:
        raise ValueError("files_settings is not set, set it on your config.yaml file.")
    for setting in files_config:
        if setting.get("custom_llm_provider") == custom_llm_provider:
            return setting
    return None

