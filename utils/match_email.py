
def match_email(text: str) -> tuple[str, int] | None:
    """Match an email address (optionally prefixed by ``mailto:``/``xmpp:``)."""
    pos = 0
    protocol: str | None = None
    if text.startswith("mailto:"):
        protocol = "mailto"
        pos = 7
    elif text.startswith("xmpp:"):
        protocol = "xmpp"
        pos = 5

    return match_any_email(text, pos, protocol)

