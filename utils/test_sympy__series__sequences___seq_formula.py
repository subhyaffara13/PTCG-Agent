
def test_sympy__series__sequences__SeqFormula():
    from sympy.series.sequences import SeqFormula
    assert _test_args(SeqFormula(x**2, (0, 10)))

