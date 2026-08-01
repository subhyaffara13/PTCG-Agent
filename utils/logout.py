
def logout(token_name: str | None = None) -> None:
    """Logout the machine from the Hub.

    Token is deleted from the machine and removed from git credential.

    Args:
        token_name (`str`, *optional*):
            Name of the access token to logout from. If `None`, will log out from all saved access tokens.
    Raises:
        [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError):
            If the access token name is not found.
    """
    if get_token() is None and not get_stored_tokens():  # No active token and no saved access tokens
        logger.warning("Not logged in!")
        return
    if not token_name:
        # Delete all saved access tokens and token
        for file_path in (constants.HF_TOKEN_PATH, constants.HF_STORED_TOKENS_PATH):
            try:
                Path(file_path).unlink()
            except FileNotFoundError:
                pass
        logger.info("Successfully logged out from all access tokens.")
    else:
        _logout_from_token(token_name)
        logger.info(f"Successfully logged out from access token: {token_name}.")

    unset_git_credential()

    # Check if still logged in
    if _get_token_from_google_colab() is not None:
        raise OSError(
            "You are automatically logged in using a Google Colab secret.\n"
            "To log out, you must unset the `HF_TOKEN` secret in your Colab settings."
        )
    if _get_token_from_environment() is not None:
        raise OSError(
            "Token has been deleted from your machine but you are still logged in.\n"
            "To log out, you must clear out both `HF_TOKEN` and `HUGGING_FACE_HUB_TOKEN` environment variables."
        )


def logout():
    """Logout and clear stored authentication"""
    clear_token()
    click.echo("✅ Logged out successfully. Authentication token cleared.")

