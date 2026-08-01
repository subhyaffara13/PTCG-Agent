
def test_exponential_complex():
    n = Dummy('n')

    assert dumeq(solveset_complex(2**x + 4**x, x),imageset(
        Lambda(n, I*(2*n*pi + pi)/log(2)), S.Integers))
    assert solveset_complex(x**z*y**z - 2, z) == FiniteSet(
        log(2)/(log(x) + log(y)))
    assert dumeq(solveset_complex(4**(x/2) - 2**(x/3), x), imageset(
        Lambda(n, 3*n*I*pi/log(2)), S.Integers))
    assert dumeq(solveset(2**x + 32, x), imageset(
        Lambda(n, (I*(2*n*pi + pi) + 5*log(2))/log(2)), S.Integers))

    eq = (2**exp(y**2/x) + 2)/(x**2 + 15)
    a = sqrt(x)*sqrt(-log(log(2)) + log(log(2) + 2*n*I*pi))
    assert solveset_complex(eq, y) == FiniteSet(-a, a)

    union1 = imageset(Lambda(n, I*(2*n*pi - pi*Rational(2, 3))/log(2)), S.Integers)
    union2 = imageset(Lambda(n, I*(2*n*pi + pi*Rational(2, 3))/log(2)), S.Integers)
    assert dumeq(solveset(2**x + 4**x + 8**x, x), Union(union1, union2))

    eq = 4**(x + 1) + 4**(x + 2) + 4**(x - 1) - 3**(x + 2) - 3**(x + 3)
    res = solveset(eq, x)
    num = 2*n*I*pi - 4*log(2) + 2*log(3)
    den = -2*log(2) + log(3)
    ans = imageset(Lambda(n, num/den), S.Integers)
    assert dumeq(res, ans)

