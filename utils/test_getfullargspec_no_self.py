
def test_getfullargspec_no_self():
    p = MapWrapper(1)
    argspec = getfullargspec_no_self(p.__init__)
    assert_equal(argspec, FullArgSpec(['pool'], None, None, (1,), [],
                                      None, {}))
    argspec = getfullargspec_no_self(p.__call__)
    assert_equal(argspec, FullArgSpec(['func', 'iterable'], None, None, None,
                                      [], None, {}))

    class _rv_generic:
        def _rvs(self, a, b=2, c=3, *args, size=None, **kwargs):
            return None

    rv_obj = _rv_generic()
    argspec = getfullargspec_no_self(rv_obj._rvs)
    assert_equal(argspec, FullArgSpec(['a', 'b', 'c'], 'args', 'kwargs',
                                      (2, 3), ['size'], {'size': None}, {}))

