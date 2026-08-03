import os

def _get_oidc_allowed_credential_dirs() -> list[str]:
    """
    Return the absolute, normalized list of directories from which
    ``oidc/file/`` is permitted to read token files.

    Defaults to standard container credential mount points. Operators can
    override via the ``LITELLM_OIDC_ALLOWED_CREDENTIAL_DIRS`` environment
    variable (comma-separated list of absolute paths).
    """
    override = os.getenv("LITELLM_OIDC_ALLOWED_CREDENTIAL_DIRS")
    raw_dirs = (
        [d.strip() for d in override.split(",") if d.strip()]
        if override
        else list(_DEFAULT_OIDC_ALLOWED_CREDENTIAL_DIRS)
    )
    return [os.path.realpath(d) for d in raw_dirs]

