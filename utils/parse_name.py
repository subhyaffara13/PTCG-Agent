
def parse_name(source, allow_numeric=False, allow_group_0=False):
    "Parses a name."
    name = source.get_while(set(")>"), include=False)

    if not name:
        raise error("missing group name", source.string, source.pos)

    if name.isdigit():
        min_group = 0 if allow_group_0 else 1
        if not allow_numeric or int(name) < min_group:
            raise error("bad character in group name", source.string,
              source.pos)
    else:
        if not name.isidentifier():
            raise error("bad character in group name", source.string,
              source.pos)

    return name

