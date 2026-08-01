
def markup_join(seq: t.Iterable[t.Any]) -> str:
    """Concatenation that escapes if necessary and converts to string."""
    buf = []
    iterator = map(soft_str, seq)
    for arg in iterator:
        buf.append(arg)
        if hasattr(arg, "__html__"):
            return Markup("").join(chain(buf, iterator))
    return concat(buf)

