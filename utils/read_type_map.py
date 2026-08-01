
def read_type_map(data: ReadBuffer) -> dict[str, Type]:
    assert read_tag(data) == DICT_STR_GEN
    size = read_int_bare(data)
    return {read_str_bare(data): read_type(data) for _ in range(size)}

