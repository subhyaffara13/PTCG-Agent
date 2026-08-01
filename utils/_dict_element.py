
def _dict_element(
    d: Mapping[str, PlistEncodable], ctx: SimpleNamespace
) -> etree.Element:
    el = etree.Element("dict")
    items = d.items()
    if ctx.sort_keys:
        items = sorted(items)  # type: ignore
    ctx.indent_level += 1
    for key, value in items:
        if not isinstance(key, str):
            if ctx.skipkeys:
                continue
            raise TypeError("keys must be strings")
        k = etree.SubElement(el, "key")
        k.text = tostr(key, "utf-8")
        el.append(_make_element(value, ctx))
    ctx.indent_level -= 1
    return el

