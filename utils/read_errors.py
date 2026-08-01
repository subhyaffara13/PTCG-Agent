
def read_errors(data: ReadBuffer) -> list[ErrorTuple]:
    assert read_tag(data) == LIST_GEN
    result = []
    for _ in range(read_int_bare(data)):
        assert read_tag(data) == TUPLE_GEN
        result.append(
            (
                read_str_opt(data),
                read_int(data),
                read_int(data),
                read_int(data),
                read_int(data),
                read_str(data),
                read_str(data),
                read_str_opt(data),
            )
        )
    return result

