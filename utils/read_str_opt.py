
def read_str_opt(data: ReadBuffer) -> str | None:
    tag = read_tag(data)
    if tag == LITERAL_NONE:
        return None
    assert tag == LITERAL_STR
    return read_str_bare(data)

