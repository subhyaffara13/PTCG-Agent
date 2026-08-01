
def parse_rel_call_group(source, info, ch, pos):
    "Parses a relative call to a group."
    digits = source.get_while(DIGITS)
    if not digits:
        raise error("missing relative group number", source.string, source.pos)

    offset = int(digits)
    group = info.group_count + offset if ch == "+" else info.group_count - offset + 1
    if group <= 0:
        raise error("invalid relative group number", source.string, source.pos)

    source.expect(")")

    return CallGroup(info, group, pos)

