import re
from typing import List

def detect_code_languages(text: str) -> List[str]:
    """
    Detect which programming languages are present in text.

    Args:
        text: The text to analyze

    Returns:
        List of detected language names
    """
    detected = []
    for lang, patterns in _CODE_PATTERNS.items():
        for pattern in patterns:
            try:
                if re.search(pattern, text, re.IGNORECASE | re.MULTILINE):
                    detected.append(lang)
                    break  # Only add each language once
            except re.error:
                continue
    return detected

