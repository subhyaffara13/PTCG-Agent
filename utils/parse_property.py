
def parse_property(source, info, positive, in_set):
    "Parses a Unicode property."
    saved_pos = source.pos
    ch = source.get()
    if ch == "{":
        negate = source.match("^")
        prop_name, name = parse_property_name(source)
        if source.match("}"):
            # It's correctly delimited.
            if info.flags & ASCII:
                encoding = ASCII_ENCODING
            elif info.flags & UNICODE:
                encoding = UNICODE_ENCODING
            else:
                encoding = 0

            prop = lookup_property(prop_name, name, positive != negate, source,
              encoding=encoding)
            return make_property(info, prop, in_set)
    elif ch and ch in "CLMNPSZ":
        # An abbreviated property, eg \pL.
        if info.flags & ASCII:
            encoding = ASCII_ENCODING
        elif info.flags & UNICODE:
            encoding = UNICODE_ENCODING
        else:
            encoding = 0

        prop = lookup_property(None, ch, positive, source, encoding=encoding)
        return make_property(info, prop, in_set)

    # Not a property, so treat as a literal "p" or "P".
    source.pos = saved_pos
    ch = "p" if positive else "P"
    return make_character(info, ord(ch), in_set)

