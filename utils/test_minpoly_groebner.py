
def test_minpoly_groebner():
    assert _minpoly_groebner(S(2)/3, x, Poly) == 3*x - 2
    assert _minpoly_groebner(
        (sqrt(2) + 3)*(sqrt(2) + 1), x, Poly) == x**2 - 10*x - 7
    assert _minpoly_groebner((sqrt(2) + 3)**(S(1)/3)*(sqrt(2) + 1)**(S(1)/3),
                             x, Poly) == x**6 - 10*x**3 - 7
    assert _minpoly_groebner((sqrt(2) + 3)**(-S(1)/3)*(sqrt(2) + 1)**(S(1)/3),
                             x, Poly) == 7*x**6 - 2*x**3 - 1
    raises(NotAlgebraic, lambda: _minpoly_groebner(pi**2, x, Poly))

