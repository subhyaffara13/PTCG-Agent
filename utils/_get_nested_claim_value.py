
def _get_nested_claim_value(data: Dict[str, Any], claim_path: str) -> Any:
    """Resolve a dot-notation claim path against an SSO result dict.

    Unlike ``get_nested_value``, this does not strip a leading ``metadata.``
    prefix, since OIDC claims may legitimately use ``metadata`` as a top-level
    key.
    """
    if not claim_path:
        return None
    if claim_path in data:
        return data[claim_path]
    placeholder = "\x00"
    parts = claim_path.replace("\\.", placeholder).split(".")
    parts = [p.replace(placeholder, ".") for p in parts]
    current: Any = data
    for part in parts:
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            return None
    return current

