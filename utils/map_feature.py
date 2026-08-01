
def mapFeature(sym, mapping):
    # Features are referenced by index according the spec.  So, if symbol is an
    # integer, use it directly.  Otherwise look up in the map if provided.
    try:
        idx = int(sym)
    except ValueError:
        try:
            idx = mapping[sym]
        except KeyError:
            raise FeatureNotFoundError(sym)
    return idx

