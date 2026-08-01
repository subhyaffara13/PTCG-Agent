
def parse_set_item(source, info):
    "Parses an item in a character set."
    version = (info.flags & _ALL_VERSIONS) or DEFAULT_VERSION

    if source.match("\\"):
        # An escape sequence in a set.
        return parse_escape(source, info, True)

    saved_pos = source.pos
    if source.match("[:"):
        # Looks like a POSIX character class.
        try:
            return parse_posix_class(source, info)
        except ParseError:
            # Not a POSIX character class.
            source.pos = saved_pos

    if version == VERSION1 and source.match("["):
        # It's the start of a nested set.

        # Negative set?
        negate = source.match("^")
        item = parse_set_union(source, info)

        if not source.match("]"):
            raise error("missing ]", source.string, source.pos)

        if negate:
            item = item.with_flags(positive=not item.positive)

        return item

    ch = source.get()
    if not ch:
        raise error("unterminated character set", source.string, source.pos)

    return Character(ord(ch))

