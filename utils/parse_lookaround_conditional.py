
def parse_lookaround_conditional(source, info, behind, positive):
    saved_flags = info.flags
    try:
        subpattern = _parse_pattern(source, info)
        source.expect(")")
    finally:
        info.flags = saved_flags
        source.ignore_space = bool(info.flags & VERBOSE)

    yes_branch = parse_sequence(source, info)
    if source.match("|"):
        no_branch = parse_sequence(source, info)
    else:
        no_branch = Sequence()

    source.expect(")")

    return LookAroundConditional(behind, positive, subpattern, yes_branch,
      no_branch)

