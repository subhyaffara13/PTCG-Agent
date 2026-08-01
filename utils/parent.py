
def parent(obj, objtype, ignore=()):
    """
>>> listiter = iter([4,5,6,7])
>>> obj = parent(listiter, list)
>>> obj == [4,5,6,7]  # actually 'is', but don't have handle any longer
True

NOTE: objtype can be a single type (e.g. int or list) or a tuple of types.

WARNING: if obj is a sequence (e.g. list), may produce unexpected results.
Parent finds *one* parent (e.g. the last member of the sequence).
    """
    depth = 1 #XXX: always looking for the parent (only, right?)
    chain = parents(obj, objtype, depth, ignore)
    parent = chain.pop()
    if parent is obj:
        return None
    return parent

