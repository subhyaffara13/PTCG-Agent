
def write_bytes(data: WriteBuffer, value: bytes) -> None:
    write_tag(data, LITERAL_BYTES)
    write_bytes_bare(data, value)

