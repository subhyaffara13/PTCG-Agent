
def test_trigsimp_groebner():
    from sympy.simplify.trigsimp import trigsimp_groebner

    c = cos(x)
    s = sin(x)
    ex = (4*s*c + 12*s + 5*c**3 + 21*c**2 + 23*c + 15)/(
        -s*c**2 + 2*s*c + 15*s + 7*c**3 + 31*c**2 + 37*c + 21)
    resnum = (5*s - 5*c + 1)
    resdenom = (8*s - 6*c)
    results = [resnum/resdenom, (-resnum)/(-resdenom)]
    assert trigsimp_groebner(ex) in results
    assert trigsimp_groebner(s/c, hints=[tan]) == tan(x)
    assert trigsimp_groebner(c*s) == c*s
    assert trigsimp((-s + 1)/c + c/(-s + 1),
                    method='groebner') == 2/c
    assert trigsimp((-s + 1)/c + c/(-s + 1),
                    method='groebner', polynomial=True) == 2/c

    # Test quick=False works
    assert trigsimp_groebner(ex, hints=[2]) in results
    assert trigsimp_groebner(ex, hints=[int(2)]) in results

    # test "I"
    assert trigsimp_groebner(sin(I*x)/cos(I*x), hints=[tanh]) == I*tanh(x)

    # test hyperbolic / sums
    assert trigsimp_groebner((tanh(x)+tanh(y))/(1+tanh(x)*tanh(y)),
                             hints=[(tanh, x, y)]) == tanh(x + y)

