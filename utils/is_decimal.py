
def is_decimal(string):
    "Checks whether a string is decimal."
    return all(ch in DIGITS for ch in string)

