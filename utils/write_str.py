
def write_str(data: WriteBuffer, value: str) -> None:
    write_tag(data, LITERAL_STR)
    write_str_bare(data, value)

