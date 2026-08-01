
def read_bytes(data: ReadBuffer) -> bytes:
    assert read_tag(data) == LITERAL_BYTES
    return read_bytes_bare(data)

