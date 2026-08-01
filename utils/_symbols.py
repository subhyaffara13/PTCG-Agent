
def _symbols(name, n):
    """get vector of symbols local to this module"""
    try:
        lsyms = _symbols_cache[name]
    except KeyError:
        lsyms = []
        _symbols_cache[name] = lsyms

    while len(lsyms) < n:
        lsyms.append( Dummy('%s%i' % (name, len(lsyms))) )

    return lsyms[:n]

