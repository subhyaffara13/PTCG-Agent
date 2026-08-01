
def auth_login(
    token: TokenOpt = None,
    add_to_git_credential: Annotated[
        bool,
        typer.Option(
            help="Save to git credential helper. Useful only if you plan to run git commands directly.",
        ),
    ] = False,
    force: Annotated[
        bool,
        typer.Option(
            help="Force re-login even if already logged in.",
        ),
    ] = False,
) -> None:
    """Login from your browser, or using a token from huggingface.co/settings/tokens."""
    if token is not None or out.mode == OutputFormat.human:
        # `--token` bypasses any prompt; in human mode the gh-style menu lives in `login()`.
        login(token=token, add_to_git_credential=add_to_git_credential, skip_if_logged_in=not force)
        return

    # Logging in is an interactive flow: besides human mode, only agent mode is supported.
    if out.mode != OutputFormat.agent:
        raise CLIError(
            "`hf auth login` is interactive and does not support --format json/quiet. "
            "Pass --token for a non-interactive login."
        )

    # agent mode: never prompt; print instructions the agent can relay to its user.
    if not force and get_token() is not None:
        out.text(agent="Already logged in. Use `hf auth login --force` to re-login.")
        return
    device_info = request_device_code()
    out.text(
        agent=(
            f"Ask the user to open {device_info['verification_uri_complete']} in a browser and enter the code "
            f"{device_info['user_code']}. The code expires in {device_info['expires_in']} seconds. "
            "Waiting for authorization..."
        )
    )
    response = poll_device_token(device_info)
    token_name, username = _save_oauth_token(response)
    out.text(agent=f"Login successful: logged in as {username} (token saved as '{token_name}').")

