
def get_url_scheme(url: str) -> Optional[str]:
    if ":" not in url:
        return None
    return url.split(":", 1)[0].lower()

