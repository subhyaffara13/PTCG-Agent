
def _get_cli_sso_poll_headers(poll_secret: str) -> Dict[str, str]:
    return {"x-litellm-cli-poll-secret": poll_secret}

