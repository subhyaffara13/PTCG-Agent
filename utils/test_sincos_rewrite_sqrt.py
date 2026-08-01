
def test_sincos_rewrite_sqrt():
    # equivalent to testing rewrite(pow)
    for p in [1, 3, 5, 17]:
        for t in [1, 8]:
            n = t*p
            # The vertices `exp(i*pi/n)` of a regular `n`-gon can
            # be expressed by means of nested square roots if and
            # only if `n` is a product of Fermat primes, `p`, and
            # powers of 2, `t'. The code aims to check all vertices
            # not belonging to an `m`-gon for `m < n`(`gcd(i, n) == 1`).
            # For large `n` this makes the test too slow, therefore
            # the vertices are limited to those of index `i < 10`.
            for i in range(1, min((n + 1)//2 + 1, 10)):
                if 1 == gcd(i, n):
                    x = i*pi/n
                    s1 = sin(x).rewrite(sqrt)
                    c1 = cos(x).rewrite(sqrt)
                    assert not s1.has(cos, sin), "fails for %d*pi/%d" % (i, n)
                    assert not c1.has(cos, sin), "fails for %d*pi/%d" % (i, n)
                    assert 1e-3 > abs(sin(x.evalf(5)) - s1.evalf(2)), "fails for %d*pi/%d" % (i, n)
                    assert 1e-3 > abs(cos(x.evalf(5)) - c1.evalf(2)), "fails for %d*pi/%d" % (i, n)
    assert cos(pi/14).rewrite(sqrt) == sqrt(cos(pi/7)/2 + S.Half)
    assert cos(pi*Rational(-15, 2)/11, evaluate=False).rewrite(
        sqrt) == -sqrt(-cos(pi*Rational(4, 11))/2 + S.Half)
    assert cos(Mul(2, pi, S.Half, evaluate=False), evaluate=False).rewrite(
        sqrt) == -1
    e = cos(pi/3/17)  # don't use pi/15 since that is caught at instantiation
    a = (
        -3*sqrt(-sqrt(17) + 17)*sqrt(sqrt(17) + 17)/64 -
        3*sqrt(34)*sqrt(sqrt(17) + 17)/128 - sqrt(sqrt(17) +
        17)*sqrt(-8*sqrt(2)*sqrt(sqrt(17) + 17) - sqrt(2)*sqrt(-sqrt(17) + 17)
        + sqrt(34)*sqrt(-sqrt(17) + 17) + 6*sqrt(17) + 34)/64 - sqrt(-sqrt(17)
        + 17)*sqrt(-8*sqrt(2)*sqrt(sqrt(17) + 17) - sqrt(2)*sqrt(-sqrt(17) +
        17) + sqrt(34)*sqrt(-sqrt(17) + 17) + 6*sqrt(17) + 34)/128 - Rational(1, 32) +
        sqrt(2)*sqrt(-8*sqrt(2)*sqrt(sqrt(17) + 17) - sqrt(2)*sqrt(-sqrt(17) +
        17) + sqrt(34)*sqrt(-sqrt(17) + 17) + 6*sqrt(17) + 34)/64 +
        3*sqrt(2)*sqrt(sqrt(17) + 17)/128 + sqrt(34)*sqrt(-sqrt(17) + 17)/128
        + 13*sqrt(2)*sqrt(-sqrt(17) + 17)/128 + sqrt(17)*sqrt(-sqrt(17) +
        17)*sqrt(-8*sqrt(2)*sqrt(sqrt(17) + 17) - sqrt(2)*sqrt(-sqrt(17) + 17)
        + sqrt(34)*sqrt(-sqrt(17) + 17) + 6*sqrt(17) + 34)/128 + 5*sqrt(17)/32
        + sqrt(3)*sqrt(-sqrt(2)*sqrt(sqrt(17) + 17)*sqrt(sqrt(17)/32 +
        sqrt(2)*sqrt(-sqrt(17) + 17)/32 +
        sqrt(2)*sqrt(-8*sqrt(2)*sqrt(sqrt(17) + 17) - sqrt(2)*sqrt(-sqrt(17) +
        17) + sqrt(34)*sqrt(-sqrt(17) + 17) + 6*sqrt(17) + 34)/32 + Rational(15, 32))/8 -
        5*sqrt(2)*sqrt(sqrt(17)/32 + sqrt(2)*sqrt(-sqrt(17) + 17)/32 +
        sqrt(2)*sqrt(-8*sqrt(2)*sqrt(sqrt(17) + 17) - sqrt(2)*sqrt(-sqrt(17) +
        17) + sqrt(34)*sqrt(-sqrt(17) + 17) + 6*sqrt(17) + 34)/32 +
        Rational(15, 32))*sqrt(-8*sqrt(2)*sqrt(sqrt(17) + 17) - sqrt(2)*sqrt(-sqrt(17) +
        17) + sqrt(34)*sqrt(-sqrt(17) + 17) + 6*sqrt(17) + 34)/64 -
        3*sqrt(2)*sqrt(-sqrt(17) + 17)*sqrt(sqrt(17)/32 +
        sqrt(2)*sqrt(-sqrt(17) + 17)/32 +
        sqrt(2)*sqrt(-8*sqrt(2)*sqrt(sqrt(17) + 17) - sqrt(2)*sqrt(-sqrt(17) +
        17) + sqrt(34)*sqrt(-sqrt(17) + 17) + 6*sqrt(17) + 34)/32 + Rational(15, 32))/32
        + sqrt(34)*sqrt(sqrt(17)/32 + sqrt(2)*sqrt(-sqrt(17) + 17)/32 +
        sqrt(2)*sqrt(-8*sqrt(2)*sqrt(sqrt(17) + 17) - sqrt(2)*sqrt(-sqrt(17) +
        17) + sqrt(34)*sqrt(-sqrt(17) + 17) + 6*sqrt(17) + 34)/32 +
        Rational(15, 32))*sqrt(-8*sqrt(2)*sqrt(sqrt(17) + 17) - sqrt(2)*sqrt(-sqrt(17) +
        17) + sqrt(34)*sqrt(-sqrt(17) + 17) + 6*sqrt(17) + 34)/64 +
        sqrt(sqrt(17)/32 + sqrt(2)*sqrt(-sqrt(17) + 17)/32 +
        sqrt(2)*sqrt(-8*sqrt(2)*sqrt(sqrt(17) + 17) - sqrt(2)*sqrt(-sqrt(17) +
        17) + sqrt(34)*sqrt(-sqrt(17) + 17) + 6*sqrt(17) + 34)/32 + Rational(15, 32))/2 +
        S.Half + sqrt(-sqrt(17) + 17)*sqrt(sqrt(17)/32 + sqrt(2)*sqrt(-sqrt(17) +
        17)/32 + sqrt(2)*sqrt(-8*sqrt(2)*sqrt(sqrt(17) + 17) -
        sqrt(2)*sqrt(-sqrt(17) + 17) + sqrt(34)*sqrt(-sqrt(17) + 17) +
        6*sqrt(17) + 34)/32 + Rational(15, 32))*sqrt(-8*sqrt(2)*sqrt(sqrt(17) + 17) -
        sqrt(2)*sqrt(-sqrt(17) + 17) + sqrt(34)*sqrt(-sqrt(17) + 17) +
        6*sqrt(17) + 34)/32 + sqrt(34)*sqrt(-sqrt(17) + 17)*sqrt(sqrt(17)/32 +
        sqrt(2)*sqrt(-sqrt(17) + 17)/32 +
        sqrt(2)*sqrt(-8*sqrt(2)*sqrt(sqrt(17) + 17) - sqrt(2)*sqrt(-sqrt(17) +
        17) + sqrt(34)*sqrt(-sqrt(17) + 17) + 6*sqrt(17) + 34)/32 +
        Rational(15, 32))/32)/2)
    assert e.rewrite(sqrt) == a
    assert e.n() == a.n()
    # coverage of fermatCoords: multiplicity > 1; the following could be
    # different but that portion of the code should be tested in some way
    assert cos(pi/9/17).rewrite(sqrt) == \
        sin(pi/9)*sin(pi*Rational(2, 17)) + cos(pi/9)*cos(pi*Rational(2, 17))

