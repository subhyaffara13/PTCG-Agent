
def read_str(data: ReadBuffer) -> str:
    assert read_tag(data) == LITERAL_STR
    return read_str_bare(data)

