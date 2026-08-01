
def test_sympy__series__sequences__SeqExprOp():
    from sympy.series.sequences import SeqExprOp, sequence
    s1 = sequence((1, 2, 3))
    s2 = sequence(x**2)
    assert _test_args(SeqExprOp(s1, s2))

