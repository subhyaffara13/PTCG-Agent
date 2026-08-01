
def _replace_escaping(s: str) -> str:
    return ESCAPING_RE.sub(replace_escape_sequence, s)


def _replace_escaping(s):
    return ESCAPING_RE.sub(_replace_escape_sequence, s)

