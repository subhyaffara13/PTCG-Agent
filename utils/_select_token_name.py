
def _select_token_name() -> str | None:
    token_names = list(get_stored_tokens().keys())

    if not token_names:
        logger.error("No stored tokens found. Please login first.")
        return None

    if out.mode != OutputFormat.human:
        raise CLIError("Use --token-name to select a token in non-interactive mode.")
    return token_names[select_choice("Select a token to switch to:", token_names)]

