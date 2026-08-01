
def notebook_login(*, skip_if_logged_in: bool = True) -> None:
    """
    Displays a prompt to log in to the HF website and store the token.

    This is equivalent to [`login`] without passing a token when run in a notebook.
    [`notebook_login`] is useful if you want to force the use of the notebook flow
    instead of a prompt in the terminal.

    For more details, see [`login`].

    Args:
        skip_if_logged_in (`bool`, defaults to `True`):
            If `True`, do not prompt for token if user is already logged in.
            Set to `False` to force re-login. In CLI, use `--force` instead.
    """
    if skip_if_logged_in and get_token() is not None:
        logger.info("User is already logged in. Use `hf auth login --force` to force re-login.")
        return

    try:
        from IPython.display import HTML, display  # type: ignore
    except ImportError:
        # Not in a notebook environment: fall back to the terminal flow
        interpreter_login(skip_if_logged_in=False)
        return

    device_info = request_device_code()
    # Escape server-provided values: they end up in raw notebook HTML.
    verification_uri = html.escape(device_info["verification_uri"])
    verification_uri_complete = html.escape(device_info["verification_uri_complete"])

    display(
        HTML(
            '<center><img src="https://huggingface.co/front/assets/huggingface_logo-noborder.svg"'
            ' width="100" alt="Hugging Face"><br><br>'
            "<p>To log in, open this URL and enter the code:</p>"
            f'<p><a href="{verification_uri_complete}" target="_blank"><b>{verification_uri}</b></a></p>'
            '<p style="font-size: 1.6em; letter-spacing: 0.3em; font-family: monospace;">'
            f"<b>{html.escape(device_info['user_code'])}</b></p></center>"
        )
    )
    display(HTML("<center><i>Waiting for authorization...</i></center>"))
    try:
        response = poll_device_token(device_info)
    except DeviceCodeError as e:
        display(HTML(f"<center><b style='color: red;'>Login failed: {html.escape(str(e))}</b></center>"))
        return

    try:
        token_name, username = _save_oauth_token(response)
    except Exception as error:
        display(HTML(f"<center><b style='color: red;'>{html.escape(str(error))}</b></center>"))
        return

    message = f"Login successful. Logged in as <b>{html.escape(username)}</b> (token: <code>{html.escape(token_name)}</code>)."
    if note := _expiration_note(response):
        message += f"<br>{html.escape(note)}"
    display(HTML(f"<center>{message}</center>"))

