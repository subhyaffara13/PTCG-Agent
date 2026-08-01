
def firwin_signature(numtaps, cutoff, *args, **kwds):
    if isinstance(cutoff, int | float):
        xp = np_compat
    else:
        xp = array_namespace(cutoff)
    return xp

