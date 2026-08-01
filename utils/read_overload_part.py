
def read_overload_part(data: ReadBuffer, tag: Tag | None = None) -> OverloadPart:
    if tag is None:
        tag = read_tag(data)
    if tag == DECORATOR:
        return Decorator.read(data)
    if tag == FUNC_DEF:
        return FuncDef.read(data)
    assert False, f"Invalid tag for an OverloadPart {tag}"

