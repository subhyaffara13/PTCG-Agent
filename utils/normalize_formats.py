
def normalize_formats(formats) -> list[str]:
    """Normalize the formats option into a list of string-encoded paired formats"""
    # Process formats - can be string, dict, or list
    if isinstance(formats, str):
        # Split on semicolon for multiple format groups
        formats = formats.split(";")
    elif isinstance(formats, dict):
        # Single dict - wrap in list for uniform processing
        formats = [formats]
    elif formats is None:
        formats = []
    elif not isinstance(formats, list):
        raise JupytextConfigurationError(
            f"Invalid type for 'formats': {type(formats).__name__}. Expected str, dict, list of str or dict."
        )

    # Each group of paired formats can be a string or a dict
    string_encoded_pairing_formats = []

    for paired_formats in formats:
        if isinstance(paired_formats, str):
            string_encoded_pairing_formats.append(paired_formats)
        elif isinstance(paired_formats, dict):
            # Convert dict to format string
            paired_formats = [
                (f if not prefix else (prefix[:-1] if prefix.endswith("/") else prefix) + "///" + f)
                for prefix, f in paired_formats.items()
            ]
            string_encoded_pairing_formats.append(short_form_multiple_formats(paired_formats))
        else:
            raise JupytextConfigurationError(
                f"Invalid paired formats: {paired_formats}. Expected str or dict, got {type(paired_formats).__name__}."
            )

    return string_encoded_pairing_formats

