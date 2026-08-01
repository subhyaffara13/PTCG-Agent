
def _is_valid_hostchar(ch: str) -> bool:
    """Return ``True`` if *ch* is valid inside a domain label (not whitespace/punctuation)."""
    if ch.isspace():
        return False
    cat = unicodedata.category(ch)
    # Unicode punctuation categories: Pc, Pd, Pe, Pf, Pi, Po, Ps
    return not cat.startswith("P")

