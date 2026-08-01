
def test_imps_errors():
    # Test errors that implemented functions can return, and still be able to
    # form expressions.
    # See: https://github.com/sympy/sympy/issues/10810
    #
    # XXX: Removed AttributeError here. This test was added due to issue 10810
    # but that issue was about ValueError. It doesn't seem reasonable to
    # "support" catching AttributeError in the same context...
    for val, error_class in product((0, 0., 2, 2.0), (TypeError, ValueError)):

        def myfunc(a):
            if a == 0:
                raise error_class
            return 1

        f = implemented_function('f', myfunc)
        expr = f(val)
        assert expr == f(val)

