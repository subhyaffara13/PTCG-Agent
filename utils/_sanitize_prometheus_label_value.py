
def _sanitize_prometheus_label_value(value: Optional[Any]) -> Optional[str]:
    """
    Same semantics as :func:`_sanitize_prometheus_label_value`, implemented with
    ``str.translate`` plus a single escape pass instead of chained ``replace``.
    """
    if value is None:
        return None

    str_value: str = value if isinstance(value, str) else str(value)

    cleaned = str_value.translate(_PROMETHEUS_LABEL_VALUE_TRANSLATE_V1)
    if "\\" not in cleaned and '"' not in cleaned:
        return cleaned

    parts: List[str] = []
    append = parts.append
    for ch in cleaned:
        if ch == "\\":
            append("\\\\")
        elif ch == '"':
            append('\\"')
        else:
            append(ch)
    return "".join(parts)

