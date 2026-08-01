
def test_competing_ambiguous():
    test_namespace = {}
    dispatch = partial(orig_dispatch, namespace=test_namespace)

    @dispatch(A, C)
    def f(x, y): # noqa:F811
        return 2

    with warns(AmbiguityWarning, test_stacklevel=False):
        @dispatch(C, A) # noqa:F811
        def f(x, y): # noqa:F811
            return 2

    assert f(A(), C()) == f(C(), A()) == 2

