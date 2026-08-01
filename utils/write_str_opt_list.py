
def write_str_opt_list(data: WriteBuffer, value: list[str | None]) -> None:
    write_tag(data, LIST_GEN)
    write_int_bare(data, len(value))
    for item in value:
        write_str_opt(data, item)

