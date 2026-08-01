
def is_cased_i(info, char):
    "Checks whether a character is cased."
    return len(_regex.get_all_cases(info.flags, char)) > 1

