
def read_bytes_list(data: ReadBuffer) -> list[bytes]:
    assert read_tag(data) == LIST_BYTES
    size = read_int_bare(data)
    return [read_bytes_bare(data) for _ in range(size)]

