
def all_urls_valid(text: str) -> bool:
    """
    Check if all URLs in text are valid.

    Args:
        text: The text containing URLs

    Returns:
        True if all URLs are valid (or no URLs), False otherwise
    """
    urls = extract_urls(text)
    return all(is_valid_url(url) for url in urls)

