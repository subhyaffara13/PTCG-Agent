
def make_character(info, value, in_set=False):
    "Makes a character literal."
    if in_set:
        # A character set is built case-sensitively.
        return Character(value)

    return Character(value, case_flags=make_case_flags(info))

