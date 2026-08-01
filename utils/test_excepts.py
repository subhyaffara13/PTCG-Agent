
def test_excepts():
    # These are descriptors, make sure this works correctly.
    assert excepts.__name__ == 'excepts'
    # in Python < 3.13 the second line is indented, in 3.13+
    # it is not, strip all lines to fudge it
    testlines = "\n".join(line.strip() for line in excepts.__doc__.splitlines())
    assert (
        'A wrapper around a function to catch exceptions and\n'
        'dispatch to a handler.\n'
    ) in testlines

    def idx(a):
        """idx docstring
        """
        return [1, 2].index(a)

    def handler(e):
        """handler docstring
        """
        assert isinstance(e, ValueError)
        return -1

    excepting = excepts(ValueError, idx, handler)
    assert excepting(1) == 0
    assert excepting(2) == 1
    assert excepting(3) == -1

    assert excepting.__name__ == 'idx_excepting_ValueError'
    assert 'idx docstring' in excepting.__doc__
    assert 'ValueError' in excepting.__doc__
    assert 'handler docstring' in excepting.__doc__

    def getzero(a):
        """getzero docstring
        """
        return a[0]

    excepting = excepts((IndexError, KeyError), getzero)
    assert excepting([]) is None
    assert excepting([1]) == 1
    assert excepting({}) is None
    assert excepting({0: 1}) == 1

    assert excepting.__name__ == 'getzero_excepting_IndexError_or_KeyError'
    assert 'getzero docstring' in excepting.__doc__
    assert 'return_none' in excepting.__doc__
    assert 'Returns None' in excepting.__doc__

    def raise_(a):
        """A function that raises an instance of the exception type given.
        """
        raise a()

    excepting = excepts((ValueError, KeyError), raise_)
    assert excepting(ValueError) is None
    assert excepting(KeyError) is None
    assert raises(TypeError, lambda: excepting(TypeError))
    assert raises(NotImplementedError, lambda: excepting(NotImplementedError))

    excepting = excepts(object(), object(), object())
    assert excepting.__name__ == 'excepting'
    assert excepting.__doc__ == excepts.__doc__

