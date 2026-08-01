
def validate_one_format(jupytext_format: dict[str, str]) -> dict[str, str]:
    """Validate extension and options for the given format"""
    if not isinstance(jupytext_format, dict):
        raise JupytextFormatError("Jupytext format should be a dictionary")

    if "format_name" in jupytext_format and jupytext_format["format_name"] not in _VALID_FORMAT_NAMES:
        raise JupytextFormatError(
            "{} is not a valid format name. Please choose one of {}".format(
                jupytext_format.get("format_name"), ", ".join(_VALID_FORMAT_NAMES)
            )
        )

    for key in jupytext_format:
        if key not in _VALID_FORMAT_INFO + _VALID_FORMAT_OPTIONS:
            raise JupytextFormatError(
                "Unknown format option '{}' - should be one of '{}'".format(key, "', '".join(_VALID_FORMAT_OPTIONS))
            )
        value = jupytext_format[key]
        if key in _BINARY_FORMAT_OPTIONS:
            if not isinstance(value, bool):
                raise JupytextFormatError(f"Format option '{key}' should be a bool, not '{str(value)}'")

    if "extension" not in jupytext_format:
        raise JupytextFormatError("Missing format extension")
    ext = jupytext_format["extension"]
    if ext not in NOTEBOOK_EXTENSIONS + [".auto"]:
        raise JupytextFormatError(
            "Extension '{}' is not a notebook extension. Please use one of '{}'.".format(
                ext, "', '".join(NOTEBOOK_EXTENSIONS + [".auto"])
            )
        )

    return jupytext_format

