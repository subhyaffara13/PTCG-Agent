
def children(obj, objtype, depth=1, ignore=()): #XXX: objtype=object ?
    """Find the chain of referrers for obj. Chain will start with obj.

    objtype: an object type or tuple of types to search for
    depth: search depth (e.g. depth=2 is 'grandchildren')
    ignore: an object or tuple of objects to ignore in the search

    NOTE: a common thing to ignore is all globals, 'ignore=(globals(),)'

    NOTE: repeated calls may yield different results, as python stores
    the last value in the special variable '_'; thus, it is often good
    to execute something to replace '_' (e.g. >>> 1+1).
    """
    edge_func = gc.get_referrers # looking for back_refs, not refs
    predicate = lambda x: isinstance(x, objtype) # looking for child type
   #if objtype is None: predicate = lambda x: True #XXX: in obj.mro() ?
    ignore = (ignore,) if not hasattr(ignore, '__len__') else ignore
    ignore = (id(obj) for obj in ignore)
    chain = find_chain(obj, predicate, edge_func, depth, ignore)
    #XXX: should pop off obj... ?
    return chain

