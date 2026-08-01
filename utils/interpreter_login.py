
def interpreter_login(*, skip_if_logged_in: bool = True) -> None:
    """
    Displays a prompt to log in to the HF website and store the token.

    This is equivalent to [`login`] without passing a token when not run in a notebook.
    [`interpreter_login`] is useful if you want to force the use of the terminal prompt
    instead of a notebook flow.

    For more details, see [`login`].

    Args:
        skip_if_logged_in (`bool`, defaults to `True`):
            If `True`, do not prompt for token if user is already logged in.
            Set to `False` to force re-login. In CLI, use `--force` instead.
    """
    if skip_if_logged_in and get_token() is not None:
        logger.info("User is already logged in. Use `hf auth login --force` to force re-login.")
        return

    if get_token() is not None:
        logger.info("Note: a token is already saved on this machine. Logging in again will replace the active token.")

    if _prompt_login_method() == "token":
        _paste_token_login()
    else:
        _device_code_login()

