
def test_sympy__functions__elementary__piecewise__Piecewise():
    from sympy.functions.elementary.piecewise import Piecewise
    assert _test_args(Piecewise((1, x >= 0), (0, True)))

