
def is_actually_fuzzy(constraints):
    "Checks whether a fuzzy constraint is actually fuzzy."
    if constraints.get("e") == (0, 0):
        return False

    if (constraints.get("s"), constraints.get("i"), constraints.get("d")) == ((0, 0), (0, 0), (0, 0)):
        return False

    return True

