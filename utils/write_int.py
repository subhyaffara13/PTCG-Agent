
def write_int(data: WriteBuffer, value: int) -> None:
    write_tag(data, LITERAL_INT)
    write_int_bare(data, value)

