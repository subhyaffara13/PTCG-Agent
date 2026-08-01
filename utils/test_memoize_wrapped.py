
def test_memoize_wrapped():

    def foo():
        """
        Docstring
        """
        pass
    memoized_foo = memoize(foo)
    assert memoized_foo.__wrapped__ is foo

