
def read_int_list(data: ReadBuffer) -> list[int]:
    assert read_tag(data) == LIST_INT
    size = read_int_bare(data)
    return [read_int_bare(data) for _ in range(size)]

