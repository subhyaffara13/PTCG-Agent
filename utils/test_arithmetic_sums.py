
def test_arithmetic_sums():
    assert summation(1, (n, a, b)) == b - a + 1
    assert Sum(S.NaN, (n, a, b)) is S.NaN
    assert Sum(x, (n, a, a)).doit() == x
    assert Sum(x, (x, a, a)).doit() == a
    assert Sum(x, (n, 1, a)).doit() == a*x
    assert Sum(x, (x, Range(1, 11))).doit() == 55
    assert Sum(x, (x, Range(1, 11, 2))).doit() == 25
    assert Sum(x, (x, Range(1, 10, 2))) == Sum(x, (x, Range(9, 0, -2)))
    lo, hi = 1, 2
    s1 = Sum(n, (n, lo, hi))
    s2 = Sum(n, (n, hi, lo))
    assert s1 != s2
    assert s1.doit() == 3 and s2.doit() == 0
    lo, hi = x, x + 1
    s1 = Sum(n, (n, lo, hi))
    s2 = Sum(n, (n, hi, lo))
    assert s1 != s2
    assert s1.doit() == 2*x + 1 and s2.doit() == 0
    assert Sum(Integral(x, (x, 1, y)) + x, (x, 1, 2)).doit() == \
        y**2 + 2
    assert summation(1, (n, 1, 10)) == 10
    assert summation(2*n, (n, 0, 10**10)) == 100000000010000000000
    assert summation(4*n*m, (n, a, 1), (m, 1, d)).expand() == \
        2*d + 2*d**2 + a*d + a*d**2 - d*a**2 - a**2*d**2
    assert summation(cos(n), (n, -2, 1)) == cos(-2) + cos(-1) + cos(0) + cos(1)
    assert summation(cos(n), (n, x, x + 2)) == cos(x) + cos(x + 1) + cos(x + 2)
    assert isinstance(summation(cos(n), (n, x, x + S.Half)), Sum)
    assert summation(k, (k, 0, oo)) is oo
    assert summation(k, (k, Range(1, 11))) == 55

