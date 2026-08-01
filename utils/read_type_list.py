
def read_type_list(data: ReadBuffer) -> list[Type]:
    assert read_tag(data) == LIST_GEN
    size = read_int_bare(data)
    return [read_type(data) for _ in range(size)]

