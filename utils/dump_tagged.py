
def dump_tagged(nodes: Sequence[object], tag: str | None, str_conv: StrConv) -> str:
    """Convert an array into a pretty-printed multiline string representation.

    The format is
      tag(
        item1..
        itemN)
    Individual items are formatted like this:
     - arrays are flattened
     - pairs (str, array) are converted recursively, so that str is the tag
     - other items are converted to strings and indented
    """
    from mypy.types import Type, TypeStrVisitor

    a: list[str] = []
    if tag:
        a.append(tag + "(")
    for n in nodes:
        if isinstance(n, list):
            if n:
                a.append(dump_tagged(n, None, str_conv))
        elif isinstance(n, tuple):
            s = dump_tagged(n[1], n[0], str_conv)
            a.append(indent(s, 2))
        elif isinstance(n, mypy.nodes.Node):
            a.append(indent(n.accept(str_conv), 2))
        elif isinstance(n, Type):
            a.append(
                indent(n.accept(TypeStrVisitor(str_conv.id_mapper, options=str_conv.options)), 2)
            )
        elif n is not None:
            a.append(indent(str(n), 2))
    if tag:
        a[-1] += ")"
    return "\n".join(a)

