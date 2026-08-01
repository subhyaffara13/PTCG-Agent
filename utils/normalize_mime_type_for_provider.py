
def normalize_mime_type_for_provider(
    mime_type: str, provider: Optional[str] = None
) -> str:
    """
    Normalize MIME type for specific provider requirements.

    Currently handles:
    - Gemini: Normalizes image/jpg to image/jpeg

    Args:
        mime_type: Original MIME type
        provider: Provider name (e.g., "gemini", "vertex_ai")

    Returns:
        str: Normalized MIME type
    """
    normalized = mime_type.lower().strip()

    # Gemini/Vertex AI requires image/jpeg, not image/jpg
    if provider and ("gemini" in provider.lower() or "vertex_ai" in provider.lower()):
        if normalized == "image/jpg":
            normalized = "image/jpeg"

    # General normalization: always normalize jpg to jpeg
    if normalized == "image/jpg":
        normalized = "image/jpeg"

    return normalized

