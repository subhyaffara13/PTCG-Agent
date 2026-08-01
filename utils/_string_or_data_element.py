
def _string_or_data_element(raw_bytes: bytes, ctx: SimpleNamespace) -> etree.Element:
    if ctx.use_builtin_types:
        return _data_element(raw_bytes, ctx)
    else:
        try:
            string = raw_bytes.decode(encoding="ascii", errors="strict")
        except UnicodeDecodeError:
            raise ValueError(
                "invalid non-ASCII bytes; use unicode string instead: %r" % raw_bytes
            )
        return _string_element(string, ctx)

