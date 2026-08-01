
def make_case_flags(info):
    "Makes the case flags."
    flags = info.flags & CASE_FLAGS

    # Turn off FULLCASE if ASCII is turned on.
    if info.flags & ASCII:
        flags &= ~FULLCASE

    return flags

