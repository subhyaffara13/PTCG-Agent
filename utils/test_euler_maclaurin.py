
def test_euler_maclaurin():
    # Exact polynomial sums with E-M
    def check_exact(f, a, b, m, n):
        A = Sum(f, (k, a, b))
        s, e = A.euler_maclaurin(m, n)
        assert (e == 0) and (s.expand() == A.doit())
    check_exact(k**4, a, b, 0, 2)
    check_exact(k**4 + 2*k, a, b, 1, 2)
    check_exact(k**4 + k**2, a, b, 1, 5)
    check_exact(k**5, 2, 6, 1, 2)
    check_exact(k**5, 2, 6, 1, 3)
    assert Sum(x-1, (x, 0, 2)).euler_maclaurin(m=30, n=30, eps=2**-15) == (0, 0)
    # Not exact
    assert Sum(k**6, (k, a, b)).euler_maclaurin(0, 2)[1] != 0
    # Numerical test
    for mi, ni in [(2, 4), (2, 20), (10, 20), (18, 20)]:
        A = Sum(1/k**3, (k, 1, oo))
        s, e = A.euler_maclaurin(mi, ni)
        assert abs((s - zeta(3)).evalf()) < e.evalf()

    raises(ValueError, lambda: Sum(1, (x, 0, 1), (k, 0, 1)).euler_maclaurin())

