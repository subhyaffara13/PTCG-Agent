
def read_int_opt(data: ReadBuffer) -> int | None:
    tag = read_tag(data)
    if tag == LITERAL_NONE:
        return None
    assert tag == LITERAL_INT
    return read_int_bare(data)

