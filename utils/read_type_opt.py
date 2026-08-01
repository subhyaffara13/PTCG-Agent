
def read_type_opt(data: ReadBuffer) -> Type | None:
    tag = read_tag(data)
    if tag == LITERAL_NONE:
        return None
    return read_type(data, tag)

