
def login(
    token: str | None = None,
    *,
    add_to_git_credential: bool = False,
    skip_if_logged_in: bool = True,
) -> None:
    """Login the machine to access the Hub.

    The `token` is persisted in cache and set as a git credential. Once done, the machine
    is logged in and the access token will be available across all `huggingface_hub`
    components. If `token` is not provided, a browser-based OAuth flow is used to
    authenticate: open a URL, enter a short code, and the token is retrieved and saved.
    In a terminal, you can also choose to paste an existing access token instead.

    To log in from outside of a script, one can also use `hf auth login` which is
    a cli command that wraps [`login`].

    > [!TIP]
    > When the token is not passed, [`login`] will automatically detect if the script runs
    > in a notebook or not. However, this detection might not be accurate due to the
    > variety of notebooks that exists nowadays. If that is the case, you can always force
    > the UI by using [`notebook_login`] or [`interpreter_login`].

    Args:
        token (`str`, *optional*):
            User access token to generate from https://huggingface.co/settings/token.
        add_to_git_credential (`bool`, defaults to `False`):
            If `True`, token will be set as git credential. If no git credential helper
            is configured, a warning will be displayed to the user. Only used when `token`
            is provided; ignored by the browser-based flow.
        skip_if_logged_in (`bool`, defaults to `True`):
            If `True`, do not prompt for token if user is already logged in.
            Set to `False` to force re-login. In CLI, use `--force` instead.
    Raises:
        [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError)
            If an organization token is passed. Only personal account tokens are valid
            to log in.
        [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError)
            If token is invalid.
        [`DeviceCodeError`]
            If the browser-based login fails (authorization denied, code expired, ...).
    """
    if token is not None:
        if not add_to_git_credential:
            logger.info(
                "The token has not been saved to the git credentials helper. Pass "
                "`add_to_git_credential=True` in this function directly or "
                "`--add-to-git-credential` if using via `hf`CLI if "
                "you want to set the git credential as well."
            )
        _validate_and_save_token(token, add_to_git_credential=add_to_git_credential)
        return
    if add_to_git_credential:
        logger.warning(
            "`add_to_git_credential=True` is only supported when a token is passed directly. "
            "It is ignored by the browser-based login."
        )
    if is_notebook():
        notebook_login(skip_if_logged_in=skip_if_logged_in)
    else:
        interpreter_login(skip_if_logged_in=skip_if_logged_in)


def login(ctx: click.Context):
    """Login to LiteLLM proxy using SSO authentication"""
    from litellm.constants import LITELLM_CLI_SOURCE_IDENTIFIER
    from litellm.proxy.client.cli.interface import show_commands

    base_url = ctx.obj["base_url"]

    try:
        cli_sso_flow = _start_cli_sso_flow(base_url=base_url)
        key_id = cli_sso_flow["login_id"]
        poll_secret = cli_sso_flow["poll_secret"]
        user_code = cli_sso_flow["user_code"]

        sso_url = f"{base_url}/sso/key/generate?" + urlencode(
            {"source": LITELLM_CLI_SOURCE_IDENTIFIER, "key": key_id}
        )

        click.echo(f"Opening browser to: {sso_url}")
        click.echo("Please complete the SSO authentication in your browser...")
        click.echo(f"Verification code: {user_code}")
        click.echo(f"Session ID: {key_id}")

        # Open browser
        webbrowser.open(sso_url)

        # Poll for authentication completion
        click.echo("Waiting for authentication...")

        auth_result = _poll_for_authentication(
            base_url=base_url, key_id=key_id, poll_secret=poll_secret
        )

        if auth_result:
            api_key = auth_result["api_key"]
            user_id = auth_result["user_id"]

            # Save token data. base_url is stored so we can verify origin
            # before reusing the key on a subsequent CLI invocation.
            save_token(
                {
                    "base_url": base_url.rstrip("/"),
                    "key": api_key,
                    "user_id": user_id or "cli-user",
                    "user_email": "unknown",
                    "user_role": "cli",
                    "auth_header_name": "Authorization",
                    "jwt_token": "",
                    "timestamp": time.time(),
                }
            )

            click.echo("\n✅ Login successful!")
            click.echo(f"JWT Token: {api_key[:20]}...")
            click.echo("You can now use the CLI without specifying --api-key")

            # Show available commands after successful login
            click.echo("\n" + "=" * 60)
            show_commands()
            return
        else:
            click.echo("❌ Authentication timed out. Please try again.")
            return

    except KeyboardInterrupt:
        click.echo("\n❌ Authentication cancelled by user.")
        return
    except Exception as e:
        click.echo(f"❌ Authentication failed: {e}")
        return

