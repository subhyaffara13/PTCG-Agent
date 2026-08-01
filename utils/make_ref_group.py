
def make_ref_group(info, name, position):
    "Makes a group reference."
    return RefGroup(info, name, position, case_flags=make_case_flags(info))

