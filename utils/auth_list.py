
def auth_list() -> None:
    """List all stored access tokens."""
    # Resolve the current token before reading the file: `get_token()` may refresh an OAuth
    # token and rewrite the stored tokens on the way.
    current_token = get_token()
    stored_tokens = _read_stored_tokens_full()

    if not stored_tokens:
        if _get_token_from_environment():
            logger.info("No stored access tokens found.")
            logger.warning("Note: Environment variable `HF_TOKEN` is set and is the current active token.")
        else:
            logger.info("No access tokens found.")
        return
    show_expires = any("expires_at" in fields for fields in stored_tokens.values())
    headers = [" ", "name", "token"] + (["expires"] if show_expires else [])

    current_token_name = None
    rows: list[list[str | int]] = []
    for token_name, fields in stored_tokens.items():
        token = fields.get("hf_token", "<not set>")
        if token == current_token:
            current_token_name = token_name
        masked_token = f"{token[:3]}****{token[-4:]}" if token != "<not set>" else token
        row: list[str | int] = ["*" if token == current_token else "", token_name, masked_token]
        if show_expires:
            row.append(_format_expiration(fields.get("expires_at")))
        rows.append(row)
    print(tabulate(rows, headers=headers))

    if _get_token_from_environment():
        logger.warning(
            "\nNote: Environment variable `HF_TOKEN` is set and is the current active token independently from the stored tokens listed above."
        )
    elif current_token_name is None:
        logger.warning(
            "\nNote: No active token is set and no environment variable `HF_TOKEN` is found. Use `hf auth login` to log in."
        )

