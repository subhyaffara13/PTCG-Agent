
def read_str_opt_list(data: ReadBuffer) -> list[str | None]:
    assert read_tag(data) == LIST_GEN
    size = read_int_bare(data)
    return [read_str_opt(data) for _ in range(size)]

