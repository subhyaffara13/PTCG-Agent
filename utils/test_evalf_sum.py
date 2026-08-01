
def test_evalf_sum():
    assert Sum(n,(n,1,2)).evalf() == 3.
    assert Sum(n,(n,1,2)).doit().evalf() == 3.
    # the next test should return instantly
    assert Sum(1/n,(n,1,2)).evalf() == 1.5

    # issue 8219
    assert Sum(E/factorial(n), (n, 0, oo)).evalf() == (E*E).evalf()
    # issue 8254
    assert Sum(2**n*n/factorial(n), (n, 0, oo)).evalf() == (2*E*E).evalf()
    # issue 8411
    s = Sum(1/x**2, (x, 100, oo))
    assert s.n() == s.doit().n()

