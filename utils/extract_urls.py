
def extract_urls(text: str) -> List[str]:
    """
    Extract all URLs from text.

    Args:
        text: The text to search for URLs

    Returns:
        List of URLs found in the text
    """
    return _URL_PATTERN.findall(text)

