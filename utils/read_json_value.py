
def read_json_value(data: ReadBuffer) -> JsonValue:
    tag = read_tag(data)
    if tag == LITERAL_NONE:
        return None
    if tag == LITERAL_FALSE:
        return False
    if tag == LITERAL_TRUE:
        return True
    if tag == LITERAL_INT:
        return read_int_bare(data)
    if tag == LITERAL_STR:
        return read_str_bare(data)
    if tag == LIST_GEN:
        size = read_int_bare(data)
        return [read_json_value(data) for _ in range(size)]
    if tag == TUPLE_GEN:
        size = read_int_bare(data)
        return tuple(read_json_value(data) for _ in range(size))
    if tag == DICT_STR_GEN:
        size = read_int_bare(data)
        return {read_str_bare(data): read_json_value(data) for _ in range(size)}
    if tag == LITERAL_FLOAT:
        return read_float_bare(data)
    assert False, f"Invalid JSON tag: {tag}"

