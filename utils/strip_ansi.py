
def strip_ansi(value: str) -> str:
    return _ansi_re.sub("", value)

