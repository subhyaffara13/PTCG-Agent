
def test_sympy__series__sequences__RecursiveSeq():
    from sympy.series.sequences import RecursiveSeq
    y = Function("y")
    n = symbols("n")
    assert _test_args(RecursiveSeq(y(n - 1) + y(n - 2), y(n), n, (0, 1)))
    assert _test_args(RecursiveSeq(y(n - 1) + y(n - 2), y(n), n))

