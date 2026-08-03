import os

def _resolve_oidc_file_path(requested_path: str) -> str:
    """
    Resolve ``requested_path`` and verify it falls within one of the allowed
    credential directories. Raises ``ValueError`` otherwise.
    """
    if not os.path.isabs(requested_path):
        raise ValueError(
            "oidc/file path must be absolute. Use the format "
            "'oidc/file//var/run/secrets/<name>' (note the leading slash "
            "after 'oidc/file/')."
        )
    resolved = os.path.realpath(requested_path)
    for allowed in _get_oidc_allowed_credential_dirs():
        try:
            if os.path.commonpath([resolved, allowed]) == allowed:
                return resolved
        except ValueError:
            # commonpath raises when paths are on different drives (Windows);
            # treat as not-matching and continue.
            continue
    raise ValueError(
        "oidc/file path is outside the allowed credential directories. "
        "Set LITELLM_OIDC_ALLOWED_CREDENTIAL_DIRS to extend the allowlist."
    )

