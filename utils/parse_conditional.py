
def parse_conditional(source, info):
    "Parses a conditional subpattern."
    saved_flags = info.flags
    saved_pos = source.pos
    ch = source.get()
    if ch == "?":
        # (?(?...
        ch = source.get()
        if ch in ("=", "!"):
            # (?(?=... or (?(?!...: lookahead conditional.
            return parse_lookaround_conditional(source, info, False, ch == "=")
        if ch == "<":
            # (?(?<...
            ch = source.get()
            if ch in ("=", "!"):
                # (?(?<=... or (?(?<!...: lookbehind conditional.
                return parse_lookaround_conditional(source, info, True, ch ==
                  "=")

        source.pos = saved_pos
        raise error("expected lookaround conditional", source.string,
          source.pos)

    source.pos = saved_pos
    try:
        group = parse_name(source, True)
        source.expect(")")
        yes_branch = parse_sequence(source, info)
        if source.match("|"):
            no_branch = parse_sequence(source, info)
        else:
            no_branch = Sequence()

        source.expect(")")
    finally:
        info.flags = saved_flags
        source.ignore_space = bool(info.flags & VERBOSE)

    if yes_branch.is_empty() and no_branch.is_empty():
        return Sequence()

    return Conditional(info, group, yes_branch, no_branch, saved_pos)

