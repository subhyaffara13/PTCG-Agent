
def parse_lookaround(source, info, behind, positive):
    "Parses a lookaround."
    saved_flags = info.flags
    try:
        subpattern = _parse_pattern(source, info)
        source.expect(")")
    finally:
        info.flags = saved_flags
        source.ignore_space = bool(info.flags & VERBOSE)

    return LookAround(behind, positive, subpattern)

