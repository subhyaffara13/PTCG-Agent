
def escape_metric_name(s: str, escaping: str = UNDERSCORES) -> str:
    """Escapes the metric name and puts it in quotes iff the name does not
    conform to the legacy Prometheus character set.
    """
    if len(s) == 0:
        return s
    if escaping == ALLOWUTF8:
        if not _is_valid_legacy_metric_name(s):
            return '"{}"'.format(_escape(s, escaping, _is_legacy_metric_rune))
        return _escape(s, escaping, _is_legacy_metric_rune)
    elif escaping == UNDERSCORES:
        if _is_valid_legacy_metric_name(s):
            return s
        return _escape(s, escaping, _is_legacy_metric_rune)
    elif escaping == DOTS:
        return _escape(s, escaping, _is_legacy_metric_rune)
    elif escaping == VALUES:
        if _is_valid_legacy_metric_name(s):
            return s
        return _escape(s, escaping, _is_legacy_metric_rune)
    return s

