
def _is_safe_cli_sso_metadata_dest_key(dest_key: str) -> bool:
    if not dest_key or not _CLI_SSO_DEST_KEY_RE.fullmatch(dest_key):
        return False
    lowered = dest_key.lower()
    return not any(fragment in lowered for fragment in _CLI_SSO_SECRET_KEY_FRAGMENTS)

