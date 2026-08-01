
def _parse_labels_map(labels: list[str] | None) -> dict[str, str] | None:
    """Parse label key-value pairs from CLI arguments.

    Args:
        labels: List of label strings in KEY=VALUE format. If KEY only, then VALUE is set to empty string.

    Returns:
        Dictionary mapping label keys to values, or None if no labels provided.
    """
    if not labels:
        return None
    labels_map: dict[str, str] = {}
    for label_var in labels:
        key, value = label_var.split("=", 1) if "=" in label_var else (label_var, "")
        labels_map[key] = value
    return labels_map

