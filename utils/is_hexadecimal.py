
def is_hexadecimal(string):
    "Checks whether a string is hexadecimal."
    return all(ch in HEX_DIGITS for ch in string)

