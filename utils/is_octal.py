
def is_octal(string):
    "Checks whether a string is octal."
    return all(ch in OCT_DIGITS for ch in string)

