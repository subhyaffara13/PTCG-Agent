
def test_longdouble_operators_with_obj(sctype, op):
    # This is/used to be tricky, because NumPy generally falls back to
    # using the ufunc via `np.asarray()`, this effectively might do:
    # longdouble + None
    #   -> asarray(longdouble) + np.array(None, dtype=object)
    #   -> asarray(longdouble).astype(object) + np.array(None, dtype=object)
    # And after getting the scalars in the inner loop:
    #   -> longdouble + None
    #
    # That would recurse infinitely.  Other scalars return the python object
    # on cast, so this type of things works OK.
    #
    # As of NumPy 2.1, this has been consolidated into the np.generic binops
    # and now checks `.item()`.  That also allows the below path to work now.
    try:
        op(sctype(3), None)
    except TypeError:
        pass
    try:
        op(None, sctype(3))
    except TypeError:
        pass

