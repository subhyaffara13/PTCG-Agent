import copy

def pickles(obj,exact=False,safe=False,**kwds):
    """
    Quick check if object pickles with dill.

    If *exact=True* then an equality test is done to check if the reconstructed
    object matches the original object.

    If *safe=True* then any exception will raised in copy signal that the
    object is not picklable, otherwise only pickling errors will be trapped.

    Additional keyword arguments are as :func:`dumps` and :func:`loads`.
    """
    if safe: exceptions = (Exception,) # RuntimeError, ValueError
    else:
        exceptions = (TypeError, AssertionError, NotImplementedError, PicklingError, UnpicklingError)
    try:
        pik = copy(obj, **kwds)
        #FIXME: should check types match first, then check content if "exact"
        try:
            #FIXME: should be "(pik == obj).all()" for numpy comparison, though that'll fail if shapes differ
            result = bool(pik.all() == obj.all())
        except (AttributeError, TypeError):
            warnings.filterwarnings('ignore') #FIXME: be specific
            result = pik == obj
            if warnings.filters: del warnings.filters[0]
        if hasattr(result, 'toarray'): # for unusual types like sparse matrix
            result = result.toarray().all()
        if result: return True
        if not exact:
            result = type(pik) == type(obj)
            if result: return result
            # class instances might have been dumped with byref=False
            return repr(type(pik)) == repr(type(obj)) #XXX: InstanceType?
        return False
    except exceptions:
        return False


def pickles(name, exact=False, verbose=True):
    """quick check if object pickles with dill"""
    obj = objects[name]
    try:
        pik = pickle.loads(pickle.dumps(obj))
        if exact:
            try:
                assert pik == obj
            except AssertionError:
                assert type(obj) == type(pik)
                if verbose: print ("weak: %s %s" % (name, type(obj)))
        else:
            assert type(obj) == type(pik)
    except Exception:
        if verbose: print ("fails: %s %s" % (name, type(obj)))

