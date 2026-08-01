
def test_gosper_nan():
    a = Symbol('a', positive=True)
    b = Symbol('b', positive=True)
    n = Symbol('n', integer=True)
    m = Symbol('m', integer=True)
    f2d = n*(n + a + b)*a**n*b**n/(factorial(n + a)*factorial(n + b))
    g2d = 1/(factorial(a - 1)*factorial(
        b - 1)) - a**(m + 1)*b**(m + 1)/(factorial(a + m)*factorial(b + m))
    g = gosper_sum(f2d, (n, 0, m))
    assert simplify(g - g2d) == 0

