from pathlib import Path


def _set_active_token(
    token_name: str,
    add_to_git_credential: bool,
) -> None:
    """Set the active access token.

    Args:
        token_name (`str`):
            The name of the token to set as active.
    """
    token = _get_token_by_name(token_name)
    if not token:
        raise ValueError(f"Token {token_name} not found in {constants.HF_STORED_TOKENS_PATH}")
    if add_to_git_credential:
        if _is_git_credential_helper_configured():
            set_git_credential(token)
            logger.info(
                "Your token has been saved in your configured git credential helpers"
                + f" ({','.join(list_credential_helpers())})."
            )
        else:
            logger.warning("Token has not been saved to git credential helper.")
    # Write token to HF_TOKEN_PATH
    _write_secret(Path(constants.HF_TOKEN_PATH), token)
    logger.info(f"Your token has been saved to {constants.HF_TOKEN_PATH}")

