
def parents(obj, objtype, depth=1, ignore=()): #XXX: objtype=object ?
    """Find the chain of referents for obj. Chain will end with obj.

    objtype: an object type or tuple of types to search for
    depth: search depth (e.g. depth=2 is 'grandparents')
    ignore: an object or tuple of objects to ignore in the search
    """
    edge_func = gc.get_referents # looking for refs, not back_refs
    predicate = lambda x: isinstance(x, objtype) # looking for parent type
   #if objtype is None: predicate = lambda x: True #XXX: in obj.mro() ?
    ignore = (ignore,) if not hasattr(ignore, '__len__') else ignore
    ignore = (id(obj) for obj in ignore)
    chain = find_chain(obj, predicate, edge_func, depth)[::-1]
    #XXX: should pop off obj... ?
    return chain

