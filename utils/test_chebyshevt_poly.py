
def test_chebyshevt_poly():
    raises(ValueError, lambda: chebyshevt_poly(-1, x))

    assert chebyshevt_poly(1, x, polys=True) == Poly(x)

    assert chebyshevt_poly(0, x) == 1
    assert chebyshevt_poly(1, x) == x
    assert chebyshevt_poly(2, x) == 2*x**2 - 1
    assert chebyshevt_poly(3, x) == 4*x**3 - 3*x
    assert chebyshevt_poly(4, x) == 8*x**4 - 8*x**2 + 1
    assert chebyshevt_poly(5, x) == 16*x**5 - 20*x**3 + 5*x
    assert chebyshevt_poly(6, x) == 32*x**6 - 48*x**4 + 18*x**2 - 1
    assert chebyshevt_poly(75, x) == (2*chebyshevt_poly(37, x)*chebyshevt_poly(38, x) - x).expand()
    assert chebyshevt_poly(100, x) == (2*chebyshevt_poly(50, x)**2 - 1).expand()

    assert chebyshevt_poly(1).dummy_eq(x)
    assert chebyshevt_poly(1, polys=True) == Poly(x)

