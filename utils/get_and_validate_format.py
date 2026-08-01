
def get_and_validate_format() -> Literal["toml", "ini"]:
    """Make sure that the output format is either .toml or .ini."""
    # pylint: disable-next=bad-builtin
    format_type = input(
        "Please choose the format of configuration, (T)oml or (I)ni (.cfg): "
    ).lower()

    if format_type not in SUPPORTED_FORMATS:
        raise InvalidUserInput(", ".join(sorted(SUPPORTED_FORMATS)), format_type)

    if format_type.startswith("t"):
        return "toml"
    return "ini"

