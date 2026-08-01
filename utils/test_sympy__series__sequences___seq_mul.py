
def test_sympy__series__sequences__SeqMul():
    from sympy.series.sequences import SeqMul, sequence
    s1 = sequence((1, 2, 3))
    s2 = sequence(x**2)
    assert _test_args(SeqMul(s1, s2))

