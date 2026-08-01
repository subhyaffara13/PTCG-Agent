
def _check_firstset(info, reverse, fs):
    "Checks the firstset for the pattern."
    if not fs or None in fs:
        return None

    # If we ignore the case, for simplicity we won't build a firstset.
    members = set()
    case_flags = NOCASE
    for i in fs:
        if isinstance(i, Character) and not i.positive:
            return None

#        if i.case_flags:
#            if isinstance(i, Character):
#                if is_cased_i(info, i.value):
#                    return []
#            elif isinstance(i, SetBase):
#                return []
        case_flags |= i.case_flags
        members.add(i.with_flags(case_flags=NOCASE))

    if case_flags == (FULLCASE | IGNORECASE):
        return None

    # Build the firstset.
    fs = SetUnion(info, list(members), case_flags=case_flags & ~FULLCASE,
      zerowidth=True)
    fs = fs.optimise(info, reverse, in_set=True)

    return fs

