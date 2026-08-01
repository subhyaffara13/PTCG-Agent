
def _should_read_secret_from_secret_manager() -> bool:
    """
    Returns True if the secret manager should be used to read the secret, False otherwise

    - If the secret manager client is not set, return False
    - If the `_key_management_settings` access mode is "read_only" or "read_and_write", return True
    - Otherwise, return False
    """
    if litellm.secret_manager_client is not None:
        if litellm._key_management_settings is not None:
            if (
                litellm._key_management_settings.access_mode == "read_only"
                or litellm._key_management_settings.access_mode == "read_and_write"
            ):
                return True
    return False

