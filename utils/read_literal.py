
def read_literal(data: ReadBuffer, tag: Tag) -> int | str | bool | float:
    if tag == LITERAL_INT:
        return read_int_bare(data)
    elif tag == LITERAL_STR:
        return read_str_bare(data)
    elif tag == LITERAL_FALSE:
        return False
    elif tag == LITERAL_TRUE:
        return True
    elif tag == LITERAL_FLOAT:
        return read_float_bare(data)
    assert False, f"Unknown literal tag {tag}"

