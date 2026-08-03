from pathlib import Path


def _read_stored_tokens_full() -> dict[str, dict[str, str]]:
    """Read all sections of the stored tokens INI file, with all their fields.

    Beside `hf_token`, sections for OAuth tokens also carry `refresh_token` and `expires_at`
    (unix timestamp), used by [`get_token`] to transparently refresh them.
    """
    tokens_path = Path(constants.HF_STORED_TOKENS_PATH)
    if not tokens_path.exists():
        return {}
    # interpolation=None: token values are opaque strings, a `%` must not be interpreted.
    config = configparser.ConfigParser(interpolation=None)
    try:
        config.read(tokens_path)
        return {token_name: dict(config.items(token_name)) for token_name in config.sections()}
    except configparser.Error as e:
        logger.error(f"Error parsing stored tokens file: {e}")
        return {}

