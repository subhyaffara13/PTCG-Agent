
def test_DiscreteRV():
    p = S(1)/2
    x = Symbol('x', integer=True, positive=True)
    pdf = p*(1 - p)**(x - 1) # pdf of Geometric Distribution
    D = DiscreteRV(x, pdf, set=S.Naturals, check=True)
    assert E(D) == E(Geometric('G', S(1)/2)) == 2
    assert P(D > 3) == S(1)/8
    assert D.pspace.domain.set == S.Naturals
    raises(ValueError, lambda: DiscreteRV(x, x, FiniteSet(*range(4)), check=True))

    # purposeful invalid pmf but it should not raise since check=False
    # see test_drv_types.test_ContinuousRV for explanation
    X = DiscreteRV(x, 1/x, S.Naturals)
    assert P(X < 2) == 1
    assert E(X) == oo

