
def write_str_opt(data: WriteBuffer, value: str | None) -> None:
    if value is not None:
        write_tag(data, LITERAL_STR)
        write_str_bare(data, value)
    else:
        write_tag(data, LITERAL_NONE)

