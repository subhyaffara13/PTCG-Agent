
def read_int(data: ReadBuffer) -> int:
    assert read_tag(data) == LITERAL_INT
    return read_int_bare(data)

