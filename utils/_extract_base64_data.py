
def _extract_base64_data(image_url: str) -> str:
    """
    Extract pure base64 data from an image URL.

    If the URL is a data URL (e.g., "data:image/png;base64,iVBOR..."),
    extract and return only the base64 data portion.
    Otherwise, return the original URL unchanged.

    This is needed for providers like Ollama that expect pure base64 data
    rather than full data URLs.

    Args:
        image_url: The image URL or data URL to process

    Returns:
        The base64 data if it's a data URL, otherwise the original URL
    """
    if image_url.startswith("data:") and ";base64," in image_url:
        return image_url.split(";base64,", 1)[1]
    return image_url

