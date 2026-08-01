
def mapLookup(sym, mapping):
    # Lookups are addressed by name.  So resolved them using a map if available.
    # Fallback to parsing as lookup index if a map isn't provided.
    if mapping is not None:
        try:
            idx = mapping[sym]
        except KeyError:
            raise LookupNotFoundError(sym)
    else:
        idx = int(sym)
    return idx

