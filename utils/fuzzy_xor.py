
def fuzzy_xor(args):
    """Return None if any element of args is not True or False, else
    True (if there are an odd number of True elements), else False."""
    t = 0
    for a in args:
        ai = fuzzy_bool(a)
        if ai:
            t += 1
        elif ai is None:
            return
    return t % 2 == 1

