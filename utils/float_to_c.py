
def float_to_c(x: float) -> str:
    """Return C literal representation of a float value."""
    s = str(x)
    if s == "inf":
        return "INFINITY"
    elif s == "-inf":
        return "-INFINITY"
    elif s == "nan":
        return "NAN"
    return s

