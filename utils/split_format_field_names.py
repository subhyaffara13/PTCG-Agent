
def split_format_field_names(
    format_string: str,
) -> tuple[str, Iterable[tuple[bool, str]]]:
    try:
        return _string.formatter_field_name_split(format_string)  # type: ignore[no-any-return]
    except ValueError as e:
        raise IncompleteFormatString() from e

