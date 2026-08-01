
def xfail_inherited_tests(tests):
    """
    Given a list of test names which are defined by a superclass of the
    class this decorates, mark them as expected failure.  This is useful
    if you are doing poor man's parameterized tests by subclassing a generic
    test class.
    """
    def deco(cls):
        for t in tests:
            # NB: expectedFailure operates by mutating the method in question,
            # which is why you have to copy the function first
            setattr(cls, t, unittest.expectedFailure(copy_func(getattr(cls, t))))
        return cls
    return deco

