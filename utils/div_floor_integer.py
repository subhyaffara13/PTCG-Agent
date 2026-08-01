
def div_floor_integer(a, b):
    # NOTE: a // b is C division, but we want floor division
    # Based on c10::div_floor_integer
    quot = a // b
    remainder = a % b
    fixed = tl.where(remainder != 0, quot - 1, quot)
    return tl.where((a < 0) != (b < 0), fixed, quot)

