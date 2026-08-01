
def parse_call_named_group(source, info, pos):
    "Parses a call to a named group."
    group = parse_name(source)
    source.expect(")")

    return CallGroup(info, group, pos)

