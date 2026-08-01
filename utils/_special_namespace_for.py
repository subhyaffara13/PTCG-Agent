
def _special_namespace_for(xp):
    spx = scipy_namespace_for(xp)
    return getattr(spx, "special", None)

