
def escape_label_name(s: str, escaping: str = UNDERSCORES) -> str:
    """Escapes the label name and puts it in quotes iff the name does not
    conform to the legacy Prometheus character set.
    """
    if len(s) == 0:
        return s
    if escaping == ALLOWUTF8:
        if not _is_valid_legacy_labelname(s):
            return '"{}"'.format(_escape(s, escaping, _is_legacy_labelname_rune))
        return _escape(s, escaping, _is_legacy_labelname_rune)
    elif escaping == UNDERSCORES:
        if _is_valid_legacy_labelname(s):
            return s
        return _escape(s, escaping, _is_legacy_labelname_rune)
    elif escaping == DOTS:
        return _escape(s, escaping, _is_legacy_labelname_rune)
    elif escaping == VALUES:
        if _is_valid_legacy_labelname(s):
            return s
        return _escape(s, escaping, _is_legacy_labelname_rune)
    return s

