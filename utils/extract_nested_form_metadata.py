from typing import Any, Dict

def extract_nested_form_metadata(
    form_data: Dict[str, Any], prefix: str = "litellm_metadata["
) -> Dict[str, Any]:
    """
    Extract nested metadata from form data with bracket notation.

    Handles form data that uses bracket notation to represent nested dictionaries,
    such as litellm_metadata[spend_logs_metadata][owner] = "value".

    This is commonly encountered when SDKs or clients send form data with nested
    structures using bracket notation instead of JSON.

    Args:
        form_data: Dictionary containing form data (from request.form())
        prefix: The prefix to look for in form keys (default: "litellm_metadata[")

    Returns:
        Dictionary with nested structure reconstructed from bracket notation

    Example:
        Input form_data:
        {
            "litellm_metadata[spend_logs_metadata][owner]": "john",
            "litellm_metadata[spend_logs_metadata][team]": "engineering",
            "litellm_metadata[tags]": "production",
            "other_field": "value"
        }

        Output:
        {
            "spend_logs_metadata": {
                "owner": "john",
                "team": "engineering"
            },
            "tags": "production"
        }
    """
    if not form_data:
        return {}

    metadata: Dict[str, Any] = {}

    for key, value in form_data.items():
        # Skip keys that don't start with the prefix
        if not isinstance(key, str) or not key.startswith(prefix):
            continue

        # Skip UploadFile objects - they should not be in metadata
        if isinstance(value, UploadFile):
            verbose_proxy_logger.warning(
                f"Skipping UploadFile in metadata extraction for key: {key}"
            )
            continue

        # Extract the nested path from bracket notation
        # Example: "litellm_metadata[spend_logs_metadata][owner]" -> ["spend_logs_metadata", "owner"]
        try:
            # Remove the prefix and strip trailing ']'
            path_string = key.replace(prefix, "").rstrip("]")

            # Split by "][" to get individual path parts
            parts = path_string.split("][")

            if not parts or not parts[0]:
                verbose_proxy_logger.warning(
                    f"Invalid metadata key format (empty path): {key}"
                )
                continue

            # Navigate/create nested dictionary structure
            current = metadata
            for part in parts[:-1]:
                if not isinstance(current, dict):
                    verbose_proxy_logger.warning(
                        f"Cannot create nested path - intermediate value is not a dict at: {part}"
                    )
                    break
                current = current.setdefault(part, {})
            else:
                # Set the final value (only if we didn't break out of the loop)
                if isinstance(current, dict):
                    current[parts[-1]] = value
                else:
                    verbose_proxy_logger.warning(
                        f"Cannot set value - parent is not a dict for key: {key}"
                    )

        except Exception as e:
            verbose_proxy_logger.error(f"Error parsing metadata key '{key}': {str(e)}")
            continue

    return metadata

