
def is_offline_mode() -> bool:
    """Returns whether we are in offline mode for the Hub.

    When offline mode is enabled, all HTTP requests made with `get_session` will raise an `OfflineModeIsEnabled` exception.

    Example:
        ```py
        from huggingface_hub import is_offline_mode

        def list_files(repo_id: str):
            if is_offline_mode():
                ... # list files from local cache (degraded experience but still functional)
            else:
                ... # list files from Hub (complete experience)
        ```
    """
    return HF_HUB_OFFLINE

