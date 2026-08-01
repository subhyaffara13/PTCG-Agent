
def get_custom_labels_from_metadata(metadata: dict) -> Dict[str, str]:
    """
    Get custom labels from metadata
    """
    keys = litellm.custom_prometheus_metadata_labels
    if keys is None or len(keys) == 0:
        return {}

    result: Dict[str, str] = {}

    for key in keys:
        # Split the dot notation key into parts
        original_key = key
        key = key.replace("metadata.", "", 1) if key.startswith("metadata.") else key

        keys_parts = key.split(".")
        # Traverse through the dictionary using the parts
        value: Any = metadata
        for part in keys_parts:
            if isinstance(value, dict):
                value = value.get(part, None)  # Get the value, return None if not found
            else:
                value = None
            if value is None:
                break

        if value is not None and isinstance(value, str):
            result[original_key.replace(".", "_")] = value

    return result

