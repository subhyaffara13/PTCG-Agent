
def _ntos(n):
    # %f likes to add unnecessary 0's, %g isn't consistent about # decimals
    return ("%.3f" % n).rstrip("0").rstrip(".")

