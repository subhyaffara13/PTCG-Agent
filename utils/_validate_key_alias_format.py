from typing import Optional

def _validate_key_alias_format(key_alias: Optional[str]) -> None:
    """
    Validate the format of the key_alias.

    Gated behind ``litellm.enable_key_alias_format_validation`` (default **False**).
    When disabled, no validation is performed so existing workflows are not broken.

    Rules (when enabled):
    - None is OK (no alias).
    - Otherwise must be 2–255 chars
    - start/end with alphanumeric
    - only allow a-zA-Z0-9_-/.@
    """
    if not litellm.enable_key_alias_format_validation:
        return

    if key_alias is None:
        return

    if not _KEY_ALIAS_PATTERN.match(key_alias):
        raise ProxyException(
            message="Invalid key_alias format. Must be 2-255 characters, start/end with alphanumeric, and only contain a-zA-Z0-9_-/.@.",
            type=ProxyErrorTypes.bad_request_error,
            param="key_alias",
            code=400,
        )

