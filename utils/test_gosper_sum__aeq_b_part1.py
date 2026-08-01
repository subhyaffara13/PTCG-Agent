
def test_gosper_sum_AeqB_part1():
    f1a = n**4
    f1b = n**3*2**n
    f1c = 1/(n**2 + sqrt(5)*n - 1)
    f1d = n**4*4**n/binomial(2*n, n)
    f1e = factorial(3*n)/(factorial(n)*factorial(n + 1)*factorial(n + 2)*27**n)
    f1f = binomial(2*n, n)**2/((n + 1)*4**(2*n))
    f1g = (4*n - 1)*binomial(2*n, n)**2/((2*n - 1)**2*4**(2*n))
    f1h = n*factorial(n - S.Half)**2/factorial(n + 1)**2

    g1a = m*(m + 1)*(2*m + 1)*(3*m**2 + 3*m - 1)/30
    g1b = 26 + 2**(m + 1)*(m**3 - 3*m**2 + 9*m - 13)
    g1c = (m + 1)*(m*(m**2 - 7*m + 3)*sqrt(5) - (
        3*m**3 - 7*m**2 + 19*m - 6))/(2*m**3*sqrt(5) + m**4 + 5*m**2 - 1)/6
    g1d = Rational(-2, 231) + 2*4**m*(m + 1)*(63*m**4 + 112*m**3 + 18*m**2 -
             22*m + 3)/(693*binomial(2*m, m))
    g1e = Rational(-9, 2) + (81*m**2 + 261*m + 200)*factorial(
        3*m + 2)/(40*27**m*factorial(m)*factorial(m + 1)*factorial(m + 2))
    g1f = (2*m + 1)**2*binomial(2*m, m)**2/(4**(2*m)*(m + 1))
    g1g = -binomial(2*m, m)**2/4**(2*m)
    g1h = 4*pi -(2*m + 1)**2*(3*m + 4)*factorial(m - S.Half)**2/factorial(m + 1)**2

    g = gosper_sum(f1a, (n, 0, m))
    assert g is not None and simplify(g - g1a) == 0
    g = gosper_sum(f1b, (n, 0, m))
    assert g is not None and simplify(g - g1b) == 0
    g = gosper_sum(f1c, (n, 0, m))
    assert g is not None and simplify(g - g1c) == 0
    g = gosper_sum(f1d, (n, 0, m))
    assert g is not None and simplify(g - g1d) == 0
    g = gosper_sum(f1e, (n, 0, m))
    assert g is not None and simplify(g - g1e) == 0
    g = gosper_sum(f1f, (n, 0, m))
    assert g is not None and simplify(g - g1f) == 0
    g = gosper_sum(f1g, (n, 0, m))
    assert g is not None and simplify(g - g1g) == 0
    g = gosper_sum(f1h, (n, 0, m))
    # need to call rewrite(gamma) here because we have terms involving
    # factorial(1/2)
    assert g is not None and simplify(g - g1h).rewrite(gamma) == 0

