
def parse_set_member(source, info):
    "Parses a member in a character set."
    # Parse a set item.
    start = parse_set_item(source, info)
    saved_pos1 = source.pos
    if (not isinstance(start, Character) or not start.positive or not
      source.match("-")):
        # It's not the start of a range.
        return start

    version = (info.flags & _ALL_VERSIONS) or DEFAULT_VERSION

    # It looks like the start of a range of characters.
    saved_pos2 = source.pos
    if version == VERSION1 and source.match("-"):
        # It's actually the set difference operator '--', so return the
        # character.
        source.pos = saved_pos1
        return start

    if source.match("]"):
        # We've reached the end of the set, so return both the character and
        # hyphen.
        source.pos = saved_pos2
        return SetUnion(info, [start, Character(ord("-"))])

    # Parse a set item.
    end = parse_set_item(source, info)
    if not isinstance(end, Character) or not end.positive:
        # It's not a range, so return the character, hyphen and property.
        return SetUnion(info, [start, Character(ord("-")), end])

    # It _is_ a range.
    if start.value > end.value:
        raise error("bad character range", source.string, source.pos)

    if start.value == end.value:
        return start

    return Range(start.value, end.value)

