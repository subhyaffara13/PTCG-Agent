
def parse_paren(source, info):
    """Parses a parenthesised subpattern or a flag. Returns FLAGS if it's an
    inline flag.
    """
    saved_pos = source.pos
    ch = source.get(True)
    if ch == "?":
        # (?...
        saved_pos_2 = source.pos
        ch = source.get(True)
        if ch == "<":
            # (?<...
            saved_pos_3 = source.pos
            ch = source.get()
            if ch in ("=", "!"):
                # (?<=... or (?<!...: lookbehind.
                return parse_lookaround(source, info, True, ch == "=")

            # (?<...: a named capture group.
            source.pos = saved_pos_3
            name = parse_name(source)
            group = info.open_group(name)
            source.expect(">")
            saved_flags = info.flags
            try:
                subpattern = _parse_pattern(source, info)
                source.expect(")")
            finally:
                info.flags = saved_flags
                source.ignore_space = bool(info.flags & VERBOSE)

            info.close_group()
            return Group(info, group, subpattern)
        if ch in ("=", "!"):
            # (?=... or (?!...: lookahead.
            return parse_lookaround(source, info, False, ch == "=")
        if ch == "P":
            # (?P...: a Python extension.
            return parse_extension(source, info)
        if ch == "#":
            # (?#...: a comment.
            return parse_comment(source)
        if ch == "(":
            # (?(...: a conditional subpattern.
            return parse_conditional(source, info)
        if ch == ">":
            # (?>...: an atomic subpattern.
            return parse_atomic(source, info)
        if ch == "|":
            # (?|...: a common/reset groups branch.
            return parse_common(source, info)
        if ch == "R" or "0" <= ch <= "9":
            # (?R...: probably a call to a group.
            return parse_call_group(source, info, ch, saved_pos_2)
        if ch == "&":
            # (?&...: a call to a named group.
            return parse_call_named_group(source, info, saved_pos_2)
        if (ch == "+" or ch == "-") and source.peek() in DIGITS:
            return parse_rel_call_group(source, info, ch, saved_pos_2)

        # (?...: probably a flags subpattern.
        source.pos = saved_pos_2
        return parse_flags_subpattern(source, info)

    if ch == "*":
        # (*...
        saved_pos_2 = source.pos
        word = source.get_while(set(")>"), include=False)
        if word[ : 1].isalpha():
            verb = VERBS.get(word)
            if not verb:
                raise error("unknown verb", source.string, saved_pos_2)

            source.expect(")")

            return verb

    # (...: an unnamed capture group.
    source.pos = saved_pos
    group = info.open_group()
    saved_flags = info.flags
    try:
        subpattern = _parse_pattern(source, info)
        source.expect(")")
    finally:
        info.flags = saved_flags
        source.ignore_space = bool(info.flags & VERBOSE)

    info.close_group()

    return Group(info, group, subpattern)

