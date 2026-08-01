
def _mask_sensitive_fields(
    data: Dict[str, Any], sensitive_fields: Set[str]
) -> Dict[str, Any]:
    """Mask sensitive fields for API responses. Non-sensitive fields are left as-is."""
    masked = {}
    for key, value in data.items():
        if value is not None and key in sensitive_fields and isinstance(value, str):
            masked[key] = _sensitive_masker._mask_value(value)
        else:
            masked[key] = value
    return masked

