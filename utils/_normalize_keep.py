
def _normalize_keep(keep_obj: Mapping[str, Any]) -> dict[str, Any]:
    """Map keep-dict keys to canonical lowercase item keys.

    Later occurrences win on alias collision (e.g. both ``Book`` and ``book``
    present) so the model's last-written value applies.
    """
    out: dict[str, Any] = {}
    for k, v in keep_obj.items():
        canonical = _ITEM_KEY_ALIASES.get(str(k).strip().lower())
        if canonical is not None:
            out[canonical] = v
    return out

