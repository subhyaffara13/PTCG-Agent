
def fuzzy_nand(args):
    """Return False if all args are True, True if they are all False,
    else None."""
    return fuzzy_not(fuzzy_and(args))

