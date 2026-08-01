
def parse_subpattern(source, info, flags_on, flags_off):
    "Parses a subpattern with scoped flags."
    saved_flags = info.flags
    info.flags = (info.flags | flags_on) & ~flags_off

    # Ensure that there aren't multiple encoding flags set.
    if info.flags & (ASCII | LOCALE | UNICODE):
        info.flags = (info.flags & ~_ALL_ENCODINGS) | flags_on

    source.ignore_space = bool(info.flags & VERBOSE)
    try:
        subpattern = _parse_pattern(source, info)
        source.expect(")")
    finally:
        info.flags = saved_flags
        source.ignore_space = bool(info.flags & VERBOSE)

    return subpattern

