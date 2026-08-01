
def mask_sensitive_keys(
    data: Dict[str, Any], sensitive_fields: Set[str]
) -> Dict[str, Any]:
    """Return a new dict with values masked for keys listed in ``sensitive_fields``.

    Unlike :meth:`SensitiveDataMasker.mask_dict`, this does exact key-name
    matching (not segment matching), so callers explicitly enumerate which
    fields to mask. Non-string and None values are passed through unchanged.

    Values shorter than ``visible_prefix + visible_suffix`` (8 by default)
    fall outside :meth:`SensitiveDataMasker._mask_value`'s partial-reveal
    range and are replaced with a fixed-length all-mask string, so a short
    credential is never returned verbatim.
    """
    masked: Dict[str, Any] = {}
    mask_char = _default_masker.mask_char
    min_visible = _default_masker.visible_prefix + _default_masker.visible_suffix
    for key, value in data.items():
        if value is not None and key in sensitive_fields and isinstance(value, str):
            if len(value) < min_visible:
                masked[key] = mask_char * len(value) if value else value
            else:
                masked[key] = _default_masker._mask_value(value)
        else:
            masked[key] = value
    return masked

