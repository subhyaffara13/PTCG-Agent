
def get_stored_tokens() -> dict[str, str]:
    """
    Returns the parsed INI file containing the access tokens.
    The file is located at `HF_STORED_TOKENS_PATH`, defaulting to `~/.cache/huggingface/stored_tokens`.
    If the file does not exist, an empty dictionary is returned.

    Returns: `dict[str, str]`
        Key is the token name and value is the token.
    """
    return {token_name: fields.get("hf_token", "") for token_name, fields in _read_stored_tokens_full().items()}

