
def remainder_integer(a, b):
    # NOTE: a % b matches C division, not floor division
    remainder = a % b
    return tl.where((remainder != 0) & ((a < 0) != (b < 0)), remainder + b, remainder)

