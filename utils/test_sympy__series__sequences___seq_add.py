
def test_sympy__series__sequences__SeqAdd():
    from sympy.series.sequences import SeqAdd, sequence
    s1 = sequence((1, 2, 3))
    s2 = sequence(x**2)
    assert _test_args(SeqAdd(s1, s2))

