
def read_str_list(data: ReadBuffer) -> list[str]:
    assert read_tag(data) == LIST_STR
    size = read_int_bare(data)
    return [read_str_bare(data) for _ in range(size)]

