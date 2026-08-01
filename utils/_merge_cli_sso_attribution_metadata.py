
def _merge_cli_sso_attribution_metadata(
    existing_metadata: Dict[str, Any], attribution_metadata: Dict[str, Any]
) -> Dict[str, Any]:
    """Merge attribution metadata into existing user metadata in-place.

    Preserves original value types (in particular, string claim values that
    happen to look numeric are NOT coerced to ``int``/``float``). Nested dicts
    are merged iteratively so attribution claims do not clobber unrelated keys
    under the same parent.
    """
    pending: List[Tuple[Dict[str, Any], Dict[str, Any]]] = [
        (existing_metadata, attribution_metadata)
    ]
    while pending:
        target, source = pending.pop()
        for key, value in source.items():
            if value is None:
                continue
            existing_value = target.get(key)
            if isinstance(value, dict) and isinstance(existing_value, dict):
                pending.append((existing_value, value))
            else:
                target[key] = value
    return existing_metadata

