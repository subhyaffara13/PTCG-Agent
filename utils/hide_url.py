
def hide_url(url: str) -> HiddenText:
    redacted = redact_auth_from_url(url)
    return HiddenText(url, redacted=redacted)

