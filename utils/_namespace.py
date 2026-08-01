
def _namespace(obj):
    """_namespace(obj); return namespace hierarchy (as a list of names)
    for the given object.  For an instance, find the class hierarchy.

    For example:

    >>> from functools import partial
    >>> p = partial(int, base=2)
    >>> _namespace(p)
    [\'functools\', \'partial\']
    """
    # mostly for functions and modules and such
    #FIXME: 'wrong' for decorators and curried functions
    try: #XXX: needs some work and testing on different types
        module = qual = str(getmodule(obj)).split()[1].strip('>').strip('"').strip("'")
        qual = qual.split('.')
        if ismodule(obj):
            return qual
        # get name of a lambda, function, etc
        name = getname(obj) or obj.__name__ # failing, raise AttributeError
        # check special cases (NoneType, ...)
        if module in ['builtins','__builtin__']: # BuiltinFunctionType
            if _intypes(name): return ['types'] + [name]
        return qual + [name] #XXX: can be wrong for some aliased objects
    except Exception: pass
    # special case: numpy.inf and numpy.nan (we don't want them as floats)
    if str(obj) in ['inf','nan','Inf','NaN']: # is more, but are they needed?
        return ['numpy'] + [str(obj)]
    # mostly for classes and class instances and such
    module = getattr(obj.__class__, '__module__', None)
    qual = str(obj.__class__)
    try: qual = qual[qual.index("'")+1:-2]
    except ValueError: pass # str(obj.__class__) made the 'try' unnecessary
    qual = qual.split(".")
    if module in ['builtins','__builtin__']:
        # check special cases (NoneType, Ellipsis, ...)
        if qual[-1] == 'ellipsis': qual[-1] = 'EllipsisType'
        if _intypes(qual[-1]): module = 'types' #XXX: BuiltinFunctionType
        qual = [module] + qual
    return qual


def _namespace(xp):
    """A shim for the `device` arg of `np.asarray(x, device=device)` and acos/arccos.

    Will be able to replace with `np_compat if xp is None else xp` when we drop
    support for numpy 1.x and cupy 13.x
    """
    return np_compat if xp is None else array_namespace(xp.empty(0))

