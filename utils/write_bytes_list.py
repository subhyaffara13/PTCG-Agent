
def write_bytes_list(data: WriteBuffer, value: Sequence[bytes]) -> None:
    write_tag(data, LIST_BYTES)
    write_int_bare(data, len(value))
    for item in value:
        write_bytes_bare(data, item)

