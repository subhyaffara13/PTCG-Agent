
def _str_header_value(value: t.Any) -> str:
    if not isinstance(value, str):
        value = str(value)

    if _newline_re.search(value) is not None:
        raise ValueError("Header values must not contain newline characters.")

    return value  # type: ignore[no-any-return]

