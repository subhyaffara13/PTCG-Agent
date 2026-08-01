
def _logout_from_token(token_name: str) -> None:
    """Logout from a specific access token.

    Args:
        token_name (`str`):
            The name of the access token to logout from.
    """
    stored_tokens = _read_stored_tokens_full()
    # If there is no access tokens saved or the access token name is not found, do nothing
    if token_name not in stored_tokens:
        return

    fields = stored_tokens.pop(token_name)
    _save_stored_tokens_full(stored_tokens)

    if fields.get("hf_token") == _get_token_from_file():
        logger.warning(f"Active token '{token_name}' has been deleted.")
        Path(constants.HF_TOKEN_PATH).unlink(missing_ok=True)

