
def parse_set(source, info):
    "Parses a character set."
    version = (info.flags & _ALL_VERSIONS) or DEFAULT_VERSION

    saved_ignore = source.ignore_space
    source.ignore_space = False
    # Negative set?
    negate = source.match("^")
    try:
        if version == VERSION0:
            item = parse_set_imp_union(source, info)
        else:
            item = parse_set_union(source, info)

        if not source.match("]"):
            raise error("missing ]", source.string, source.pos)
    finally:
        source.ignore_space = saved_ignore

    if negate:
        item = item.with_flags(positive=not item.positive)

    item = item.with_flags(case_flags=make_case_flags(info))

    return item

