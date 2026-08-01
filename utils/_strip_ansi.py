
def _strip_ansi(s: str) -> str:
    return _ansi_re.sub("", str(s))


def _strip_ansi(s: str) -> str:
    return _ANSI_RE.sub("", s)


def _strip_ansi(text: str) -> str:
    return _ANSI_RE.sub("", text)

