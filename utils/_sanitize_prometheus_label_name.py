
def _sanitize_prometheus_label_name(label: str) -> str:
    """
    Sanitize a label name to comply with Prometheus label name requirements.

    Prometheus label names must match: ^[a-zA-Z_][a-zA-Z0-9_]*$
    - First character: letter (a-z, A-Z) or underscore (_)
    - Subsequent characters: letters, digits (0-9), or underscores (_)

    Args:
        label: The label name to sanitize

    Returns:
        A sanitized label name that complies with Prometheus requirements
    """
    if not label:
        return "_"

    # Replace all invalid characters with underscores
    # Keep only letters, digits, and underscores
    sanitized = re.sub(r"[^a-zA-Z0-9_]", "_", label)

    # Ensure first character is valid (letter or underscore)
    if sanitized and not re.match(r"^[a-zA-Z_]", sanitized[0]):
        sanitized = "_" + sanitized

    # Handle empty string after sanitization
    if not sanitized:
        sanitized = "_"

    return sanitized

