
def setReference(mapper, mapping, sym, setter, collection, key):
    try:
        mapped = mapper(sym, mapping)
    except ReferenceNotFoundError as e:
        try:
            if mapping is not None:
                mapping.addDeferredMapping(
                    lambda ref: setter(collection, key, ref), sym, e
                )
                return
        except AttributeError:
            pass
        raise
    setter(collection, key, mapped)

