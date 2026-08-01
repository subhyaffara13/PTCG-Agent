
def write_str_list(data: WriteBuffer, value: Sequence[str]) -> None:
    write_tag(data, LIST_STR)
    write_int_bare(data, len(value))
    for item in value:
        write_str_bare(data, item)

