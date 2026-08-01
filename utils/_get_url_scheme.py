
def _get_url_scheme(url):
    if ":" not in url:
        return None
    return url.split(":", 1)[0].lower()

