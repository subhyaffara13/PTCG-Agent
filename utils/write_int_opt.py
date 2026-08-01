
def write_int_opt(data: WriteBuffer, value: int | None) -> None:
    if value is not None:
        write_tag(data, LITERAL_INT)
        write_int_bare(data, value)
    else:
        write_tag(data, LITERAL_NONE)

