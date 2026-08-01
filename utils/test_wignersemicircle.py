
def test_wignersemicircle():
    R = Symbol("R", positive=True)

    X = WignerSemicircle('x', R)
    assert pspace(X).domain.set == Interval(-R, R)
    assert density(X)(x) == 2*sqrt(-x**2 + R**2)/(pi*R**2)
    assert E(X) == 0


    #Tests ChiNoncentralDistribution
    assert characteristic_function(X)(x) == \
           Piecewise((2*besselj(1, R*x)/(R*x), Ne(x, 0)), (1, True))

