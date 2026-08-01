
def set_format_options(fmt, format_options):
    """Apply the desired format options to the format description fmt"""
    if not format_options:
        return

    for opt in format_options:
        try:
            key, value = opt.split("=")
        except ValueError as err:
            raise ValueError(f"Format options are expected to be of the form key=value, not '{opt}'") from err

        if key not in _VALID_FORMAT_OPTIONS:
            raise ValueError(
                "'{}' is not a valid format option. Expected one of '{}'".format(key, "', '".join(_VALID_FORMAT_OPTIONS))
            )

        if key in _BINARY_FORMAT_OPTIONS:
            value = str2bool(value)

        fmt[key] = value

