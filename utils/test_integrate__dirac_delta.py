
def test_integrate_DiracDelta():
    # This is here to check that deltaintegrate is being called, but also
    # to test definite integrals. More tests are in test_deltafunctions.py
    assert integrate(DiracDelta(x) * f(x), (x, -oo, oo)) == f(0)
    assert integrate(DiracDelta(x)**2, (x, -oo, oo)) == DiracDelta(0)
    # issue 4522
    assert integrate(integrate((4 - 4*x + x*y - 4*y) * \
        DiracDelta(x)*DiracDelta(y - 1), (x, 0, 1)), (y, 0, 1)) == 0
    # issue 5729
    p = exp(-(x**2 + y**2))/pi
    assert integrate(p*DiracDelta(x - 10*y), (x, -oo, oo), (y, -oo, oo)) == \
        integrate(p*DiracDelta(x - 10*y), (y, -oo, oo), (x, -oo, oo)) == \
        integrate(p*DiracDelta(10*x - y), (x, -oo, oo), (y, -oo, oo)) == \
        integrate(p*DiracDelta(10*x - y), (y, -oo, oo), (x, -oo, oo)) == \
        1/sqrt(101*pi)

