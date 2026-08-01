
def _same(measure, tol=0):
    vals = set(measure.values())
    if (max(vals) - min(vals)) <= tol:
        return True
    return False

