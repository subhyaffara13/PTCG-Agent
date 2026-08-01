
def test_continuous_domain_acot():
    acot_cont = Piecewise((pi+acot(x), x<0), (acot(x), True))
    assert continuous_domain(acot_cont, x, S.Reals) == S.Reals

