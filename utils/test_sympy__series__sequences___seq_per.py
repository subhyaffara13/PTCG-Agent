
def test_sympy__series__sequences__SeqPer():
    from sympy.series.sequences import SeqPer
    assert _test_args(SeqPer((1, 2, 3), (0, 10)))

