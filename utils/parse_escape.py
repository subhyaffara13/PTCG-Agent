
def parse_escape(source, info, in_set):
    "Parses an escape sequence."
    saved_ignore = source.ignore_space
    source.ignore_space = False
    ch = source.get()
    source.ignore_space = saved_ignore
    if not ch:
        # A backslash at the end of the pattern.
        raise error("bad escape (end of pattern)", source.string, source.pos)
    if ch in HEX_ESCAPES:
        # A hexadecimal escape sequence.
        return parse_hex_escape(source, info, ch, HEX_ESCAPES[ch], in_set, ch)
    elif ch == "g" and not in_set:
        # A group reference.
        saved_pos = source.pos
        try:
            return parse_group_ref(source, info)
        except error:
            # Invalid as a group reference, so assume it's a literal.
            source.pos = saved_pos

        return make_character(info, ord(ch), in_set)
    elif ch == "G" and not in_set:
        # A search anchor.
        return SearchAnchor()
    elif ch == "L" and not in_set:
        # A string set.
        return parse_string_set(source, info)
    elif ch == "N":
        # A named codepoint.
        return parse_named_char(source, info, in_set)
    elif ch in "pP":
        # A Unicode property, positive or negative.
        return parse_property(source, info, ch == "p", in_set)
    elif ch == "R" and not in_set:
        # A line ending.
        charset = [0x0A, 0x0B, 0x0C, 0x0D]
        if info.guess_encoding == UNICODE:
            charset.extend([0x85, 0x2028, 0x2029])

        return Atomic(Branch([String([0x0D, 0x0A]), SetUnion(info, [Character(c)
          for c in charset])]))
    elif ch == "X" and not in_set:
        # A grapheme cluster.
        return Grapheme()
    elif ch in ALPHA:
        # An alphabetic escape sequence.
        # Positional escapes aren't allowed inside a character set.
        if not in_set:
            if info.flags & WORD:
                value = WORD_POSITION_ESCAPES.get(ch)
            elif info.flags & ASCII:
                value = ASCII_POSITION_ESCAPES.get(ch)
            elif info.flags & UNICODE:
                value = UNICODE_POSITION_ESCAPES.get(ch)
            else:
                value = POSITION_ESCAPES.get(ch)

            if value:
                return value

        if info.flags & ASCII:
            value = ASCII_CHARSET_ESCAPES.get(ch)
        elif info.flags & UNICODE:
            value = UNICODE_CHARSET_ESCAPES.get(ch)
        else:
            value = CHARSET_ESCAPES.get(ch)

        if value:
            return value

        value = CHARACTER_ESCAPES.get(ch)
        if value:
            return Character(ord(value))

        raise error("bad escape \\%s" % ch, source.string, source.pos)
    elif ch in DIGITS:
        # A numeric escape sequence.
        return parse_numeric_escape(source, info, ch, in_set)
    else:
        # A literal.
        return make_character(info, ord(ch), in_set)

