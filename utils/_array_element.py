
def _array_element(
    array: Sequence[PlistEncodable], ctx: SimpleNamespace
) -> etree.Element:
    el = etree.Element("array")
    if len(array) == 0:
        return el
    ctx.indent_level += 1
    for value in array:
        el.append(_make_element(value, ctx))
    ctx.indent_level -= 1
    return el

