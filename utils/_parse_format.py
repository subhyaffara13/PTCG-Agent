
def _parse_format(format_value):
    """Parses a ``--format`` value modeled after gcloud.

    Returns a tuple ``(format_name, fields)`` where ``fields`` is a list of
    selected field names (empty when no projection was provided). Examples:

    >>> _parse_format("json")
    ('json', [])
    >>> _parse_format("json(current_version_number)")
    ('json', ['current_version_number'])
    >>> _parse_format("json(status, current_version_number)")
    ('json', ['status', 'current_version_number'])
    """
    if format_value is None:
        return None, []
    value = format_value.strip()
    paren = value.find("(")
    if paren == -1:
        return value, []
    if not value.endswith(")"):
        raise ValueError(f"Malformed --format value: {format_value!r}")
    name = value[:paren].strip()
    inner = value[paren + 1 : -1]
    fields = [f.strip() for f in inner.split(",") if f.strip()]
    return name, fields

