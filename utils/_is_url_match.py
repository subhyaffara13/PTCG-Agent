
def _is_url_match(url, matchers: List[str]) -> bool:
    """Check if URL matches any of the provided matchers."""
    try:
        parsed_url = httpx.URL(url) if isinstance(url, str) else url
        url_str = str(parsed_url).lower()
        hostname = parsed_url.host or ""

        for matcher in matchers:
            if matcher.lower() in url_str or matcher.lower() in hostname.lower():
                return True

        # Also check for localhost with matcher in path
        if hostname in ("localhost", "127.0.0.1"):
            for matcher in matchers:
                if matcher.lower() in url_str:
                    return True

        return False
    except Exception:
        return False

