import re

def _sanitize_gcp_label_value(value: str) -> str:
    """
    Sanitize a string to meet GCP label value constraints.

    GCP label values must:
    - Be lowercase
    - Contain only letters, numbers, underscores, and hyphens
    - Be max 63 characters

    Args:
        value: The string to sanitize

    Returns:
        A sanitized string that meets GCP label constraints
    """
    sanitized = re.sub(r"[^a-z0-9_-]", "_", value.lower())
    return sanitized[:_GCP_LABEL_VALUE_MAX_LEN]

