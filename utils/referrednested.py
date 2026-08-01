
def referrednested(func, recurse=True): #XXX: return dict of {__name__: obj} ?
    """get functions defined inside of func (e.g. inner functions in a closure)

    NOTE: results may differ if the function has been executed or not.
    If len(nestedcode(func)) > len(referrednested(func)), try calling func().
    If possible, python builds code objects, but delays building functions
    until func() is called.
    """
    import gc
    funcs = set()
    # get the code objects, and try to track down by referrence
    for co in nestedcode(func, recurse):
        # look for function objects that refer to the code object
        for obj in gc.get_referrers(co):
            # get methods
            _ = getattr(obj, '__func__', None) # ismethod
            if getattr(_, '__code__', None) is co: funcs.add(obj)
            # get functions
            elif getattr(obj, '__code__', None) is co: funcs.add(obj)
            # get frame objects
            elif getattr(obj, 'f_code', None) is co: funcs.add(obj)
            # get code objects
            elif hasattr(obj, 'co_code') and obj is co: funcs.add(obj)
#     frameobjs => func.__code__.co_varnames not in func.__code__.co_cellvars
#     funcobjs => func.__code__.co_cellvars not in func.__code__.co_varnames
#     frameobjs are not found, however funcobjs are...
#     (see: test_mixins.quad ... and test_mixins.wtf)
#     after execution, code objects get compiled, and then may be found by gc
    return list(funcs)

