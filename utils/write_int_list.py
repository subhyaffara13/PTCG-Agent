
def write_int_list(data: WriteBuffer, value: list[int]) -> None:
    write_tag(data, LIST_INT)
    write_int_bare(data, len(value))
    for item in value:
        write_int_bare(data, item)

