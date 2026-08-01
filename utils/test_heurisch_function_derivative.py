
def test_heurisch_function_derivative():
    # TODO: it looks like this used to work just by coincindence and
    # thanks to sloppy implementation. Investigate why this used to
    # work at all and if support for this can be restored.

    df = diff(f(x), x)

    assert heurisch(f(x)*df, x) == f(x)**2/2
    assert heurisch(f(x)**2*df, x) == f(x)**3/3
    assert heurisch(df/f(x), x) == log(f(x))

