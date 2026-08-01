
def test_diofantissue_294():
    f = y(n) - y(n - 1) - 2*y(n - 2) - 2*n
    assert rsolve(f, y(n)) == (-1)**n*C0 + 2**n*C1 - n - Rational(5, 2)
    # issue sympy/sympy#11261
    assert rsolve(f, y(n), {y(0): -1, y(1): 1}) == (-(-1)**n/2 + 2*2**n -
                                                    n - Rational(5, 2))
    # issue sympy/sympy#7055
    assert rsolve(-2*y(n) + y(n + 1) + n - 1, y(n)) == 2**n*C0 + n

