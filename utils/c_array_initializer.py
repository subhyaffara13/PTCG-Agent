
def c_array_initializer(components: list[str], *, indented: bool = False) -> str:
    """Construct an initializer for a C array variable.

    Components are C expressions valid in an initializer.

    For example, if components are ["1", "2"], the result
    would be "{1, 2}", which can be used like this:

        int a[] = {1, 2};

    If the result is long, split it into multiple lines.
    """
    indent = " " * 4 if indented else ""
    res = []
    current: list[str] = []
    cur_len = 0
    for c in components:
        if not current or cur_len + 2 + len(indent) + len(c) < 70:
            current.append(c)
            cur_len += len(c) + 2
        else:
            res.append(indent + ", ".join(current))
            current = [c]
            cur_len = len(c)
    if not res:
        # Result fits on a single line
        return "{%s}" % ", ".join(current)
    # Multi-line result
    res.append(indent + ", ".join(current))
    return "{\n    " + ",\n    ".join(res) + "\n" + indent + "}"

