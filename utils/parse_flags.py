
def parse_flags(source, info):
    "Parses flags being turned on/off."
    flags_on = parse_flag_set(source)
    if source.match("-"):
        flags_off = parse_flag_set(source)
        if not flags_off:
            raise error("bad inline flags: no flags after '-'", source.string,
              source.pos)
    else:
        flags_off = 0

    if flags_on & LOCALE:
        # Remember that this pattern as an inline locale flag.
        info.inline_locale = True

    return flags_on, flags_off

