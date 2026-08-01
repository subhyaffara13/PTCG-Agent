
def parse_atomic(source, info):
    "Parses an atomic subpattern."
    saved_flags = info.flags
    try:
        subpattern = _parse_pattern(source, info)
        source.expect(")")
    finally:
        info.flags = saved_flags
        source.ignore_space = bool(info.flags & VERBOSE)

    return Atomic(subpattern)

