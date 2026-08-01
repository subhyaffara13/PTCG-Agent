
def _data_element(data: bytes, ctx: SimpleNamespace) -> etree.Element:
    el = etree.Element("data")
    # NOTE: mypy is confused about whether el.text should be str or bytes.
    el.text = _encode_base64(  # type: ignore
        data,
        maxlinelength=(76 if ctx.pretty_print else None),
        indent_level=ctx.indent_level,
    )
    return el

