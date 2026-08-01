
def _replace_help_escaping(s: str) -> str:
    return HELP_ESCAPING_RE.sub(replace_escape_sequence, s)

