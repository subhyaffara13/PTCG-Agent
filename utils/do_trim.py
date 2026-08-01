
def do_trim(value: str, chars: t.Optional[str] = None) -> str:
    """Strip leading and trailing characters, by default whitespace."""
    return soft_str(value).strip(chars)

