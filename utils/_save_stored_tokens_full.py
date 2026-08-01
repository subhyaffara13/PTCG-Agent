
def _save_stored_tokens_full(stored_tokens: dict[str, dict[str, str]]) -> None:
    """Write all sections and their fields to the stored tokens INI file."""
    config = configparser.ConfigParser(interpolation=None)
    for token_name in sorted(stored_tokens.keys()):
        config.add_section(token_name)
        for key, value in stored_tokens[token_name].items():
            config.set(token_name, key, value)

    buf = io.StringIO()
    config.write(buf)
    _write_secret(Path(constants.HF_STORED_TOKENS_PATH), buf.getvalue())

