
def contains_code_language(text: str, languages: List[str]) -> bool:
    """
    Check if text contains code from specific languages.

    Args:
        text: The text to check
        languages: List of language names to check for

    Returns:
        True if any of the specified languages are detected
    """
    detected = detect_code_languages(text)
    return any(lang.lower() in [d.lower() for d in detected] for lang in languages)

